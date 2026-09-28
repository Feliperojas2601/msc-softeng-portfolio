// ============================================================================
// mock-data.ts — Datos hardcodeados para W02-detalle-alarma, extraídos con
// fidelidad exacta de Figma (nodo 121:107) vía Figma MCP.
// ============================================================================

export interface DayChip {
  label: string;
  active: boolean;
}

export const ALARM_DAYS: DayChip[] = [
  { label: 'L', active: true },
  { label: 'M', active: true },
  { label: 'X', active: true },
  { label: 'J', active: true },
  { label: 'V', active: true },
  { label: 'S', active: false },
  { label: 'D', active: false },
];

export interface AlarmDatum {
  label: string;
  value: string;
}

export const ALARM_DATA: AlarmDatum[] = [
  { label: 'RETO', value: 'Escritura · 57 caracteres' },
  { label: 'ÚLTIMA DESACTIVACIÓN', value: 'Hoy a las 06:39' },
  { label: 'RACHA', value: '5 días seguidos' },
];

export type DonutVariant = 'exito' | 'acento' | 'peligro';

export interface DonutSlice {
  label: string;
  percent: number;
  variant: DonutVariant;
}

export const DISTRIBUTION: DonutSlice[] = [
  { label: 'Reto completado', percent: 68, variant: 'exito' },
  { label: 'Pospuesta', percent: 22, variant: 'acento' },
  { label: 'Salida de emergencia', percent: 10, variant: 'peligro' },
];

export interface ResponseBar {
  day: string;
  seconds: number;
  heightPx: number;
  highlighted: boolean;
}

export const RESPONSE_TIME: ResponseBar[] = [
  { day: 'L', seconds: 18, heightPx: 70, highlighted: false },
  { day: 'M', seconds: 24, heightPx: 93, highlighted: false },
  { day: 'X', seconds: 15, heightPx: 58, highlighted: false },
  { day: 'J', seconds: 31, heightPx: 120, highlighted: true },
  { day: 'V', seconds: 22, heightPx: 85, highlighted: false },
  { day: 'S', seconds: 12, heightPx: 46, highlighted: false },
  { day: 'D', seconds: 27, heightPx: 105, highlighted: false },
];

export type HistoryStatusVariant = 'exito' | 'peligro';

export interface HistoryItem {
  title: string;
  subtitle: string;
  status: string;
  statusVariant: HistoryStatusVariant;
}

export const RECENT_HISTORY: HistoryItem[] = [
  { title: 'Hoy · 06:30', subtitle: 'Completada en 39 s', status: 'Reto completado', statusVariant: 'exito' },
  { title: 'Ayer · 06:30', subtitle: 'Salida de emergencia a los 34 s', status: 'Salida de emergencia', statusVariant: 'peligro' },
];

export interface MockUser {
  initials: string;
  name: string;
  email: string;
}

export const CURRENT_USER: MockUser = {
  initials: 'PA',
  name: 'Paula Alarcón',
  email: 'paula.abc@gmail.com',
};
