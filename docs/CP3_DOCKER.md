# CP3 — Execução e validação com Docker

## Objetivo

O ambiente Docker do FinChat executa o frontend, a API, o Ollama e a preparação do modelo local. A API aplica as migrations antes de iniciar, pode popular dados de demonstração e usa SQLite em volume persistente. O frontend é servido por Nginx e encaminha `/api/` para a API sem expor configuração interna ao navegador.

## Pré-requisitos

- Docker Desktop com containers Linux e Docker Compose v2.
- Pelo menos 4 GB livres para imagens e modelo local.
- Portas `5173`, `8080` e `11434` livres, ou portas alternativas no `.env`.
- Um `JWT_SECRET_KEY` aleatório com pelo menos 32 caracteres.

Gere a chave sem usar um serviço externo:

```powershell
docker run --rm python:3.11-slim-bookworm python -c "import secrets; print(secrets.token_urlsafe(48))"
Copy-Item .env.example .env
```

Cole o valor em `JWT_SECRET_KEY` no `.env`. Nunca publique o `.env`.

## Variáveis principais

```dotenv
JWT_SECRET_KEY=SUBSTITUA_POR_UMA_CHAVE_FORTE
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=http://localhost:5173
FINCHAT_PORT=8080
FRONTEND_PORT=5173
OLLAMA_PORT=11434
OLLAMA_MODEL=gemma3:1b
LLM_ENABLED=true
SEED_DEMO_DATA=true
```

Se já existir Ollama na porta `11434`, use `OLLAMA_PORT=11435`. A comunicação interna entre API e Ollama permanece em `11434`.

## Construir e iniciar

```powershell
docker compose config --quiet
docker compose up -d --build --wait
docker compose ps
```

Na primeira inicialização, `ollama-model` baixa `gemma3:1b`. O tempo depende da rede e da máquina. O serviço termina com código zero depois do download; isso é esperado.

Com `SEED_DEMO_DATA=true`, o seed idempotente roda na inicialização. Caso a opção esteja desativada:

```powershell
docker compose exec api python -m app.seed
```

## URLs

- Aplicação: `http://127.0.0.1:5173`
- Swagger: `http://127.0.0.1:8080/docs`
- Saúde: `http://127.0.0.1:8080/health`
- Ollama: `http://127.0.0.1:11434` ou a porta definida em `OLLAMA_PORT`

## Verificação

```powershell
Invoke-RestMethod http://127.0.0.1:8080/health
$env:CP3_VALIDATE_AI='true'
.\.venv\Scripts\python.exe scripts\cp3_validate.py
Remove-Item Env:\CP3_VALIDATE_AI
docker compose exec api python -m pytest -q -p no:cacheprovider
```

O script HTTP cria uma transação temporária e a exclui ao final. Quando `CP3_VALIDATE_AI=true`, ele também exige que a resposta venha do Ollama, sem fallback.

## Logs e manutenção

```powershell
docker compose logs --tail 100 api
docker compose logs --tail 100 frontend
docker compose logs --tail 100 ollama
docker compose stop
docker compose start --wait
docker compose down
```

`docker compose down` preserva os volumes. Não use `docker compose down --volumes` se quiser conservar o banco e o modelo.

## Persistência e segurança

- Banco: volume `finchat_finchat_data`, montado em `/app/data`.
- Modelos: volume `finchat_ollama_data`.
- API: usuário não privilegiado `finchat` (UID 10001).
- Frontend: Nginx sem privilégios (UID 101).
- `.env`, `.git`, bancos locais, evidências e dependências locais não entram nas imagens.
- O frontend adiciona cabeçalhos de segurança; a API também adiciona proteção contra MIME sniffing, frame embedding e permissões de navegador desnecessárias.

## Solução de problemas

| Sintoma | Ação |
| --- | --- |
| Porta já em uso | Altere `FINCHAT_PORT`, `FRONTEND_PORT` ou `OLLAMA_PORT` no `.env`. |
| `dockerDesktopLinuxEngine` indisponível | Inicie o Docker Desktop e aguarde o engine ficar pronto. |
| Modelo demora a responder | Aguarde o primeiro carregamento; confira `docker compose logs ollama`. |
| IA usa fallback | Confira `LLM_ENABLED`, o modelo baixado e a saúde do Ollama. O fallback é comportamento suportado. |
| API não inicia | Confira `JWT_SECRET_KEY` e execute `docker compose logs api`. |
| Dados de demo ausentes | Defina `SEED_DEMO_DATA=true` ou execute o seed manualmente. |

Evidências desta validação estão em `evidencias/docker/` e `evidencias/testes/`.
