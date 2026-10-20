# Evidência consolidada — CP3

Execução local: 18/10/2026. Deploy público: 20/10/2026. Fuso America/Sao_Paulo.

| Verificação | Resultado |
| --- | --- |
| `docker compose up -d --build --wait` | Aprovado |
| API container | Saudável em `127.0.0.1:8080` |
| Frontend container | Saudável em `127.0.0.1:5173` |
| Ollama container | Saudável em `127.0.0.1:11435` |
| Preparação `gemma3:1b` | Concluída com código 0 |
| Pytest local | 96 aprovados, 2 avisos de depreciação |
| Pytest no container | 96 aprovados, 2 avisos de depreciação |
| Vitest | 3 aprovados |
| Build Vite | 2.243 módulos transformados; aprovado |
| `npm audit` | 0 vulnerabilidades |
| Cenários HTTP CT-01 a CT-07 | Todos aprovados |
| Ollama real | `analysis_source=ollama`, `fallback_used=false` |
| Inspeção visual | Login, dashboard desktop e viewport móvel aprovados |
| Blueprint Render | API Docker e frontend estático `Deployed` |
| URLs públicas | Frontend, API e health check responderam HTTP 200 |
| Fluxo público | CT-01 a CT-06 aprovados contra a API pública |
| Análise pública | Origem `deterministic`, resumo e recomendações presentes |

Os avisos de backend vêm de aliases depreciados de `httpx`/Starlette em dependências, não de falha funcional. A suíte terminou com código 0.

Arquivos detalhados:

- `testes/cenarios_http_cp3.json`
- `testes/pytest_local.txt`
- `testes/pytest_docker.txt`
- `testes/vitest.txt`
- `testes/frontend_build.txt`
- `testes/npm_audit.txt`
- `testes/login_cp3_container.png`
- `docker/logs_servicos.txt`
- `docker/validacao_compose.txt`
- `deploy/verificacao_urls.json`
- `deploy/validacao_publica.json`

Nenhum segredo, token JWT ou arquivo `.env` foi incluído nas evidências.
