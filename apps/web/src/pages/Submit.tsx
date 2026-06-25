import { useMemo, useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { FlaskConical, Sparkles } from "lucide-react";
import clsx from "clsx";
import { api, ApiError, errorMessage } from "../lib/api";
import type {
  AnalysisResult,
  BiosafetyBlock,
  SequenceType,
  SequenceWithAnalysis,
} from "../lib/types";
import { baseColorVar, baseComposition } from "../lib/seq";
import SequenceStrip from "../components/SequenceStrip";
import AnalysisCards from "../components/AnalysisCards";
import { Banner, Card, Empty } from "../components/ui";

const TYPES: SequenceType[] = ["DNA", "RNA", "protein"];

export default function Submit() {
  const [type, setType] = useState<SequenceType>("DNA");
  const [organism, setOrganism] = useState("");
  const [description, setDescription] = useState("");
  const [seq, setSeq] = useState("");
  const [analyze, setAnalyze] = useState(true);

  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [biosafetyBlock, setBiosafetyBlock] = useState<BiosafetyBlock | null>(null);
  const [result, setResult] = useState<SequenceWithAnalysis | null>(null);

  const cleaned = useMemo(() => seq.replace(/\s+/g, "").toUpperCase(), [seq]);
  const comp = useMemo(() => baseComposition(cleaned), [cleaned]);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setBiosafetyBlock(null);
    setResult(null);
    if (!cleaned) {
      setError("Cole uma sequência antes de submeter.");
      return;
    }
    setBusy(true);
    try {
      const res = await api.post<SequenceWithAnalysis>("/sequences", {
        description: description || undefined,
        sequence_type: type,
        raw_sequence: cleaned,
        organism: organism || undefined,
        analyze,
      });
      setResult(res);
    } catch (err) {
      if (err instanceof ApiError && err.status === 403) {
        const d = (err.detail ?? {}) as BiosafetyBlock;
        setBiosafetyBlock(d);
      } else {
        setError(errorMessage(err, "Falha ao submeter a sequência."));
      }
    } finally {
      setBusy(false);
    }
  };

  const analysis: AnalysisResult | null = result?.analysis ?? null;

  return (
    <div>
      <header className="mb-6">
        <h1 className="text-2xl font-extrabold tracking-tight">Submeter & analisar</h1>
        <p className="mt-1 text-text-muted">
          Submeta uma sequência e receba análise multi-fonte instantânea — com proveniência em cada
          resultado.
        </p>
      </header>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* LEFT — form */}
        <form onSubmit={onSubmit} className="card space-y-5 p-5">
          {/* segmented type */}
          <div>
            <span className="label">Tipo de sequência</span>
            <div
              className="inline-flex rounded-xl border border-border bg-bg-base/50 p-1"
              role="radiogroup"
              aria-label="Tipo de sequência"
            >
              {TYPES.map((t) => (
                <button
                  key={t}
                  type="button"
                  role="radio"
                  aria-checked={type === t}
                  onClick={() => setType(t)}
                  className={clsx(
                    "rounded-lg px-4 py-1.5 text-sm font-medium transition-colors",
                    type === t
                      ? "bg-accent text-bg-base shadow-glow-sm"
                      : "text-text-muted hover:text-text-primary",
                  )}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="label" htmlFor="organism">
                Organismo <span className="text-text-muted/60">(opcional)</span>
              </label>
              <input
                id="organism"
                className="input"
                placeholder="Homo sapiens"
                value={organism}
                onChange={(e) => setOrganism(e.target.value)}
              />
            </div>
            <div>
              <label className="label" htmlFor="description">
                Descrição <span className="text-text-muted/60">(opcional)</span>
              </label>
              <input
                id="description"
                className="input"
                placeholder="GFP variante…"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>
          </div>

          <div>
            <label className="label" htmlFor="seq">
              Sequência bruta
            </label>
            <textarea
              id="seq"
              rows={6}
              className="input resize-y font-mono text-[13px] leading-relaxed tracking-wider"
              placeholder="ATGGTGAGCAAGGGCGAGGAG…"
              value={seq}
              onChange={(e) => setSeq(e.target.value)}
              spellCheck={false}
            />
            {cleaned ? (
              <div className="mt-3 space-y-2">
                <SequenceStrip sequence={cleaned} max={120} />
                <BaseStats comp={comp} />
              </div>
            ) : (
              <p className="mt-2 font-mono text-xs text-text-muted">
                {cleaned.length} bases — a prévia colorida aparece aqui.
              </p>
            )}
          </div>

          <label className="flex cursor-pointer items-center justify-between rounded-xl border border-border bg-bg-base/40 px-4 py-3">
            <span className="flex items-center gap-2 text-sm font-medium text-text-primary">
              <Sparkles size={16} className="text-accent" />
              Analisar na submissão
            </span>
            <input
              type="checkbox"
              className="h-5 w-5 accent-[#00E599]"
              checked={analyze}
              onChange={(e) => setAnalyze(e.target.checked)}
              aria-label="Analisar na submissão"
            />
          </label>

          {error && (
            <p className="rounded-lg border border-danger/40 bg-danger/10 px-3 py-2 text-sm text-danger">
              {error}
            </p>
          )}

          <button type="submit" disabled={busy} className="btn-primary w-full shadow-glow">
            <FlaskConical size={18} aria-hidden="true" />
            {busy ? "Submetendo…" : "Submeter sequência"}
          </button>
        </form>

        {/* RIGHT — results */}
        <div className="space-y-4">
          {biosafetyBlock && (
            <Banner tone="danger" title="Submissão bloqueada por biossegurança">
              <div className="space-y-2">
                {biosafetyBlock.risk_level && (
                  <p>
                    Nível de risco:{" "}
                    <span className="font-mono uppercase">{biosafetyBlock.risk_level}</span>
                  </p>
                )}
                {biosafetyBlock.recommendation && <p>{biosafetyBlock.recommendation}</p>}
                {biosafetyBlock.flags && biosafetyBlock.flags.length > 0 && (
                  <ul className="flex flex-wrap gap-1.5">
                    {biosafetyBlock.flags.map((f, i) => (
                      <li key={i} className="chip text-danger">
                        {f}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </Banner>
          )}

          {busy && (
            <Card>
              <div className="flex items-center gap-3 font-mono text-sm text-text-muted">
                <span className="h-2 w-2 animate-pulseDot rounded-full bg-accent" />
                consultando UniProt, PubMed, InterPro, AlphaFold, STRING…
              </div>
            </Card>
          )}

          {result && (
            <>
              <Card className="animate-fade-slide">
                <p className="text-xs uppercase tracking-wide text-text-muted">Sequência registrada</p>
                <div className="mt-1 flex flex-wrap items-center gap-2">
                  <Link
                    to={`/sequences/${result.sequence.id}`}
                    className="font-mono text-sm text-accent hover:underline"
                  >
                    #{result.sequence.id}
                  </Link>
                  <span className="chip">{result.sequence.sequence_type}</span>
                  {result.sequence.organism && (
                    <span className="text-xs italic text-text-muted">
                      {result.sequence.organism}
                    </span>
                  )}
                </div>
              </Card>
              {analysis ? (
                <AnalysisCards analysis={analysis} />
              ) : (
                <Empty
                  title="Sequência registrada sem análise."
                  hint="Ative “Analisar na submissão” para obter resultados multi-fonte."
                />
              )}
            </>
          )}

          {!busy && !result && !biosafetyBlock && (
            <Empty
              title="Os resultados aparecem aqui."
              hint="Preencha o formulário à esquerda e submeta uma sequência para ver biossegurança, UniProt, literatura, domínios, estrutura e interações."
              icon={<FlaskConical size={28} />}
            />
          )}
        </div>
      </div>
    </div>
  );
}

function BaseStats({ comp }: { comp: ReturnType<typeof baseComposition> }) {
  const bases = ["A", "C", "G", "T"];
  const showU = comp.counts.U > 0;
  const keys = showU ? ["A", "C", "G", "U"] : bases;
  return (
    <div className="grid grid-cols-4 gap-2">
      {keys.map((b) => (
        <div
          key={b}
          className="rounded-lg border border-border/60 bg-bg-base/40 px-2 py-1.5 text-center"
        >
          <div className="font-mono text-sm font-bold" style={{ color: baseColorVar(b) }}>
            {b}
          </div>
          <div className="font-mono text-[11px] text-text-primary">{comp.counts[b]}</div>
          <div className="font-mono text-[10px] text-text-muted">
            {comp.percents[b].toFixed(0)}%
          </div>
        </div>
      ))}
    </div>
  );
}
