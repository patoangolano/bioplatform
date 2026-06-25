import clsx from "clsx";
import { str, type Loose } from "../lib/types";

type Classification = "observation" | "inference" | "hypothesis";

const DOT: Record<Classification, string> = {
  observation: "var(--prov-observation)",
  inference: "var(--prov-inference)",
  hypothesis: "var(--prov-hypothesis)",
};

const LABEL: Record<Classification, string> = {
  observation: "observação",
  inference: "inferência",
  hypothesis: "hipótese",
};

function normClass(v: string | undefined): Classification {
  const s = (v ?? "").toLowerCase();
  if (s.startsWith("obs")) return "observation";
  if (s.startsWith("hyp") || s.startsWith("hip")) return "hypothesis";
  return "inference";
}

/**
 * Small mono chip materializing "proveniência obrigatória":
 * source tool + classification dot + truncated input hash.
 */
export default function ProvenanceStamp({
  item,
  className,
}: {
  item: Loose;
  className?: string;
}) {
  const tool = str(item, "source_tool", "tool", "name") ?? "desconhecido";
  const cls = normClass(str(item, "classification", "class", "type"));
  const hash = str(item, "input_hash", "hash", "digest");
  const ts = str(item, "timestamp", "created_at", "time");

  return (
    <span
      className={clsx(
        "chip max-w-full",
        className,
      )}
      title={
        `ferramenta: ${tool}\nclassificação: ${LABEL[cls]}` +
        (hash ? `\nhash: ${hash}` : "") +
        (ts ? `\ntimestamp: ${ts}` : "")
      }
    >
      <span
        className="h-2 w-2 shrink-0 rounded-full"
        style={{ backgroundColor: DOT[cls] }}
        aria-hidden="true"
      />
      <span className="truncate text-text-primary">{tool}</span>
      {hash && (
        <span className="truncate text-text-muted">
          {hash.length > 12 ? `${hash.slice(0, 12)}…` : hash}
        </span>
      )}
    </span>
  );
}

export function ProvenanceRow({ items }: { items?: Loose[] }) {
  if (!items || items.length === 0) return null;
  return (
    <div className="mt-3 flex flex-wrap gap-1.5 border-t border-border/60 pt-3">
      <span className="mr-1 self-center text-[11px] uppercase tracking-wide text-text-muted/70">
        proveniência
      </span>
      {items.map((p, i) => (
        <ProvenanceStamp key={i} item={p} />
      ))}
    </div>
  );
}
