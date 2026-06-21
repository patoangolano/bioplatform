# Plano de Uso — Hostinger API MCP

## Objetivo

Usar os MCPs da Hostinger para automação de infraestrutura da VPS diretamente via Claude Code.

## MCPs Disponíveis

- `hostinger-vps` — gerenciamento de VPS (listar, reiniciar, snapshots)
- `hostinger-dns` — gerenciamento de zonas DNS
- `hostinger-domains` — domínios registrados
- `hostinger-billing` — informações de faturamento

## Fases de Adoção

### Fase 1 — Inspeção (atual)
- Listar VPS disponíveis
- Verificar IP, hostname, recursos (RAM, CPU, disco)
- Validar estado operacional

### Fase 2 — DNS
- Configurar registros A/AAAA apontando para a VPS
- Configurar CNAME para subdomínios (api.*, www.*)

### Fase 3 — Automação
- Criar snapshots antes de cada deploy
- Agendar snapshots periódicos via script

### Fase 4 — Monitoramento
- Verificar estado da VPS periodicamente
- Reiniciar automaticamente se necessário (com confirmação)

## Regras de Segurança

- Operações destrutivas (deletar, recriar) requerem confirmação explícita
- Sempre verificar retorno do MCP antes de prosseguir
- Registrar toda operação executada

## Status

MCPs conectados e testáveis. Aguardando primeiro uso operacional real.
