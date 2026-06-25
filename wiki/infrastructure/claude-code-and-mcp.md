---
title: "Claude Code e MCP"
slug: "claude-code-and-mcp"
type: infrastructure
status: active
created: 2026-06-23
updated: 2026-06-23
tags:
  - infrastructure
  - claude-code
  - mcp
  - ferramenta:claude-code
  - dominio:bioinformatica
source_count: 0
source_files: []
related_pages:
  - "[[tooling-stack]]"
  - "[[project-architecture]]"
  - "[[vps-setup]]"
  - "[[bioinformatics-project]]"
---

# Claude Code e MCP

O [[Claude Code]] e a interface primaria de desenvolvimento e execucao da [[bioplatform]], substituindo editores tradicionais por um ambiente de terminal com IA que escreve, depura, implanta e consulta pipelines em linguagem natural. O ciclo de trabalho tipico envolve edicao de codigo, execucao de analises, interacao com o banco de dados e orquestracao de containers Docker -- tudo mediado pelo Claude Code como agente central, com acesso direto ao sistema de arquivos e a shells persistentes no VPS.

## MCP -- Model Context Protocol

O MCP e o protocolo que conecta o Claude Code a ferramentas externas, permitindo que o modelo acesse bases de dados, APIs cientificas e utilitarios de bioinformatica como funcoes nativas. Cada servidor MCP expoe um conjunto de operacoes (tools) que o Claude Code descobre e invoca automaticamente. Nao ha cola manual entre sistemas: o protocolo negocia schemas JSON estaticos, e o Claude Code decide quando e como chamar cada ferramenta com base no contexto da conversa.

## 15 Servidores MCP de Bioinformatica

Implantados no VPS Hostinger KVM4 via **Streamable HTTP** (substituto do SSE em producao), os 15 servidores cobrem todo o ciclo de analise genomica:

| # | Servidor | Funcao Principal |
|---|----------|------------------|
| 1 | NCBI Datasets | Genomas, genes, anotacoes e taxonomia |
| 2 | UniProt | Proteínas, dominios, variantes e vias |
| 3 | BLAST | Alinhamento de sequencias contra NCBI |
| 4 | BWA | Alinhamento de reads (BWA-MEM, BWA-ALN) |
| 5 | SAMtools | Manipulacao de BAM/SAM, estatisticas |
| 6 | bcftools | Chamada e filtragem de variantes |
| 7 | bedtools | Operacoes com intervalos genomicos |
| 8 | FastQC | Controle de qualidade de reads |
| 9 | SeqKit | Processamento de FASTA/FASTQ |
| 10 | MyGene/BioThings | Busca de genes por simbolo, ID ou ontologia |
| 11 | MyVariant/BioThings | Busca de variantes por rsID ou HGVS |
| 12 | MyChem/BioThings | Informacao quimica por InChIKey ou PubChem |
| 13 | MyTaxon/BioThings | Taxonomia por NCBI ID ou nome cientifico |
| 14 | OpenGenes | Genes associados a longevidade e envelhecimento |
| 15 | SynergyAge | Epistasia genetica e efeitos de longevidade |

Cada servidor roda em container Docker com imagem Python minimal, expondo um endpoint `/mcp` unico consumido pelo Claude Code via configuracao `mcpServers` no `claude_desktop_config.json`. Consulte [[mcp-servers]] para o catalogo completo com schemas de entrada e saida.

## Servidores MCP Locais

Alem dos servidores remotos, quatro servidores MCP rodam diretamente na maquina de desenvolvimento (Windows + WSL2):

- **PostgreSQL MCP** (`pg-mcp-server-stuzero`) -- Consultas SQL diretas ao banco `bioplatform`, leitura de schemas e dados de projetos. Ponte entre linguagem natural e SQL sem cliente intermediario.
- **Obsidian MCP** (`obsidian-mcp-server`) -- Leitura, escrita e busca na wiki local do Obsidian. Permite que o Claude Code navegue e atualize a base de conhecimento enquanto trabalha.
- **Docker MCP** (`docker-mcp-py`) -- Gerenciamento de containers, imagens, redes e volumes Docker. Implanta, inspeciona e depura servicos diretamente do Claude Code.
- **Filesystem MCP** -- Acesso ao sistema de arquivos alem do workspace padrao, com operacoes de leitura, escrita, busca e listagem de diretorios.

## Implicacoes de Arquitetura

O modelo Claude Code + MCP elimina a necessidade de scripts wrapper para integrar ferramentas: o prompt em linguagem natural e a camada de abstracao. Isso significa que um fluxo como "buscar o gene BRCA1 no NCBI, alinhar com BWA contra hg38 e chamar variantes com bcftools" pode ser executado como uma unica conversa encadeada, com cada etapa chamando o servidor MCP correspondente. Para detalhes da infraestrutura que hospeda esse ecossistema, consulte [[vps-setup]] e [[tooling-stack]].
