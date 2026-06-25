import { useEffect, useRef, useState, type FormEvent } from "react";
import { useSearchParams } from "react-router-dom";
import { Search } from "lucide-react";
import clsx from "clsx";
import { api, errorMessage } from "../lib/api";
import type { BlastJob, BlastSubmitResponse } from "../lib/types";
import { Card, CardTitle, Empty } from "../components/ui";

const PROGRAMS = ["blastp", "blastn", "blastx", "tblastn", "tblastx"] as const;
type Program = (typeof PROGRAMS)[number];

function statusTone(status: string): string {
  const s = status.toLowerCase();
  if (s.includes("complet") || s.includes("success") || s.includes("done"))
    return "text-accent";
  if (s.includes("fail") || s.includes("error")) return "text-danger";
  return "text-warning";
}

export default function Blast() {
  const [params] = useSearchParams();
  const [sequenceId, setSequenceId] = useState(params.get("sequence") ?? "");
  const [program, setProgram] = useState<Program>("blastp");
  const [database, setDatabase] = useState("nr");
  const [limit, setLimit] = useState(10);

  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [job, setJob] = useState<BlastJob | null>(null);
  const poll = useRef<number | undefined>(undefined);

  useEffect(() => {
    return () => {
      if (poll.current) window.clearInterval(poll.current);
    };
  }, []);

  const finished = (s?: string) => {
    const v = (s ?? "").toLowerCase();
    return v.includes("complet") || v.includes("fail") || v.includes("error") || v.includes("done");
  };

  const startPolling = (jobId: string) => {
    if (poll.current) window.clearInterval(poll.current);
    poll.current = window.setInterval(async () => {
      try {
        const j = await api.get<BlastJob>(`/blast/jobs/${jobId}`);
        setJob(j);
        if (finished(j.status)) {
          if (poll.current) window.clearInterval(poll.current);
        }
      } catch (err) {
        setError(errorMessage(err, "Falha ao consultar o job."));
        if (poll.current) window.clearInterval(poll.current);
      }
    }, 3000);
  };

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setJob(null);
    if (!sequenceId.trim()) {
      setError("Informe o ID da sequência.");
      return;
    }
    setBusy(true);
    try {
      const res = await api.post<BlastSubmitResponse>("/blast/submit", {
        sequence_id: isNaN(Number(sequenceId)) ? sequenceId : Number(sequenceId),
        program,
        database,
        limit,
      });
      setJob({ job_id: res.job_id, status: res.status });
      startPolling(res.job_id);
    } catch (err) {
      setError(errorMessage(err, "Não foi possível submeter o BLAST."));
    } finally {
      setBusy(false);
    }
  };

  const running = job ? !finished(job.status) : false;

  return (
    <div className="space-y-5">
      <header>
        <h1 className="text-2xl font-extrabold tracking-tight">BLAST</h1>
        <p className="mt-1 text-text-muted">
          Submeta uma busca BLAST por ID de sequência e acompanhe o job até concluir.
        </p>
      </header>

      <div className="grid gap-6 lg:grid-cols-2">
        <form onSubmit={onSubmit} className="card space-y-4 p-5">
          <div>
            <label className="label" htmlFor="seqid">
              ID da sequência
            </label>
            <input
              id="seqid"
              className="input font-mono"
              placeholder="123"
              value={sequenceId}
              onChange={(e) => setSequenceId(e.target.value)}
            />
          </div>

          <div>
            <span className="label">Programa</span>
            <div className="flex flex-wrap gap-1.5">
              {PROGRAMS.map((p) => (
                <button
                  key={p}
                  type="button"
                  onClick={() => setProgram(p)}
                  aria-pressed={program === p}
                  className={clsx(
                    "rounded-lg border px-3 py-1.5 font-mono text-xs transition-colors",
                    program === p
                      ? "border-accent bg-accent/10 text-accent"
                      : "border-border text-text-muted hover:text-text-primary",
                  )}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label" htmlFor="db">
                Banco de dados
              </label>
              <input
                id="db"
                className="input font-mono"
                placeholder="nr"
                value={database}
                onChange={(e) => setDatabase(e.target.value)}
              />
            </div>
            <div>
              <label className="label" htmlFor="limit">
                Limite
              </label>
              <input
                id="limit"
                type="number"
                min={1}
                max={500}
                className="input font-mono"
                value={limit}
                onChange={(e) => setLimit(Math.max(1, Number(e.target.value) || 1))}
              />
            </div>
          </div>

          {error && (
            <p className="rounded-lg border border-danger/40 bg-danger/10 px-3 py-2 text-sm text-danger">
              {error}
            </p>
          )}

          <button type="submit" disabled={busy || running} className="btn-primary w-full shadow-glow">
            <Search size={18} aria-hidden="true" />
            {busy ? "Submetendo…" : running ? "Job em execução…" : "Submeter BLAST"}
          </button>
        </form>

        <div>
          {!job ? (
            <Empty
              title="Nenhum job ainda."
              hint="Submeta uma busca para acompanhar o status aqui."
              icon={<Search size={28} />}
            />
          ) : (
            <Card>
              <CardTitle
                icon={<Search size={18} />}
                badge={
                  <span className={clsx("chip", statusTone(job.status))}>
                    {running && (
                      <span className="h-2 w-2 animate-pulseDot rounded-full bg-warning" />
                    )}
                    {job.status}
                  </span>
                }
              >
                Job BLAST
              </CardTitle>

              <dl className="space-y-1.5 font-mono text-xs text-text-muted">
                <Row k="job_id" v={job.job_id} />
                {job.started_at && <Row k="started" v={job.started_at} />}
                {job.completed_at && <Row k="completed" v={job.completed_at} />}
              </dl>

              {job.error_message && (
                <p className="mt-3 rounded-lg border border-danger/40 bg-danger/10 px-3 py-2 text-sm text-danger">
                  {job.error_message}
                </p>
              )}

              {job.results !== undefined && job.results !== null && (
                <div className="mt-3">
                  <p className="mb-1 text-xs uppercase tracking-wide text-text-muted">
                    Resultados
                  </p>
                  <pre className="max-h-80 overflow-auto rounded-lg border border-border bg-bg-base/60 p-3 font-mono text-[11px] text-text-primary">
                    {JSON.stringify(job.results, null, 2)}
                  </pre>
                </div>
              )}
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}

function Row({ k, v }: { k: string; v: string }) {
  return (
    <div className="flex gap-2">
      <dt className="w-20 shrink-0 text-text-muted/70">{k}</dt>
      <dd className="min-w-0 break-all text-text-primary">{v}</dd>
    </div>
  );
}
