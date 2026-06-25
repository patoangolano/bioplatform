import {
  Atom,
  BookOpen,
  Boxes,
  Dna,
  Network,
  ShieldCheck,
  ShieldAlert,
  ShieldX,
} from "lucide-react";
import clsx from "clsx";
import type { AnalysisResult, Loose } from "../lib/types";
import { num, str } from "../lib/types";
import { Card, CardTitle, Empty } from "./ui";
import { ProvenanceRow } from "./ProvenanceStamp";
import PlddtGauge from "./PlddtGauge";

function Reveal({ index, children }: { index: number; children: React.ReactNode }) {
  return (
    <div className="animate-fade-slide" style={{ animationDelay: `${index * 80}ms` }}>
      {children}
    </div>
  );
}

/* ---------- Biosafety panel ---------- */
function BiosafetyPanel({ bio }: { bio: Loose }) {
  const risk = (str(bio, "risk_level", "risk", "level") ?? "").toUpperCase();
  const flags = Array.isArray(bio.flags)
    ? (bio.flags as unknown[]).filter((x) => typeof x === "string")
    : [];
  const recommendation = str(bio, "recommendation", "message");

  let tone: "ok" | "warning" | "danger" = "ok";
  let title = "Biossegurança — liberado";
  let Icon = ShieldCheck;
  if (risk.includes("CRITICAL") || risk.includes("HIGH") || risk.includes("BLOCK")) {
    tone = "danger";
    title = "Biossegurança — bloqueado";
    Icon = ShieldX;
  } else if (risk.includes("MEDIUM") || risk.includes("MODER") || risk.includes("WARN") || risk.includes("ATEN")) {
    tone = "warning";
    title = "Biossegurança — atenção";
    Icon = ShieldAlert;
  }

  const toneCls = {
    ok: "border-accent/50 bg-accent/10",
    warning: "border-warning/50 bg-warning/10",
    danger: "border-danger/50 bg-danger/10",
  }[tone];
  const iconCls = { ok: "text-accent", warning: "text-warning", danger: "text-danger" }[tone];

  return (
    <div className={clsx("rounded-xl border p-5", toneCls)}>
      <div className="flex items-center gap-2.5">
        <Icon size={20} className={iconCls} aria-hidden="true" />
        <h3 className="text-base font-bold text-text-primary">{title}</h3>
        {risk && (
          <span className={clsx("ml-auto chip", iconCls)}>{risk.toLowerCase()}</span>
        )}
      </div>
      {recommendation && <p className="mt-2 text-sm text-text-primary/90">{recommendation}</p>}
      {flags.length > 0 && (
        <ul className="mt-3 flex flex-wrap gap-1.5">
          {(flags as string[]).map((f, i) => (
            <li key={i} className="chip text-text-primary">
              {f}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

/* ---------- UniProt ---------- */
function UniProtCard({ items }: { items: Loose[] }) {
  return (
    <Card>
      <CardTitle icon={<Atom size={18} />}>UniProt</CardTitle>
      {items.length === 0 ? (
        <Empty title="Sem correspondências UniProt." />
      ) : (
        <ul className="space-y-2.5">
          {items.map((m, i) => {
            const acc = str(m, "accession", "primaryAccession", "id");
            const name = str(m, "protein_name", "name", "proteinName", "description");
            const organism = str(m, "organism", "organism_name", "species");
            return (
              <li key={i} className="rounded-lg border border-border/60 bg-bg-base/40 px-3 py-2.5">
                <div className="flex flex-wrap items-center gap-2">
                  {acc && (
                    <a
                      href={`https://www.uniprot.org/uniprotkb/${acc}`}
                      target="_blank"
                      rel="noreferrer"
                      className="font-mono text-sm font-medium text-accent hover:underline"
                    >
                      {acc}
                    </a>
                  )}
                  {name && <span className="text-sm text-text-primary">{name}</span>}
                </div>
                {organism && (
                  <p className="mt-0.5 text-xs italic text-text-muted">{organism}</p>
                )}
              </li>
            );
          })}
        </ul>
      )}
    </Card>
  );
}

/* ---------- Literature ---------- */
function LiteratureCard({ items }: { items: Loose[] }) {
  return (
    <Card>
      <CardTitle icon={<BookOpen size={18} />}>Literatura (PubMed)</CardTitle>
      {items.length === 0 ? (
        <Empty title="Nenhuma referência encontrada." />
      ) : (
        <ul className="space-y-2.5">
          {items.map((lit, i) => {
            const pmid = str(lit, "pmid", "PMID", "id");
            const title = str(lit, "title", "ArticleTitle") ?? "(sem título)";
            const authors = str(lit, "authors", "author");
            const year = str(lit, "year", "pubYear", "Year");
            const journal = str(lit, "journal", "Journal", "source");
            return (
              <li key={i} className="rounded-lg border border-border/60 bg-bg-base/40 px-3 py-2.5">
                {pmid ? (
                  <a
                    href={`https://pubmed.ncbi.nlm.nih.gov/${pmid}`}
                    target="_blank"
                    rel="noreferrer"
                    className="text-sm font-medium text-text-primary hover:text-accent hover:underline"
                  >
                    {title}
                  </a>
                ) : (
                  <span className="text-sm font-medium text-text-primary">{title}</span>
                )}
                <p className="mt-0.5 truncate text-xs text-text-muted">
                  {[authors, journal, year].filter(Boolean).join(" · ")}
                  {pmid && <span className="ml-2 font-mono">PMID:{pmid}</span>}
                </p>
              </li>
            );
          })}
        </ul>
      )}
    </Card>
  );
}

/* ---------- InterPro ---------- */
function InterProCard({ items }: { items: Loose[] }) {
  return (
    <Card>
      <CardTitle icon={<Boxes size={18} />}>Domínios (InterPro)</CardTitle>
      {items.length === 0 ? (
        <Empty title="Nenhum domínio detectado." />
      ) : (
        <ul className="space-y-2">
          {items.map((d, i) => {
            const id = str(d, "id", "accession", "interpro_id");
            const name = str(d, "name", "description");
            const type = str(d, "type", "category");
            return (
              <li
                key={i}
                className="flex flex-wrap items-center gap-2 rounded-lg border border-border/60 bg-bg-base/40 px-3 py-2"
              >
                {id && <span className="font-mono text-xs text-cyan-secondary">{id}</span>}
                {name && <span className="text-sm text-text-primary">{name}</span>}
                {type && (
                  <span className="ml-auto rounded bg-bg-surface-2 px-1.5 py-0.5 text-[10px] uppercase tracking-wide text-text-muted">
                    {type}
                  </span>
                )}
              </li>
            );
          })}
        </ul>
      )}
    </Card>
  );
}

/* ---------- AlphaFold ---------- */
function AlphaFoldCard({ items }: { items: Loose[] }) {
  return (
    <Card>
      <CardTitle icon={<Dna size={18} />}>Estrutura (AlphaFold)</CardTitle>
      {items.length === 0 ? (
        <Empty title="Sem modelos estruturais." />
      ) : (
        <ul className="space-y-4">
          {items.map((s, i) => {
            const plddt = num(s, "plddt_confidence", "plddt", "confidence", "mean_plddt");
            const up = str(s, "uniprot", "uniprot_id", "uniprotAccession", "accession");
            const url = str(s, "model_url", "url", "pdbUrl", "cifUrl");
            return (
              <li key={i} className="rounded-lg border border-border/60 bg-bg-base/40 px-3 py-3">
                <div className="mb-2 flex flex-wrap items-center gap-2">
                  {up && <span className="font-mono text-xs text-accent">{up}</span>}
                  {url && (
                    <a
                      href={url}
                      target="_blank"
                      rel="noreferrer"
                      className="ml-auto text-xs text-cyan-secondary hover:underline"
                    >
                      modelo →
                    </a>
                  )}
                </div>
                {typeof plddt === "number" ? (
                  <PlddtGauge value={plddt} />
                ) : (
                  <p className="text-xs text-text-muted">pLDDT indisponível.</p>
                )}
              </li>
            );
          })}
        </ul>
      )}
    </Card>
  );
}

/* ---------- STRING ---------- */
function StringCard({ items }: { items: Loose[] }) {
  const scored = items.map((it) => ({
    partner: str(it, "partner", "name", "preferredName", "target") ?? "?",
    score: num(it, "score", "combined_score", "weight") ?? 0,
  }));
  const max = Math.max(1, ...scored.map((s) => (s.score > 1 ? s.score / 1000 : s.score)));
  return (
    <Card>
      <CardTitle icon={<Network size={18} />}>Interações (STRING)</CardTitle>
      {scored.length === 0 ? (
        <Empty title="Nenhuma interação prevista." />
      ) : (
        <ul className="space-y-2">
          {scored
            .sort((a, b) => b.score - a.score)
            .map((s, i) => {
              const norm = s.score > 1 ? s.score / 1000 : s.score;
              return (
                <li key={i} className="flex items-center gap-3">
                  <span className="w-28 shrink-0 truncate font-mono text-xs text-text-primary">
                    {s.partner}
                  </span>
                  <div className="h-2 flex-1 overflow-hidden rounded-full bg-bg-base">
                    <div
                      className="h-full rounded-full bg-accent/80"
                      style={{ width: `${Math.min(100, (norm / max) * 100)}%` }}
                    />
                  </div>
                  <span className="w-12 shrink-0 text-right font-mono text-xs text-text-muted">
                    {norm.toFixed(2)}
                  </span>
                </li>
              );
            })}
        </ul>
      )}
    </Card>
  );
}

function asLooseArray(v: unknown): Loose[] {
  return Array.isArray(v) ? (v.filter((x) => x && typeof x === "object") as Loose[]) : [];
}

export default function AnalysisCards({ analysis }: { analysis: AnalysisResult }) {
  const uniprot = asLooseArray(analysis.uniprot_matches);
  const literature = asLooseArray(analysis.literature);
  const interpro = asLooseArray(analysis.interpro_domains);
  const alphafold = asLooseArray(analysis.alphafold_structures);
  const stringI = asLooseArray(analysis.string_interactions);
  const provenance = asLooseArray(analysis.provenance);
  const bio = analysis.biosafety && typeof analysis.biosafety === "object" ? analysis.biosafety : null;

  let idx = 0;
  return (
    <div className="space-y-4">
      {bio && (
        <Reveal index={idx++}>
          <BiosafetyPanel bio={bio} />
        </Reveal>
      )}
      <Reveal index={idx++}>
        <div>
          <UniProtCard items={uniprot} />
          <ProvenanceRow items={provenance} />
        </div>
      </Reveal>
      <Reveal index={idx++}>
        <LiteratureCard items={literature} />
      </Reveal>
      <Reveal index={idx++}>
        <InterProCard items={interpro} />
      </Reveal>
      <Reveal index={idx++}>
        <AlphaFoldCard items={alphafold} />
      </Reveal>
      <Reveal index={idx++}>
        <StringCard items={stringI} />
      </Reveal>
    </div>
  );
}
