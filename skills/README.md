# Skills — Protocolos Institucionais para Claude Code

Skills são protocolos padronizados que condicionam o comportamento do agente AI
durante análises bioinformáticas. Reduzem desperdício de contexto e garantem
consistência entre sessões e pesquisadores.

## Estrutura

```
skills/
├── protocols/     — Workflows passo-a-passo
├── thresholds/    — Parâmetros numéricos de filtragem
└── templates/     — Formatos de saída padronizados
```

## Uso

Claude Code lê os arquivos automaticamente quando referenciados no CLAUDE.md.
Para usar um protocolo específico, mencione-o na conversa:

> "Analise esta sequência seguindo o protocolo de BLAST analysis"

O agente aplicará os parâmetros e regras definidos no skill correspondente.

## Criando Novos Skills

1. Escolha a categoria (protocol, threshold, template)
2. Crie um arquivo .md ou .yaml na pasta apropriada
3. Siga o formato dos exemplos existentes
4. Inclua classificação de proveniência quando aplicável
