# Testes funcionais, automatizados e de integração — CP3

Execução final: 18/10/2026

## Ambiente

- Windows 11, Python 3.11 no `.venv`, Node.js e Docker Desktop.
- Frontend CP3 em `http://127.0.0.1:5173`, servido por Nginx no container.
- API CP3 em `http://127.0.0.1:8080` e também acessível pelo proxy `/api/v1` do frontend.
- SQLite persistente no volume `finchat_finchat_data`.
- Ollama no container, com `gemma3:1b` no volume `finchat_ollama_data`.
- Dados fictícios do seed; nenhum dado financeiro real foi usado.

## Cenários executados

### CT-01 — Comunicação frontend/API/banco

- **Funcionalidade:** integração entre Nginx, FastAPI e banco.
- **Pré-condições:** Compose com frontend e API saudáveis.
- **Passos:** acessar `GET /api/v1/health` pela porta 5173.
- **Entrada:** nenhuma.
- **Esperado:** HTTP 200, `status=ok`, `database=ok`, `environment=CP3`.
- **Obtido:** exatamente o envelope esperado.
- **Status:** **APROVADO**.
- **Evidência:** `evidencias/testes/cenarios_http_cp3.json` e `evidencias/docker/validacao_compose.txt`.

### CT-02 — Criação, persistência, consulta e consolidação

- **Funcionalidade:** fluxo principal de transação CPF.
- **Pré-condições:** usuário demo CPF autenticado e categoria de despesa existente.
- **Passos:** consultar dashboard; criar despesa temporária de R$ 12,34; consultar a transação; consultar o dashboard novamente; remover a transação.
- **Entrada:** descrição única, valor `12.34`, data corrente, tipo `EXPENSE`, origem `CASH`.
- **Esperado:** criação HTTP 201, item presente na listagem e despesas do dashboard acrescidas em R$ 12,34.
- **Obtido:** criação, leitura e consolidação confirmadas; limpeza HTTP 200 executada ao final.
- **Status:** **APROVADO**.
- **Evidência:** `evidencias/testes/cenarios_http_cp3.json` e logs do proxy em `evidencias/docker/logs_servicos.txt`.

### CT-03 — Entrada monetária inválida

- **Funcionalidade:** validação e falha controlada.
- **Pré-condições:** usuário CPF autenticado.
- **Passos:** tentar criar transação com valor zero.
- **Entrada:** `amount="0.00"`.
- **Esperado:** HTTP 422, código `VALIDATION_ERROR`, sem persistência.
- **Obtido:** HTTP 422 com envelope padronizado.
- **Status:** **APROVADO**.
- **Evidência:** `evidencias/testes/cenarios_http_cp3.json`.

### CT-04 — Autorização CPF/CNPJ

- **Funcionalidade:** proteção da área empresarial.
- **Pré-condições:** usuário CPF autenticado.
- **Passos:** consultar `GET /partners`.
- **Entrada:** JWT válido de perfil CPF.
- **Esperado:** HTTP 403 e código `FORBIDDEN`.
- **Obtido:** bloqueio 403 conforme a regra.
- **Status:** **APROVADO**.
- **Evidência:** `evidencias/testes/cenarios_http_cp3.json`.

### CT-05 — Consulta empresarial CNPJ

- **Funcionalidade:** leitura de parceiros e contratos.
- **Pré-condições:** usuário demo CNPJ autenticado e seed aplicado.
- **Passos:** consultar `GET /partners` e `GET /contracts`.
- **Entrada:** JWT válido de perfil CNPJ.
- **Esperado:** HTTP 200 e coleções não vazias.
- **Obtido:** dois parceiros e dois contratos.
- **Status:** **APROVADO**.
- **Evidência:** `evidencias/testes/cenarios_http_cp3.json`.

### CT-06 — Login e recuperação de perfil pelo frontend

- **Funcionalidade:** autenticação integrada.
- **Pré-condições:** usuário fictício `cpf@finchat.demo` existente.
- **Passos:** efetuar login pelo proxy e consultar `/auth/me`.
- **Entrada:** credencial exclusivamente demonstrativa do seed.
- **Esperado:** token Bearer e perfil `CPF`, sem exposição do hash.
- **Obtido:** login e leitura do perfil aprovados.
- **Status:** **APROVADO**.
- **Evidência:** `evidencias/testes/cenarios_http_cp3.json`.

### CT-07 — Ollama real no fluxo Docker

- **Funcionalidade:** análise inteligente local.
- **Pré-condições:** serviço Ollama saudável, `gemma3:1b` baixado e usuário CPF com movimentações.
- **Passos:** enviar o período corrente para `/ai/financial-analysis` pelo frontend.
- **Entrada:** `2026-10-01` a `2026-10-18`.
- **Esperado:** schema estruturado, `analysis_source=ollama`, `fallback_used=false`.
- **Obtido:** resposta válida do Ollama sem fallback.
- **Status:** **APROVADO**.
- **Evidência:** `evidencias/testes/cenarios_http_cp3.json` e logs do Ollama.

### CT-08 — Inspeção visual e responsiva

- **Funcionalidade:** login e dashboard React.
- **Pré-condições:** frontend Docker saudável.
- **Passos:** abrir o sistema em navegador controlável; entrar como CPF; conferir cards, gráfico, transações, navegação e logout; repetir em 390 × 844.
- **Entrada:** credencial fictícia do seed.
- **Esperado:** dados da API visíveis, sem erro de console aparente, e logout acessível no celular.
- **Obtido:** dashboard exibido corretamente em desktop e celular.
- **Status:** **APROVADO**.
- **Evidência:** `evidencias/testes/login_cp3_container.png` e inspeção controlada registrada em 17/10/2026.

## Testes automatizados

| Suíte | Resultado real |
| --- | --- |
| Pytest local | **96 passed**, 2 avisos de depreciação de dependências |
| Pytest dentro do container da API | **96 passed**, 2 avisos de depreciação de dependências |
| Vitest frontend | **3 passed** |
| TypeScript + Vite | Build aprovado, 2.243 módulos transformados |
| `npm audit` | **0 vulnerabilidades** |

O CP3 acrescentou três testes em `tests/test_cp3.py`: porta dinâmica e seed opcional do container; rejeição de porta inválida; health check CP3 com cabeçalhos HTTP defensivos.

## Correções realizadas durante os testes

1. O frontend não fazia parte do Compose: foi criada imagem multi-stage Node/Nginx e proxy para a API.
2. O processo da API usava porta fixa: agora respeita `PORT` e rejeita valores fora de 1–65535.
3. O seed de demonstração passou a ser opcional por `SEED_DEMO_DATA`, útil no ambiente acadêmico publicado.
4. API e frontend receberam cabeçalhos `nosniff`, `DENY`, `no-referrer` e política de permissões.
5. A identidade visível e o OpenAPI/health foram atualizados de CP2 para CP3.

## Reproduzir

```powershell
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider
cd frontend
npm.cmd test -- --run
npm.cmd run build
npm.cmd audit
cd ..
docker compose up -d --build --wait
docker compose exec -T api pytest -q -p no:cacheprovider
$env:CP3_VALIDATE_AI='true'
.\.venv\Scripts\python.exe scripts\cp3_validate.py
```

Os avisos Pytest vêm da transição de compatibilidade entre `fastapi/starlette` e uma futura versão do `httpx`; não causaram falha funcional e estão registrados integralmente nos logs.

## Validação pública — 20/10/2026

O mesmo fluxo HTTP foi executado contra `https://finchat-cp3-api.onrender.com/api/v1`. CT-01 a CT-06 foram aprovados, incluindo criação e limpeza de uma transação temporária. A análise pública retornou origem `deterministic`, resumo financeiro e duas recomendações. Em navegador controlável, o login CPF e o dashboard foram exibidos corretamente em `https://finchat-cp3.onrender.com`.

Evidências: `evidencias/deploy/verificacao_urls.json` e `evidencias/deploy/validacao_publica.json`.
