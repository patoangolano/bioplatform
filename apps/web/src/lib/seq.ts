// Sequence helpers: deterministic pseudo-random ACGT and base composition.

const BASES = ["A", "C", "G", "T"] as const;

/** Deterministic ACGT string from a numeric seed (mulberry32). */
export function pseudoSequence(length = 96, seed = 1337): string {
  let t = seed >>> 0;
  let out = "";
  for (let i = 0; i < length; i++) {
    t += 0x6d2b79f5;
    let r = Math.imul(t ^ (t >>> 15), 1 | t);
    r ^= r + Math.imul(r ^ (r >>> 7), 61 | r);
    const v = ((r ^ (r >>> 14)) >>> 0) / 4294967296;
    out += BASES[Math.floor(v * 4)];
  }
  return out;
}

export interface BaseComposition {
  counts: Record<string, number>;
  total: number;
  percents: Record<string, number>;
}

/** Count A/C/G/T/U (case-insensitive); "other" bucket for anything else. */
export function baseComposition(seq: string): BaseComposition {
  const counts: Record<string, number> = { A: 0, C: 0, G: 0, T: 0, U: 0, other: 0 };
  for (const ch of seq.toUpperCase()) {
    if (ch in counts && ch !== "other") counts[ch] += 1;
    else if (/[A-Z]/.test(ch)) counts.other += 1;
  }
  const total = seq.replace(/\s/g, "").length || 0;
  const percents: Record<string, number> = {};
  for (const k of Object.keys(counts)) {
    percents[k] = total > 0 ? (counts[k] / total) * 100 : 0;
  }
  return { counts, total, percents };
}

export function baseColorVar(base: string): string {
  switch (base.toUpperCase()) {
    case "A":
      return "var(--base-a)";
    case "C":
      return "var(--base-c)";
    case "G":
      return "var(--base-g)";
    case "T":
    case "U":
      return "var(--base-t)";
    default:
      return "var(--text-muted)";
  }
}
