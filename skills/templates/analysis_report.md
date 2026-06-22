# Template: Relatório de Análise de Sequência

## Estrutura Padrão

```markdown
# Relatório de Análise — [Nome/ID da Sequência]

## 1. Identificação
- Tipo: [DNA/RNA/proteína]
- Comprimento: [N] resíduos/bases
- Organismo: [se informado]
- Data: [timestamp]

## 2. Homologia (BLAST)
- Top hit: [accession] — [nome] ([organismo])
- Identidade: [X]% | Coverage: [Y]% | E-value: [Z]
- Classificação: [observação]

## 3. Anotação Funcional
- Função: [descrição UniProt]
- Domínios: [lista InterPro]
- GO Terms: [molecular function, biological process, cellular component]
- Classificação: [inferência]

## 4. Estrutura
- AlphaFold ID: [AF-XXXXX]
- Confiança global (pLDDT): [score]
- Modelo: [URL]
- Classificação: [observação]

## 5. Rede de Interações
- Parceiros principais: [lista STRING top 5]
- Enriquecimento: [top pathways KEGG/GO]
- Classificação: [inferência]

## 6. Literatura Relacionada
- [PMID] — [título] ([ano])
- [PMID] — [título] ([ano])

## 7. Hipóteses para Investigação
- [hipótese 1 baseada nos dados]
- [hipótese 2]
- Classificação: [hipótese]

## Proveniência
| Etapa | Ferramenta | Versão | Input Hash | Timestamp |
|-------|-----------|--------|------------|-----------|
| BLAST | NCBI BLAST | 2.15 | [hash] | [ISO8601] |
| UniProt | REST API | 2024_05 | [hash] | [ISO8601] |
| ... | ... | ... | ... | ... |
```

## Notas de Uso
- Sempre preencher a tabela de proveniência
- Separar claramente observação/inferência/hipótese
- Incluir links diretos para fontes (PubMed, UniProt, AlphaFold)
- Marcar seções geradas por IA com nota de proveniência
