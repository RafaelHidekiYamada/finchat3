# Diagnóstico inicial do Checkpoint 3

Data da análise: 18/10/2026

## Estado preservado

O FinChat chega ao CP3 como uma aplicação full stack funcional. O repositório não contém `AGENTS.md`; portanto, não há instruções locais adicionais. O histórico Git estava limpo no início desta etapa e o banco local, o volume Docker e todas as funcionalidades dos CP1 e CP2 foram preservados.

| Camada | Tecnologia e estado encontrado |
| --- | --- |
| Frontend | React 18, TypeScript, Vite 7, React Router, Axios, Tailwind CSS 4 e Recharts. Possui autenticação, dashboard, CRUD financeiro, área CNPJ e análise inteligente. |
| Backend | FastAPI, Pydantic 2, SQLAlchemy 2, Alembic, JWT HS256 e Uvicorn. Respostas e erros usam envelopes padronizados. |
| Banco | SQLite na execução local/Docker, com suporte configurável a PostgreSQL via `psycopg`. Migrations `0001` e `0002`; valores monetários usam `Decimal`. |
| IA | Ollama local (`gemma3:1b`) com payload minimizado e fallback determinístico. Não depende de chave paga. |
| Contêineres | API e Ollama já possuíam Dockerfile/Compose validados no CP2; o frontend ainda era executado fora do Compose. |
| Testes | 93 testes Pytest e 3 testes Vitest aprovados ao fim do CP2. |
| Deploy | Não havia URL pública comprovada nem arquivo de infraestrutura como código. |

## Fluxos de negócio existentes

1. Cadastro e login de usuários CPF ou CNPJ, com senha derivada por PBKDF2 e token JWT com expiração, emissor e audiência.
2. Cadastro de contas, categorias e transações; cálculo de saldos e resumos sem uso de `float`.
3. Dashboard consolidado por período com receitas, despesas, alertas, fluxo mensal e transações recentes.
4. Área empresarial exclusiva para CNPJ, com clientes, fornecedores, contratos e resumos financeiros.
5. Simulação idempotente de conexão bancária e interpretação local de comandos de chat.
6. Análise financeira via Ollama, limitada a agregados, com schema validado e fallback determinístico.

## Segurança e integração

### Controles já presentes

- `.env`, bancos, logs, dependências e artefatos de build ignorados pelo Git.
- JWT exige `sub`, `iat`, `exp`, `iss` e `aud`; algoritmo fixado em HS256.
- Chave JWT obrigatória com pelo menos 32 caracteres e rejeição de marcadores.
- Senhas nunca retornadas; PBKDF2-SHA256 com salt e 600 mil iterações.
- Isolamento de dados por usuário e bloqueio da área CNPJ para perfis CPF.
- CORS somente com origens explícitas, sem curinga.
- Erros internos não retornam stack trace, SQL ou parâmetros.
- Ollama recebe apenas agregados financeiros, sem documento, contato, identidade ou token.

### Riscos e limitações identificados

| Item | Risco | Tratamento no CP3 |
| --- | --- | --- |
| Frontend fora do Compose | Demonstração dependia de Node instalado no host | Criar imagem Nginx sem privilégios e incluir o serviço no Compose. |
| Porta fixa no container da API | Incompatibilidade com plataformas que injetam `PORT` | Ler e validar `PORT`, mantendo 8000 como padrão. |
| Deploy sem banco persistente | SQLite é efêmero em serviços gratuitos | Preparar PostgreSQL gerenciado no Blueprint do Render. |
| Ollama incompatível com plano gratuito de 512 MB | Modelo local não cabe no serviço público gratuito | Desativar Ollama no deploy e usar o fallback determinístico; manter Ollama no ambiente local. |
| Cabeçalhos HTTP ausentes | Menor proteção contra sniffing, framing e recursos do navegador | Adicionar cabeçalhos defensivos na API e no Nginx. |
| Rate limiting distribuído ausente | Tentativas repetidas de login não são limitadas | Registrar como limitação conhecida; implementação correta exige armazenamento compartilhado. |
| Token em `localStorage` | Um XSS futuro poderia ler o token | Mitigar com ausência de HTML dinâmico, dependências auditadas e cabeçalhos; recomendar cookie HttpOnly em evolução futura. |
| PostgreSQL ainda não validado em produção pública | Depende da criação de conta/recurso externo | Blueprint e procedimento documentados; não declarar deploy antes de URL real responder. |

## Requisitos do CP3

| Requisito | Estado inicial | Ação definida |
| --- | --- | --- |
| Cinco cenários funcionais | Parcial: testes existiam, sem documento CP3 | Executar fluxos reais e registrar em `CP3_TESTES.md`. |
| Dois testes automatizados | Atendido quantitativamente | Acrescentar testes específicos de inicialização, produção e segurança. |
| Evidências reais | Evidências apenas dos CPs anteriores | Criar `evidencias/testes`, `evidencias/docker` e `evidencias/deploy`. |
| Dockerfile e Compose | Backend/Ollama atendidos | Adicionar frontend e validar comunicação completa. |
| Deploy público | Pendente | Preparar Render Blueprint gratuito e publicar somente se houver sessão/autorização. |
| Monetização | Pendente | Elaborar modelo SaaS freemium com premissas e viabilidade. |
| README CP3 | Pendente | Atualizar execução, resultados, deploy, limitações e links. |
| Organização ágil | Link do Trello já existe | Preservar o link e preparar backlog CP3 importável. |
| Apresentação | Apenas roteiro CP2 | Criar roteiro final CP3 com demonstração real. |
| Pacote ZIP | Pendente | Gerar pacote sanitizado, sem segredos, bancos ou dependências. |

## Decisões de implementação

- Preservar FastAPI, React, SQLAlchemy, SQLite local e Ollama; nenhuma migração de stack é necessária.
- Usar Nginx não privilegiado para o frontend no Docker e proxy interno para a API.
- Preparar Render por compatibilidade com Docker, FastAPI, site estático e PostgreSQL em um único Blueprint.
- Usar recursos gratuitos apenas para a demonstração acadêmica, sem contratação automática ou garantia de produção.
- Manter a análise determinística no deploy público e o Ollama local no Docker completo.
