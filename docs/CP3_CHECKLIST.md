# CP3 — Checklist final

Atualizado em 20/10/2026.

| Entregável | Estado | Evidência/observação |
| --- | --- | --- |
| CP1 e CP2 preservados | Concluído | Suíte completa aprovada |
| Diagnóstico técnico | Concluído | `docs/CP3_DIAGNOSTICO.md` |
| Cinco ou mais cenários reais | Concluído | CT-01 a CT-08 em `docs/CP3_TESTES.md` |
| Dois ou mais testes automatizados novos | Concluído | 3 testes CP3 e 1 regressão direcionada |
| Suíte backend | Concluído | 96 aprovados, local e Docker |
| Suíte frontend | Concluído | 3 aprovados |
| Build frontend | Concluído | Build Vite aprovado |
| Auditoria de dependências frontend | Concluído | 0 vulnerabilidades no `npm audit` |
| Dockerfile/Compose | Concluído | API, frontend/Nginx, Ollama e model-init |
| Migrations e seed no container | Concluído | Inicialização automatizada e testada |
| Ollama real | Concluído | `analysis_source=ollama`, sem fallback |
| Fallback determinístico | Concluído | Coberto pela suíte automatizada |
| Inspeção visual em navegador controlável | Concluído | Desktop e viewport móvel; captura em evidências |
| Cabeçalhos básicos de segurança | Concluído | API e Nginx |
| Configuração de deploy | Concluído | `render.yaml` e `docs/CP3_DEPLOY.md` |
| Deploy público executado | Concluído | Blueprint Render aplicado; API e frontend `Deployed` |
| Fluxo principal na URL pública | Concluído | Health, login, dashboard, CRUD temporário, autorização e análise validados |
| Monetização | Concluído | `docs/CP3_MONETIZACAO.md` |
| Backlog/Trello | Parcial | Quadro verificado; cartões externos não foram alterados |
| Roteiro da apresentação | Concluído | `docs/CP3_APRESENTACAO.md` |
| Vídeo/link da apresentação | **Pendente** | Gravação depende da equipe |
| README atualizado | Concluído | Instruções e estado real do CP3 |
| ZIP sanitizado | Concluído após empacotamento | `CP3_FINCHAT_GRUPO_PROVISORIO.zip` |
| Envio ao GitHub | Concluído | `RafaelHidekiYamada/finchat3`, branch `main` |

## Pendências que exigem ação externa

1. Gravar a apresentação e adicionar o link ao README.
2. Se desejado, transportar o backlog local para o Trello.
3. Para uso além da demonstração, contratar ou liberar um banco persistente e alterar `DATABASE_URL`.

Essas pendências não são apresentadas como concluídas e não invalidam a execução local verificada.
