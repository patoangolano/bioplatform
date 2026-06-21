# Deploy Guide — bioplatform na VPS Hostinger

## Resumo da infraestrutura

| Componente | Detalhe |
|-----------|---------|
| VPS | Hostinger KVM4, 4 vCPU, 16GB RAM, 200GB disco |
| IP | 187.77.232.5 |
| OS | Ubuntu 24.04 (Docker + Traefik pré-instalados) |
| Domínio | bio.quackai.com.br |
| Proxy | Caddy (substitui Traefik) |
| Firewall | quackai-fw (ativada, portas 22/80/443/ICMP) |

## Pré-requisitos

1. **DNS configurado** — siga `docs/DNS_SETUP.md`
2. **Acesso SSH** à VPS: `ssh root@187.77.232.5`
3. **Repositório acessível** — via git clone ou tarball

## Deploy — Primeiro uso

### 1. Bootstrap da VPS

```bash
ssh root@187.77.232.5

# Baixa o projeto
git clone https://github.com/SEU_USUARIO/bioplatform.git /opt/bioplatform
cd /opt/bioplatform

# Executa bootstrap (instala deps, cria user, configura UFW)
chmod +x infra/scripts/bootstrap-vps.sh
./infra/scripts/bootstrap-vps.sh
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
nano .env
```

**Variáveis obrigatórias para produção:**

| Variável | O que mudar |
|----------|-------------|
| `POSTGRES_PASSWORD` | Senha forte (mínimo 16 chars) |
| `DATABASE_URL` | Mesma senha do POSTGRES_PASSWORD |
| `API_SECRET_KEY` | String aleatória de 32+ chars |
| `DOMAIN` | `bio.quackai.com.br` (já preenchido) |
| `ALLOWED_ORIGINS` | `https://bio.quackai.com.br` |
| `NCBI_API_KEY` | Opcional (aumenta rate limit PubMed) |

**Gerar secrets seguros:**
```bash
# Gera senha de 32 chars
openssl rand -base64 32
```

### 3. Deploy

```bash
chmod +x infra/scripts/deploy.sh
./infra/scripts/deploy.sh
```

O script automaticamente:
- Desabilita o Traefik pré-instalado
- Executa migrações do banco
- Builda as imagens Docker
- Sobe todos os serviços
- Verifica health check

### 4. Verificar

```bash
# Status dos containers
docker compose ps

# Health check
curl https://bio.quackai.com.br/health

# Testar endpoint de sequências
curl -X POST https://bio.quackai.com.br/api/v1/sequences/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "BRCA1",
    "sequence_type": "protein",
    "raw_sequence": "MDLSALREVE",
    "organism": "Homo sapiens",
    "analyze": true
  }'
```

## Deploy — Atualizações subsequentes

```bash
ssh root@187.77.232.5
cd /opt/bioplatform
./infra/scripts/deploy.sh
```

Ou com tarball:
```bash
./infra/scripts/deploy.sh --tarball /tmp/bioplatform-v0.2.0.tar.gz
```

## Rollback

```bash
./infra/scripts/rollback.sh --tag v0.1.0
```

## Monitoramento

```bash
# Logs em tempo real
docker compose logs -f api

# Logs do Caddy (acesso)
docker compose logs -f caddy

# Uso de recursos
docker stats
```

## Portas e serviços

| Serviço | Porta interna | Porta externa | Notas |
|---------|--------------|---------------|-------|
| Caddy | 80, 443 | 80, 443 | Ponto de entrada único |
| API | 8000 | — | Acessível via Caddy |
| PostgreSQL | 5432 | 127.0.0.1:5432 | Apenas localhost |
| Redis | 6379 | 127.0.0.1:6379 | Apenas localhost |
| Worker | — | — | Sem porta exposta |

## Segurança

- ✅ Firewall Hostinger ativada (DROP default, ACCEPT em 22/80/443)
- ✅ PostgreSQL e Redis não expostos externamente
- ✅ Caddy como único ponto de entrada com HTTPS automático
- ✅ Headers de segurança (HSTS, X-Frame-Options, etc.)
- ✅ Containers rodam como non-root user
- ⚠️ Porta 3000 e 11434 abertas no firewall — remover se não usar

## Estrutura de volumes

| Volume | Conteúdo | Backup |
|--------|----------|--------|
| `pgdata` | Dados PostgreSQL | Sim — crítico |
| `redisdata` | Cache Redis | Não — recriável |
| `caddy_data` | Certificados TLS | Sim — evita rate limit Let's Encrypt |
| `caddy_config` | Config runtime | Não — recriável |

## Backup do banco

```bash
# Dump manual
docker compose exec postgres pg_dump -U bio biodb > backup_$(date +%Y%m%d).sql

# Restore
docker compose exec -T postgres psql -U bio biodb < backup_20260621.sql
```
