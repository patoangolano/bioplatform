import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft, Search } from "lucide-react";
import { api, errorMessage } from "../lib/api";
import type { SequenceWithAnalysis } from "../lib/types";
import SequenceStrip from "../components/SequenceStrip";
import AnalysisCards from "../components/AnalysisCards";
import { Card, Empty, Skeleton } from "../components/ui";
import { baseComposition } from "../lib/seq";

export default function SequenceDetail() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<SequenceWithAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    (async () => {
      try {
        const res = await api.get<SequenceWithAnalysis>(`/sequences/${id}`);
        if (alive) setData(res);
      } catch (err) {
        if (alive) setError(errorMessage(err, "Não foi possível carregar esta sequência."));
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, [id]);

  const seq = data?.sequence;
  const comp = seq ? baseComposition(seq.raw_sequence) : null;

  return (
    <div className="space-y-5">
      <Link
        to="/sequences"
        className="inline-flex items-center gap-1 text-sm text-text-muted hover:text-accent"
      >
        <ArrowLeft size={14} /> Sequências
      </Link>

      {loading ? (
        <div className="space-y-3">
          <Skeleton className="h-24 w-full" />
          <Skeleton className="h-40 w-full" />
        </div>
      ) : error ? (
        <Empty title={error} />
      ) : !seq ? (
        <Empty title="Sequência não encontrada." />
      ) : (
        <>
          <Card>
            <div className="flex flex-wrap items-center gap-2">
              <h1 className="text-xl font-extrabold tracking-tight">Sequência #{seq.id}</h1>
              <span className="chip">{seq.sequence_type}</span>
              {seq.organism && (
                <span className="text-sm italic text-text-muted">{seq.organism}</span>
              )}
              <Link
                to={`/blast?sequence=${seq.id}`}
                className="btn-ghost ml-auto px-3 py-1.5 text-sm"
              >
                <Search size={15} aria-hidden="true" />
                BLAST
              </Link>
            </div>
            {seq.description && (
              <p className="mt-2 text-sm text-text-primary/90">{seq.description}</p>
            )}
            <div className="mt-3">
              <SequenceStrip sequence={seq.raw_sequence} max={160} />
            </div>
            {comp && (
              <p className="mt-2 font-mono text-xs text-text-muted">
                {comp.total} bases · A {comp.counts.A} · C {comp.counts.C} · G {comp.counts.G} ·{" "}
                {comp.counts.U > 0 ? `U ${comp.counts.U}` : `T ${comp.counts.T}`}
              </p>
            )}
          </Card>

          {data?.analysis ? (
            <AnalysisCards analysis={data.analysis} />
          ) : (
            <Empty
              title="Sem análise registrada para esta sequência."
              hint="Reenvie a sequência com a análise ativada para gerar resultados."
            />
          )}
        </>
      )}
    </div>
  );
}
