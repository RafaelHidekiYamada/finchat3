# CP3 — Roteiro de apresentação

Tempo sugerido: 7 a 8 minutos. Antes de gravar, inicie o Compose, confira os dados de demonstração e feche telas que exibam `.env`, token JWT ou informações pessoais.

## 1. Abertura — 30 s

Apresentar o FinChat como aplicação full stack para controle financeiro pessoal e empresarial. Explicar que o CP3 preserva CP1/CP2 e acrescenta validação, empacotamento, preparação de deploy e proposta de monetização.

## 2. Problema e público — 30 s

Pessoas e pequenos negócios precisam visualizar saldo, receitas, despesas, parceiros e contratos sem depender de planilhas fragmentadas. O produto atende perfis CPF e CNPJ com permissões distintas.

## 3. Arquitetura — 45 s

Mostrar brevemente: React estático → FastAPI/JWT → serviços/repositórios → SQLite. O Docker local também inclui Nginx e Ollama; no Render gratuito, regras determinísticas mantêm a análise funcionando e o SQLite é efêmero.

## 4. Ambiente reproduzível — 45 s

Mostrar `docker compose ps`: frontend, API e Ollama saudáveis; `ollama-model` concluído. Explicar migrations automáticas, seed opcional, volumes persistentes e execução sem privilégios.

## 5. Demonstração CPF — 2 min

1. Abrir `http://127.0.0.1:5173`.
2. Entrar com `cpf@finchat.demo` e `FinChatDemo!2026`.
3. Mostrar dashboard, contas, categorias e transações.
4. Criar uma despesa pequena e confirmar atualização do dashboard.
5. Abrir Análise inteligente e mostrar `analysis_source` quando pertinente.
6. Excluir a movimentação criada para preservar o estado da demo.

## 6. Demonstração CNPJ — 1 min

Entrar com `empresa@finchat.demo` e a mesma senha fictícia. Mostrar parceiros, contratos e visão empresarial. Explicar que o backend retorna `403` quando CPF tenta acessar essas rotas.

## 7. Qualidade e evidências — 45 s

Apresentar o resultado: 96 testes backend, 3 testes frontend, build aprovado, auditoria npm sem vulnerabilidades e cenários HTTP reais. Mostrar `docs/CP3_TESTES.md` e a pasta `evidencias/`.

## 8. Deploy — 30 s

Abrir `https://finchat-cp3.onrender.com`, mostrar o Blueprint aplicado e explicar a API Docker e o frontend estático. Destacar a limitação do banco efêmero no plano acadêmico gratuito.

## 9. Monetização — 45 s

Apresentar planos Gratuito, Pessoal e Negócio, cenário de receita, custos estimados e ponto de equilíbrio. Reforçar que são hipóteses acadêmicas a validar com usuários.

## 10. Limitações e próximos passos — 30 s

Open Finance e WhatsApp são simulados; Ollama público não está incluído; o plano gratuito pode suspender a API e recriar o banco efêmero. Próximos passos: banco persistente, vídeo final e teste de preço.

## 11. Encerramento — 15 s

Destacar que a entrega é reproduzível, testada, documentada e honesta sobre o que está local, simulado ou ainda pendente.

## Plano de contingência

- Se o Ollama estiver carregando, demonstre o fallback e mostre a evidência do teste real já registrado.
- Se Docker falhar, use as evidências e explique como reproduzir.
- Se o serviço gratuito estiver retomando após inatividade, aguarde o health check e use as evidências públicas registradas.
- Nunca exponha `JWT_SECRET_KEY`, `.env` ou um token completo na gravação.
