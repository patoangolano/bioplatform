import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Dna, FlaskConical } from "lucide-react";
import { api, errorMessage } from "../lib/api";
import type { SequenceResponse } from "../lib/types";
import { useAuth } from "../lib/auth";
import SequenceStrip from "../components/SequenceStrip";
import { Card, Empty, Skeleton } from "../components/ui";

export default function Dashboard() {
  const { user } = useAuth();
  const [recent, setRecent] = useState<SequenceResponse[] | null>(null);
  const [total, setTotal] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const list = await api.get<SequenceResponse[]>("/sequences?limit=6&offset=0");
        if (!alive) return;
        const safe = Array.isArray(list) ? list : [];
        setRecent(safe);
        setTotal(safe.length);
      } catch (err) {
        if (alive) {
          setError(errorMessage(err, "Não foi possível carregar suas sequências."));
          setRecent([]);
        }
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  return (
    <div className="space-y-6">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold tracking-tight">
            Olá{user?.full_name ? `, ${user.full_name.split(" ")[0]}` : ""}.
          </h1>
          <p className="mt-1 text-text-muted">
            Submeta uma sequência e obtenha análise multi-fonte com proveniência.
          </p>
        </div>
        <Link to="/submit" className="btn-primary shadow-glow">
          <FlaskConical size={18} aria-hidden="true" />
          Submeter sequência
        </Link>
      </header>

      {/* hero banner */}
      <Card className="overflow-hidden">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div className="max-w-md">
            <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-accent">
              quackai biolab
            </p>
            <h2 className="mt-1 font-display text-xl font-bold">
              sequência → análise multi-fonte instantânea
            </h2>
            <p className="mt-1 text-sm text-text-muted">
              UniProt, PubMed, InterPro, AlphaFold e STRING — cada resultado carimbado com
              proveniência.
            </p>
          </div>
          <div className="min-w-0 flex-1 md:max-w-sm">
            <SequenceStrip max={88} seed={2024} />
          </div>
        </div>
      </Card>

      {/* stats */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
        <Stat label="Suas sequências" value={total} hint="recentes carregadas" />
        <Stat label="Fontes integradas" value={5} hint="UniProt · PubMed · …" />
        <Stat label="Proveniência" value="100%" hint="por resultado" />
      </div>

      {/* recent */}
      <section>
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-lg font-bold">Sequências recentes</h2>
          <Link
            to="/sequences"
            className="inline-flex items-center gap-1 text-sm text-accent hover:underline"
          >
            ver todas <ArrowRight size={14} />
          </Link>
        </div>

        {error && (
          <p className="mb-3 rounded-lg border border-danger/40 bg-danger/10 px-3 py-2 text-sm text-danger">
            {error}
          </p>
        )}

        {recent === null ? (
          <div className="space-y-2">
            {[0, 1, 2].map((i) => (
              <Skeleton key={i} className="h-16 w-full" />
            ))}
          </div>
        ) : recent.length === 0 ? (
          <Empty
            title="Nenhuma sequência ainda."
            hint="Submeta sua primeira sequência para começar a ver análises aqui."
            icon={<Dna size={28} />}
          />
        ) : (
          <ul className="space-y-2">
            {recent.map((s) => (
              <li key={s.id}>
                <Link
                  to={`/sequences/${s.id}`}
                  className="flex items-center gap-3 rounded-xl border border-border bg-bg-surface/60 px-4 py-3 transition-colors hover:border-accent/40"
                >
                  <span className="font-mono text-sm text-accent">#{s.id}</span>
                  <span className="chip shrink-0">{s.sequence_type}</span>
                  <span className="min-w-0 flex-1 truncate font-mono text-xs text-text-muted">
                    {s.raw_sequence?.slice(0, 48) || s.description || "—"}
                  </span>
                  <ArrowRight size={16} className="shrink-0 text-text-muted" />
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

function Stat({
  label,
  value,
  hint,
}: {
  label: string;
  value: number | string | null;
  hint?: string;
}) {
  return (
    <Card className="p-4">
      <p className="text-xs uppercase tracking-wide text-text-muted">{label}</p>
      <p className="mt-1 font-display text-2xl font-extrabold text-text-primary">
        {value === null ? "—" : value}
      </p>
      {hint && <p className="mt-0.5 font-mono text-[11px] text-text-muted/70">{hint}</p>}
    </Card>
  );
}
