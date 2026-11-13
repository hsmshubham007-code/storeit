# Security baseline

- Keep secrets in an ignored local `.env` file; never commit it.
- Commit only placeholder values in `.env.example`.
- Do not use company accounts, credentials, files, databases, or services.
- Do not add cloud-provider credentials until the relevant integration is designed
  and explicitly approved.
- Do not claim encryption, authentication, authorization, or recovery features
  exist until they are implemented and tested.
