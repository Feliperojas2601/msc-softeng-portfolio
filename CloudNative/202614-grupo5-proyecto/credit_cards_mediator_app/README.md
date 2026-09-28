# credit_cards_mediator_app

Worker de RF-006 desplegado como contenedor (no Lambda) junto al resto de
las apps. No atiende peticiones HTTP: `src/worker.py` corre un loop
continuo (`while`, síncrono, sin `asyncio` ni hilos) que cada ~2 segundos
reclama eventos pendientes con
`POST /credit-cards/internal/verification-events/claim` (Bearer de
servicio), y por cada uno consulta
`GET /credit-cards/internal/{cardId}/verification` para recuperar el
propietario, RUV, estado, últimos cuatro dígitos y franquicia. La API nunca
entrega el token de pagos en esta operación.

## Por qué contenedor y no Lambda

El diseño original usaba Lambda + SQS (`credit_cards_app` publicaba un
mensaje al crear la tarjeta). Se descartó porque los pods de EKS corren con
el rol `LabEksNodeRole` (provisto por AWS Academy), sin permisos de SQS, y
Academy Learner Lab bloquea por completo adjuntarle una política nueva
(`iam:AttachRolePolicy` devuelve `AccessDenied`, verificado en vivo):
`credit_cards_app` nunca podía publicar en la cola.

Se probó luego una Lambda disparada por EventBridge (sin SQS, con polling
HTTP), pero `rate(1 minute)` es el mínimo que permite EventBridge —
demasiado lento frente a las pruebas de la entrega, que revisan el estado
pocos segundos después de crear la tarjeta. Un segundo disparador (Function
URL pública) tampoco sirve: su hostname es dinámico y solo existe después
de `post_k8s_stacks`, cuando `credit_cards_app` ya se desplegó sin poder
conocerlo (mismo problema de orden que evitó `identity_webhook_app`).

Un contenedor con su propio loop no tiene ninguna de estas restricciones:
no necesita ningún permiso de AWS (solo llama por HTTP a TrueNative,
`credit_cards_app`, `users_app` y `notifications_app` por DNS de clúster,
igual que `identity_webhook_app`), y no depende de ningún mínimo de
intervalo externo — puede reclamar cada 2 segundos indefinidamente. La
restricción de "sin tareas en segundo plano" (`docs/requerimientos/rf-006.md`)
es específica de `credit_cards_app`; el propio diseño ya asume que el
polling vive "en componentes separados".

Si el estado es `POR_VERIFICAR`, consulta TrueNative. Un `202` libera la
reserva mediante `POST /credit-cards/internal/verification-events/{eventId}/release`,
enviando `leaseId` y Bearer de servicio. El evento queda disponible tras un
segundo para el siguiente ciclo. Cada reclamo reserva un evento durante
60 segundos; esa reserva protege el procesamiento y permite recuperarlo si
el worker cae. Una reserva ajena, vencida o ya liberada recibe `409`.
Un resultado terminal se guarda mediante `PATCH` a la
misma ruta interna y el evento se confirma con
`POST /credit-cards/internal/verification-events/{eventId}/ack`.

Para una tarjeta terminal, consulta `GET /users/{userId}` y envía
`POST {NOTIFICATIONS_API_BASE_URL}/notify` con el contrato:

```json
{
  "type": "CREDIT_CARD_VERIFICATION",
  "userId": "owner-123",
  "email": "owner@example.com",
  "fullName": null,
  "status": "VERIFICADA",
  "ruv": "ruv-123",
  "lastFourDigits": "1234",
  "franchise": "VISA"
}
```

`APROBADA` permanece en la base de tarjetas y se traduce a `VERIFICADA`
solo en el correo. `RECHAZADA` se conserva. El correo se obtiene de
usuarios, no del evento reclamado. No se transmite PAN, CVV, token de pagos
ni Bearer del usuario.

## Reintentos

Si falla usuarios, la consulta interna, TrueNative o notificaciones
(incluido HTTP 502 o timeout), `process_event` propaga la excepción,
`run_once` la registra como fallo y el evento queda sin `ack` — el
siguiente ciclo posterior al vencimiento de la reserva lo vuelve a intentar.
Los fallos temporales al reclamar eventos se registran y el worker continúa
en el próximo ciclo, sin terminar el proceso. No se revierte una
aprobación ni un rechazo. Al reintentar, el estado ya persistido permite
saltar TrueNative y el `PATCH`, y repetir únicamente la consulta del
destinatario, el `POST /notify` y el `ack`.

La entrega de notificaciones es al menos una vez: si el `ack` falla después
de un `POST /notify` exitoso, el siguiente ciclo reprocesa el evento y
puede reenviar el correo. No existe deduplicación durable del correo en
`notifications_app`. El flujo de identidad conserva su manejo best-effort.

## Evento reclamado

Cada elemento devuelto por `claim` tiene esta forma (ver
`VerificationOutboxRepository.claim` en `credit_cards_app`):

```json
{
  "eventId": "verification-123",
  "cardId": "card-123",
  "ruv": "ruv-123",
  "attempt": 0,
  "leaseId": "lease-123"
}
```

## Configuración

| Variable | Uso |
| --- | --- |
| TRUE_NATIVE_BASE_URL | URL accesible de TrueNative. |
| TRUE_NATIVE_SECRET_TOKEN | Token exclusivo de TrueNative. |
| CARDS_API_BASE_URL | URL accesible de tarjetas. |
| CARDS_API_SECRET | Mismo valor que CREDIT_CARDS_INTERNAL_SECRET en tarjetas. |
| USERS_API_BASE_URL | URL de usuarios, sin /users. |
| NOTIFICATIONS_API_BASE_URL | URL accesible de notificaciones, sin /notify. |

No se reenvía CARDS_API_SECRET ni el token de TrueNative a usuarios o
notificaciones. El cliente HTTP rechaza redirecciones.

## Despliegue

`k8s/aws/credit_cards_mediator_app.yml` — un `Deployment` simple, sin
`Service` ni `Ingress` (no atiende peticiones) y sin probes (no expone
HTTP; un proceso caído se reinicia igual vía el ciclo de vida normal del
pod).

## Pruebas

```powershell
python -m pytest -q
```
