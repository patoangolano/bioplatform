# Migrations do Banco de Dados

## Convenções

- Migrations são numeradas sequencialmente: `001_`, `002_`, `003_`, etc.
- Sempre usar `BEGIN`/`COMMIT` para garantir atomicidade — se algo falhar, nenhuma alteração parcial é aplicada.
- Cada arquivo deve conter um cabeçalho com descrição e data.

## Como executar

Executar manualmente com:

```bash
docker exec -i bioplatform-postgres-1 psql -U $POSTGRES_USER -d $POSTGRES_DB < migration.sql
```

Exemplo:

```bash
docker exec -i bioplatform-postgres-1 psql -U bioplatform -d bioplatform < infra/db/migrations/001_initial_schema.sql
```

## Futuro

Integrar com [Alembic](https://alembic.sqlalchemy.org/) para migrations automáticas, versionamento e rollback controlado.
