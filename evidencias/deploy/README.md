# Evidência de deploy

Em 18/10/2026, as URLs antecipadas pelo `render.yaml` foram consultadas e responderam `404`, conforme `verificacao_urls.json`.

Isso comprova somente que **não existe deploy público validado nesses endereços**. Como a versão CP3 permanece local por solicitação do usuário, nenhum serviço foi criado e nenhuma alegação de publicação foi feita.

Depois de autorizado o envio ao repositório e aplicado o Blueprint, esta pasta deve receber:

- URL real do frontend e da API;
- resposta de `/health`;
- captura do login/dashboard público;
- data/hora e resultado do fluxo principal;
- eventuais ajustes de CORS e nomes atribuídos pelo Render.
