import { useEffect, useState } from "react";
import { ShieldCheck, Lock } from "lucide-react";
import { api, ApiError, errorMessage } from "../lib/api";
import type { AdminStats, UserRead } from "../lib/types";
import { useAuth } from "../lib/auth";
import { Card, Empty, Skeleton } from "../components/ui";

export default function Admin() {
  const { user } = useAuth();
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [statsUnavailable, setStatsUnavailable] = useState(false);
  const [users, setUsers] = useState<UserRead[] | null>(null);
  const [usersUnavailable, setUsersUnavailable] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const isAdmin = Boolean(user?.is_admin);

  useEffect(() => {
    if (!isAdmin) {
      setLoading(false);
      return;
    }
    let alive = true;
    (async () => {
      try {
        const s = await api.get<AdminStats>("/admin/stats");
        if (alive) setStats(s);
      } catch (err) {
        if (!alive) return;
        if (err instanceof ApiError && err.status === 404) setStatsUnavailable(true);
        else setError(errorMessage(err, "Falha ao carregar estatísticas."));
      }
      try {
        const u = await api.get<UserRead[]>("/admin/users");
        if (alive) setUsers(Array.isArray(u) ? u : []);
      } catch (err) {
        if (!alive) return;
        if (err instanceof ApiError && err.status === 404) setUsersUnavailable(true);
        else setError((prev) => prev ?? errorMessage(err, "Falha ao carregar usuários."));
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, [isAdmin]);

  if (!isAdmin) {
    return (
      <div className="mx-auto max-w-md py-16">
        <Empty
          title="Acesso restrito"
          hint="Esta área é exclusiva para administradores. Se você acredita que deveria ter acesso, fale com o responsável pela plataforma."
          icon={<Lock size={30} />}
        />
      </div>
    );
  }

  const statEntries: { label: string; key: keyof AdminStats }[] = [
    { label: "Usuários", key: "total_users" },
    { label: "Sequências", key: "total_sequences" },
    { label: "Jobs totais", key: "total_jobs" },
    { label: "Jobs ativos", key: "active_jobs" },
    { label: "Concluídos", key: "completed_jobs" },
    { label: "Falhados", key: "failed_jobs" },
  ];

  return (
    <div className="space-y-6">
      <header className="flex items-center gap-2.5">
        <ShieldCheck className="text-accent" size={22} />
        <h1 className="text-2xl font-extrabold tracking-tight">Admin</h1>
      </header>

      {error && (
        <p className="rounded-lg border border-danger/40 bg-danger/10 px-3 py-2 text-sm text-danger">
          {error}
        </p>
      )}

      <section>
        <h2 className="mb-3 text-lg font-bold">Estatísticas</h2>
        {loading ? (
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <Skeleton key={i} className="h-20 w-full" />
            ))}
          </div>
        ) : statsUnavailable ? (
          <Empty title="Endpoint indisponível." hint="GET /admin/stats não respondeu (404)." />
        ) : (
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
            {statEntries.map(({ label, key }) => (
              <Card key={key} className="p-4">
                <p className="text-xs uppercase tracking-wide text-text-muted">{label}</p>
                <p className="mt-1 font-display text-2xl font-extrabold">
                  {stats?.[key] ?? "—"}
                </p>
              </Card>
            ))}
          </div>
        )}
      </section>

      <section>
        <h2 className="mb-3 text-lg font-bold">Usuários</h2>
        {loading ? (
          <Skeleton className="h-32 w-full" />
        ) : usersUnavailable ? (
          <Empty title="Endpoint indisponível." hint="GET /admin/users não respondeu (404)." />
        ) : users && users.length > 0 ? (
          <div className="overflow-x-auto rounded-xl border border-border">
            <table className="w-full text-left text-sm">
              <thead className="bg-bg-surface-2/60 text-xs uppercase tracking-wide text-text-muted">
                <tr>
                  <th className="px-4 py-2.5 font-medium">ID</th>
                  <th className="px-4 py-2.5 font-medium">E-mail</th>
                  <th className="px-4 py-2.5 font-medium">Nome</th>
                  <th className="px-4 py-2.5 font-medium">Papel</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {users.map((u) => (
                  <tr key={String(u.id)} className="hover:bg-bg-surface-2/40">
                    <td className="px-4 py-2.5 font-mono text-xs text-text-muted">{u.id}</td>
                    <td className="px-4 py-2.5 font-mono text-xs text-text-primary">{u.email}</td>
                    <td className="px-4 py-2.5 text-text-primary">{u.full_name || "—"}</td>
                    <td className="px-4 py-2.5">
                      <span
                        className={
                          u.is_admin
                            ? "chip text-accent"
                            : "chip text-text-muted"
                        }
                      >
                        {u.is_admin ? "admin" : "usuário"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <Empty title="Nenhum usuário encontrado." />
        )}
      </section>
    </div>
  );
}
