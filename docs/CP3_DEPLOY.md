# CP3 — Plano de deploy público

## Plataforma escolhida

O projeto foi preparado para o Render por meio de `render.yaml`:

- API FastAPI como Web Service Docker;
- frontend React como Static Site;
- PostgreSQL gerenciado;
- migrations e seed executados pelo processo de inicialização da API;
- análise determinística habilitada mesmo sem Ollama.

O Blueprint segue a especificação oficial do [Render](https://render.com/docs/blueprint-spec). A plataforma também documenta o fluxo de [primeiro deploy](https://render.com/docs/your-first-deploy), [serviços Docker](https://render.com/docs/docker) e [infraestrutura como código](https://render.com/docs/infrastructure-as-code).

## Estado real em 18/10/2026

**Deploy público não executado e URL pública não validada.** As URLs previstas no arquivo de configuração retornaram `404` durante a verificação, conforme `evidencias/deploy/verificacao_urls.json`.

O código CP3 está somente no computador local porque foi solicitado explicitamente que nada fosse enviado ao GitHub ainda. O Render não consegue construir esta versão sem que ela esteja em um repositório acessível ou seja enviada por outro mecanismo autorizado. Portanto, o projeto está preparado para deploy, mas não é correto declará-lo publicado.

## Variáveis do serviço da API

| Variável | Configuração no Blueprint |
| --- | --- |
| `JWT_SECRET_KEY` | Gerada pelo Render |
| `JWT_ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` |
| `DATABASE_URL` | Injetada pelo PostgreSQL do Blueprint |
| `CORS_ORIGINS` | URL HTTPS do frontend |
| `LLM_ENABLED` | `false` no plano público inicial |
| `SEED_DEMO_DATA` | `true` para avaliação acadêmica |

No frontend, `VITE_API_BASE_URL` aponta para a URL HTTPS da API. Se o Render atribuir sufixos diferentes, as duas URLs devem ser ajustadas antes do build definitivo.

## Por que o Ollama não está no deploy gratuito

O Ollama permanece disponível no Docker local. No ambiente público inicial, `LLM_ENABLED=false` mantém a análise por regras determinísticas, evitando depender de GPU, memória adicional ou uma API paga. A interface e o contrato da API continuam funcionais e informam a origem da análise.

## Passos para publicar depois da autorização

1. Revisar o diff e enviar a versão CP3 para uma branch do repositório.
2. No Render, criar um Blueprint apontando para `RafaelHidekiYamada/finchat3`.
3. Confirmar os três recursos definidos em `render.yaml`.
4. Aguardar o build, migrations, seed e healthcheck.
5. Substituir no Blueprint quaisquer URLs atribuídas com nomes diferentes.
6. Validar `/health`, login CPF/CNPJ, dashboard, transação e análise determinística.
7. Registrar URLs e capturas reais em `evidencias/deploy/` e atualizar README/checklist.

## Atualização e rollback

Com `autoDeployTrigger: commit`, novos commits no branch conectado iniciam novo build. Antes de atualizar produção, execute as suítes local e Docker. Em falha, use o rollback do serviço no painel e investigue os logs; mudanças de banco devem permanecer compatíveis com as migrations Alembic.

## Limitações do plano gratuito

Segundo a documentação de [instâncias gratuitas](https://render.com/docs/free), Web Services gratuitos podem adormecer após inatividade, o filesystem local é efêmero e bancos PostgreSQL gratuitos têm limites e expiração. O frontend estático pode ser hospedado como [Static Site](https://render.com/docs/static-sites). Essas condições tornam o plano adequado para demonstração acadêmica, não para produção comercial contínua.

Nenhuma compra, cobrança ou contratação de serviço foi realizada durante esta entrega.
