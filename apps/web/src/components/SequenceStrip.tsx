import { useMemo } from "react";
import clsx from "clsx";
import { baseColorVar, pseudoSequence } from "../lib/seq";

interface SequenceStripProps {
  /** Nucleotide string; if omitted a deterministic ACGT string is generated. */
  sequence?: string;
  /** Max chars rendered before truncation (responsive default). */
  max?: number;
  className?: string;
  /** Enable the left→right scanner highlight (disabled under reduced motion via CSS). */
  scanner?: boolean;
  seed?: number;
}

/**
 * Renders a nucleotide string in JetBrains Mono with per-base coloring and an
 * optional scanner highlight. The mono motif is the product's signature.
 */
export default function SequenceStrip({
  sequence,
  max = 160,
  className,
  scanner = true,
  seed = 7,
}: SequenceStripProps) {
  const display = useMemo(() => {
    const raw = (sequence ?? pseudoSequence(Math.min(max, 200), seed)).replace(/\s+/g, "");
    return raw.length > max ? raw.slice(0, max) : raw;
  }, [sequence, max, seed]);

  const truncated = (sequence ?? "").replace(/\s+/g, "").length > max;

  return (
    <div
      aria-hidden="true"
      className={clsx(
        "select-none overflow-hidden whitespace-nowrap rounded-lg border border-border/70 bg-bg-base/60 px-3 py-2 font-mono text-[13px] leading-none tracking-[0.12em]",
        scanner && "scanner-track",
        className,
      )}
    >
      {display.split("").map((ch, i) => (
        <span key={i} style={{ color: baseColorVar(ch) }}>
          {ch}
        </span>
      ))}
      {truncated && <span className="text-text-muted">…</span>}
    </div>
  );
}
