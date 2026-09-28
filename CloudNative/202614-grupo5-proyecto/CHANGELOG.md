# Changelog

All notable changes to `users_app` beyond the RF-007 change pre-approved in the
Entrega 3 statement are documented here, per the entrega's restrictions on
modifying components reused from previous entregas.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- `GET /users/{id}` in `users_app`, public by architectural decision (mirrors
  the already-public `PATCH /users/{id}`). Needed so the RF-007 identity
  verification webhook (a separate, decoupled component) can read a user's
  contact data (email, full name) to build the result notification email,
  without violating the rule that each app's data can only be read through
  the API of the app that owns it. Returns the same public profile shape as
  `GET /users/me`. Branch: `feature/rf007-identity-webhook`.
