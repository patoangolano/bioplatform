# Protocolo: Caracterização de Proteínas

## Pipeline Multi-Etapa

```
Sequência → BLAST → UniProt → InterPro → AlphaFold → STRING → Relatório
```

## Etapa 1: Busca de Homologia (BLAST)
- Programa: blastp
- Database: swissprot (primeiro), nr se necessário
- Threshold: e-value ≤1e-5, identity ≥30%, coverage ≥70%

## Etapa 2: Anotação Funcional (UniProt)
- Buscar top 3 hits por accession
- Extrair: função, GO terms, keywords, organism
- Priorizar entradas reviewed (Swiss-Prot) sobre TrEMBL

## Etapa 3: Domínios e Famílias (InterPro)
- Buscar domínios por nome da proteína e accession
- Identificar: domínios catalíticos, de ligação, regulatórios
- Mapear arquitetura de domínios

## Etapa 4: Estrutura 3D (AlphaFold)
- Buscar predição por UniProt ID
- Avaliar confiança: pLDDT >90 (muito alta), 70-90 (alta), 50-70 (baixa)
- Regiões com pLDDT <50: provavelmente desordenadas

## Etapa 5: Rede de Interações (STRING)
- Score mínimo: 700 (alta confiança)
- Limite: top 10 interatores
- Verificar enriquecimento funcional (GO, KEGG)

## Etapa 6: Relatório Consolidado
Estruturar como:
1. Identidade e classificação
2. Função e domínios
3. Estrutura e confiança
4. Rede de interações
5. Hipóteses para investigação experimental

## Proveniência
- Registrar cada etapa com: ferramenta, versão, timestamp, hash
- Classificar: observação (dados diretos), inferência (homologia), hipótese (predições)
