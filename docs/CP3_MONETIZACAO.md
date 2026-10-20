# CP3 — Proposta de monetização

## Mercado e proposta de valor

O problema central é a fragmentação do controle financeiro: pessoas e pequenos negócios registram movimentações em locais diferentes, perdem a visão de saldo e têm dificuldade para relacionar recebimentos e despesas a clientes, fornecedores ou contratos.

- **Público-alvo:** pessoas físicas, MEIs, profissionais autônomos e pequenos negócios.
- **Clientes potenciais:** usuários que hoje dependem de planilhas, anotações ou aplicativos que não combinam visão pessoal e empresarial.
- **Proposta de valor:** consolidar registros, dashboard, contratos e orientação financeira educacional em uma experiência simples, com separação CPF/CNPJ.
- **Benefícios:** menos tempo para organizar dados, identificação de gastos relevantes, acompanhamento de vencimentos e visão consolidada para decisão.
- **Diferenciais propostos:** operação local sem chave de IA paga, fallback previsível, minimização de dados enviados ao modelo e suporte a fluxos pessoais e empresariais no mesmo produto.

Esses diferenciais são hipóteses competitivas e precisam ser comparados com alternativas reais em pesquisa de mercado antes de qualquer lançamento.

## Modelo

O FinChat pode operar como SaaS freemium para pessoas e pequenos negócios. O plano gratuito facilita aquisição; os planos pagos financiam infraestrutura, suporte e evolução.

| Plano | Preço sugerido | Público | Recursos principais |
| --- | ---: | --- | --- |
| Gratuito | R$ 0/mês | Uso inicial | Controle manual, dashboard básico e fallback determinístico |
| Pessoal | R$ 19,90/mês | Pessoa física | Histórico ampliado, alertas, exportação e análises avançadas |
| Negócio | R$ 59,90/mês | MEI e pequeno negócio | Parceiros, contratos, relatórios e múltiplos usuários futuros |

Os preços são hipóteses comerciais para o trabalho acadêmico e exigem pesquisa com usuários antes de lançamento real.

## Cenário de receita

Hipótese: 150 assinantes Pessoal e 30 assinantes Negócio.

| Item | Cálculo | Valor mensal |
| --- | --- | ---: |
| Pessoal | 150 × R$ 19,90 | R$ 2.985,00 |
| Negócio | 30 × R$ 59,90 | R$ 1.797,00 |
| Receita recorrente | soma | **R$ 4.782,00** |

Receita recorrente anual hipotética: **R$ 57.384,00**.

## Custos mensais estimados

| Item | Natureza | Estimativa |
| --- | --- | ---: |
| Web Service Render pago | referência pública | US$ 7,00 |
| PostgreSQL gerenciado | hipótese conservadora | US$ 20,00 |
| Static Site | referência pública | US$ 0,00 |
| Câmbio de planejamento | hipótese: R$ 5,50/US$ | R$ 148,50 |
| Manutenção e suporte | hipótese: 20 h × R$ 80 | R$ 1.600,00 |
| Monitoramento/backups | hipótese | R$ 100,00 |
| Domínio | rateio estimado | R$ 5,00 |
| Contingência | hipótese | R$ 200,00 |
| Total estimado | — | **R$ 2.053,50** |

O preço oficial do Web Service básico deve sempre ser conferido na página de [preços do Render](https://render.com/pricing). Valores em dólar, banco, câmbio e horas são estimativas, não cotações nem compromissos de compra.

## Resultado e ponto de equilíbrio

- Resultado operacional hipotético: R$ 4.782,00 − R$ 2.053,50 = **R$ 2.728,50/mês**.
- Resultado anual hipotético: **R$ 32.742,00**.
- Ticket médio do cenário: R$ 4.782,00 ÷ 180 = **R$ 26,57**.
- Ponto de equilíbrio aproximado: R$ 2.053,50 ÷ R$ 26,57 = **78 assinantes pagantes**.

Não estão incluídos impostos, taxas de pagamento, marketing, LGPD/jurídico, atendimento em escala e eventuais APIs bancárias ou de mensageria. Uma operação real deve recalcular margem, churn, CAC, LTV e tributos.

## Riscos e condições de viabilidade

Principais riscos: baixa retenção, preço inadequado, custo de aquisição elevado, concorrência consolidada, suporte mais caro que o previsto, exigências de segurança/LGPD e aumento de custos de infraestrutura ou integrações.

Para o cenário se tornar viável, o produto precisa validar retenção e disposição de pagamento, manter isolamento e segurança dos dados, cobrar antes de ampliar custos fixos, acompanhar margem por plano e atingir aproximadamente 78 clientes no ticket médio assumido. Integrações bancárias ou de mensageria só devem entrar depois de análise jurídica, consentimento e orçamento próprios.

## Estratégia de validação

1. Medir ativação: primeiro registro financeiro e retorno em sete dias.
2. Testar intenção de pagamento com uma página de planos, sem cobrança automática.
3. Entrevistar pessoas físicas e MEIs sobre alertas, exportação e contratos.
4. Liberar o plano Pessoal para uma pequena coorte.
5. Só contratar infraestrutura maior após observar retenção e conversão.
