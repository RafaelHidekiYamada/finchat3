# Evidência de deploy

Em 20/10/2026, o Blueprint `finchat-cp3` foi aplicado no Render. A API Docker e o frontend estático aparecem como `Deployed`.

- Frontend: `https://finchat-cp3.onrender.com`
- API: `https://finchat-cp3-api.onrender.com`
- Health: `https://finchat-cp3-api.onrender.com/health`

`verificacao_urls.json` registra HTTP 200. `validacao_publica.json` registra os cenários reais executados contra a API pública. A inspeção em navegador controlável confirmou login e dashboard com os dados do seed.

A primeira tentativa de Blueprint falhou porque o workspace já tinha um banco PostgreSQL gratuito ativo. O deploy final usa SQLite efêmero e seed idempotente, sem contratar serviço pago.
