import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Dna, FlaskConical } from "lucide-react";
import { api, errorMessage } from "../lib/api";
import type { SequenceResponse } from "../lib/types";
import { Empty, Skeleton } from "../components/ui";

const PAGE = 20;

export default function Sequences() {
  const [items, setItems] = useState<SequenceResponse[] | null>(null);
  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    (async () => {
      try {
        const list = await api.get<SequenceResponse[]>(
          `/sequences?limit=${PAGE}&offset=${offset}`,
        );
        if (!alive) return;
        const safe = Array.isArray(list) ? list : [];
        setItems((prev) => (offset === 0 ? safe : [...(prev ?? []), ...safe]));
        setHasMore(safe.length === PAGE);
      } catch (err) {
        if (alive) {
          setError(errorMessage(err, "Não foi possível carregar as sequências."));
          setItems((prev) => prev ?? []);
        }
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, [offset]);

  return (
    <div className="space-y-5">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-extrabold tracking-tight">Sequências</h1>
          <p className="mt-1 text-text-muted">Todas as sequências que você registrou.</p>
        </div>
        <Link to="/submit" className="btn-primary">
          <FlaskConical size={18} aria-hidden="true" />
          Submeter sequência
        </Link>
      </header>

      {error && (
        <p className="rounded-lg border border-danger/40 bg-danger/10 px-3 py-2 text-sm text-danger">
          {error}
        </p>
      )}

      {items === null ? (
        <div className="space-y-2">
          {[0, 1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-16 w-full" />
          ))}
        </div>
      ) : items.length === 0 ? (
        <Empty
          title="Nenhuma sequência registrada."
          hint="Submeta sua primeira sequência para vê-la listada aqui."
          icon={<Dna size={28} />}
        />
      ) : (
        <>
          <ul className="space-y-2">
            {items.map((s) => (
              <li key={s.id}>
                <Link
                  to={`/sequences/${s.id}`}
                  className="flex items-center gap-3 rounded-xl border border-border bg-bg-surface/60 px-4 py-3 transition-colors hover:border-accent/40"
                >
                  <span className="font-mono text-sm text-accent">#{s.id}</span>
                  <span className="chip shrink-0">{s.sequence_type}</span>
                  {s.organism && (
                    <span className="hidden shrink-0 text-xs italic text-text-muted sm:inline">
                      {s.organism}
                    </span>
                  )}
                  <span className="min-w-0 flex-1 truncate font-mono text-xs text-text-muted">
                    {s.raw_sequence?.slice(0, 64) || s.description || "—"}
                  </span>
                </Link>
              </li>
            ))}
          </ul>

          {hasMore && (
            <button
              className="btn-ghost mx-auto block"
              disabled={loading}
              onClick={() => setOffset((o) => o + PAGE)}
            >
              {loading ? "Carregando…" : "Carregar mais"}
            </button>
          )}
        </>
      )}
    </div>
  );
}
