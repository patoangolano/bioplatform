# Configuração DNS — bio.quackai.com.br

## Pré-requisitos

- Domínio `quackai.com.br` registrado na Registro.br
- Acesso ao painel de DNS da Registro.br
- VPS Hostinger com IP: `187.77.232.5`

## Passo a passo (Registro.br)

1. Acesse https://registro.br e faça login
2. Clique no domínio `quackai.com.br`
3. Vá em **DNS** → **Editar zona**
4. Adicione o seguinte registro:

| Tipo | Nome | Valor | TTL |
|------|------|-------|-----|
| A | bio | 187.77.232.5 | 3600 |

5. Salve as alterações

## Verificação

Após salvar, a propagação leva de 5 minutos a 2 horas. Verifique com:

```bash
# Linux/Mac
dig bio.quackai.com.br +short

# Windows
nslookup bio.quackai.com.br
```

O resultado esperado é `187.77.232.5`.

## HTTPS automático

Quando o DNS propagar e o Caddy estiver rodando na VPS:

1. O Caddy detecta o domínio `bio.quackai.com.br` no Caddyfile
2. Solicita certificado Let's Encrypt automaticamente
3. HTTPS fica ativo sem intervenção manual

**Requisitos para o HTTPS funcionar:**
- Porta 80 aberta (challenge HTTP-01 do Let's Encrypt)
- Porta 443 aberta
- DNS já propagado (registro A apontando para o IP)
- Firewall quackai-fw ativada (já feito — portas 80/443 liberadas)

## Troubleshooting

| Problema | Solução |
|----------|---------|
| `dig` retorna IP errado | Aguarde propagação DNS (até 48h em casos raros) |
| Caddy não gera certificado | Verifique se portas 80/443 estão abertas no firewall |
| ERR_CONNECTION_REFUSED | Verifique se `docker compose ps` mostra Caddy rodando |
| Certificate error no browser | Aguarde ~2 min após primeiro start para emissão do cert |

## IPv6 (opcional)

Se quiser suporte IPv6, adicione também:

| Tipo | Nome | Valor | TTL |
|------|------|-------|-----|
| AAAA | bio | 2a02:4780:6e:2b3d::1 | 3600 |
