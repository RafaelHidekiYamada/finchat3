# CP3 — Deploy público no Render

## Estado comprovado em 20/10/2026

- Aplicação: <https://finchat-cp3.onrender.com>
- API: <https://finchat-cp3-api.onrender.com>
- Health check: <https://finchat-cp3-api.onrender.com/health>
- Repositório: <https://github.com/RafaelHidekiYamada/finchat3>
- Blueprint: `finchat-cp3`
- Serviços: `finchat-cp3-api` e `finchat-cp3`, ambos com estado `Deployed`.

O fluxo público foi validado de forma visual e por HTTP: health, login CPF, recuperação do perfil, dashboard, criação/leitura/exclusão de transação temporária, rejeição de entrada inválida, bloqueio CPF na área CNPJ, consultas CNPJ e análise determinística.

## Arquitetura publicada

- API FastAPI como Web Service Docker gratuito.
- Frontend React/Vite como Static Site global.
- SQLite efêmero em `/tmp/finchat.db` para a demonstração acadêmica.
- Migrations e seed idempotente executados na inicialização da API.
- `LLM_ENABLED=false`: análise pública por regras determinísticas.
- Ollama completo disponível no ambiente Docker local.

O Blueprint segue a especificação oficial do [Render](https://render.com/docs/blueprint-spec), usando [serviço Docker](https://render.com/docs/docker) e [Static Site](https://render.com/docs/static-sites).

## Ajuste necessário durante a publicação

A primeira sincronização tentou criar `finchat-cp3-db`, mas o workspace já possuía o máximo de um PostgreSQL gratuito ativo. O Render recusou o banco e cancelou a criação inicial da API. Nenhum plano pago foi contratado.

O `render.yaml` foi corrigido para usar `sqlite:////tmp/finchat.db`, a alteração foi enviada ao GitHub e o Blueprint sincronizado novamente. API e frontend foram implantados com sucesso. Como o filesystem gratuito é efêmero, os dados podem ser recriados após reinício; `SEED_DEMO_DATA=true` garante os usuários e registros fictícios da apresentação.

## Variáveis da API

| Variável | Valor/origem |
| --- | --- |
| `JWT_SECRET_KEY` | Gerada de forma segura pelo Render |
| `JWT_ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` |
| `DATABASE_URL` | `sqlite:////tmp/finchat.db` |
| `CORS_ORIGINS` | `https://finchat-cp3.onrender.com` |
| `LLM_ENABLED` | `false` |
| `SEED_DEMO_DATA` | `true` |

O frontend é construído com `VITE_API_BASE_URL=https://finchat-cp3-api.onrender.com/api/v1`.

## Publicação e atualização

1. Enviar alterações para a branch `main` de `RafaelHidekiYamada/finchat3`.
2. O Blueprint sincroniza o `render.yaml` automaticamente.
3. Aguardar o build e o health check da API.
4. Validar `GET /health` e o login no frontend.
5. Em caso de falha, consultar os logs do serviço e o histórico de Syncs do Blueprint.

## Credenciais fictícias de demonstração

| Perfil | E-mail | Senha |
| --- | --- | --- |
| CPF | `cpf@finchat.demo` | `FinChatDemo!2026` |
| CNPJ | `empresa@finchat.demo` | `FinChatDemo!2026` |

## Limitações

Segundo a documentação de [instâncias gratuitas](https://render.com/docs/free), o Web Service pode adormecer após inatividade e o filesystem é efêmero. A primeira requisição após suspensão pode demorar. Esta arquitetura atende à demonstração acadêmica, mas uma operação comercial precisa de PostgreSQL persistente, observabilidade, backups e plano de disponibilidade.

Nenhuma compra ou contratação paga foi realizada. Evidências estão em `evidencias/deploy/`.
