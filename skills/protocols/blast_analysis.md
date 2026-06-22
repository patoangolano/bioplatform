# Protocolo: Análise BLAST

## Parâmetros Padrão

| Parâmetro | Proteína (blastp) | Nucleotídeo (blastn) |
|-----------|-------------------|----------------------|
| Database | swissprot (curado) | nt |
| E-value | 1e-5 | 1e-5 |
| Max hits | 50 | 50 |
| Word size | 3 | 11 |
| Matrix | BLOSUM62 | — |

## Limiares de Interpretação

- **Identidade ≥90%**: Ortólogo provável ou parálogo muito próximo
- **Identidade 50-90%**: Homólogo provável, mesma família proteica
- **Identidade 30-50%**: Homólogo distante, arquitetura de domínio compartilhada
- **Identidade <30%**: Zona crepuscular — requer validação estrutural (AlphaFold)

## Ações de Follow-up

1. Top hits com identidade ≥50% → buscar anotação UniProt
2. Hits com domínios novos → scan InterPro
3. Hits em organismos modelo → checar interações STRING
4. Questões estruturais → predição AlphaFold

## Classificação de Proveniência

| Dado | Classificação |
|------|---------------|
| Hit BLAST (e-value, score) | observação |
| Inferência de homologia | inferência |
| Predição funcional de homólogos distantes | hipótese |

## Critérios de Rejeição

- Descarte hits com coverage <50% da query
- Ignore hits com e-value >0.01 em modo padrão
- Marque como suspeito hits exclusivamente em sequências genômicas não-anotadas
