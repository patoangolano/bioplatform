// AlphaFold pLDDT confidence gauge with 4 standard bands, themed to dark.
function band(plddt: number): { label: string; color: string } {
  if (plddt >= 90) return { label: "muito alta", color: "var(--cyan)" };
  if (plddt >= 70) return { label: "alta", color: "var(--accent)" };
  if (plddt >= 50) return { label: "baixa", color: "var(--warning)" };
  return { label: "muito baixa", color: "var(--danger)" };
}

export default function PlddtGauge({ value }: { value: number }) {
  const v = Math.max(0, Math.min(100, value));
  const { label, color } = band(v);
  return (
    <div>
      <div className="mb-1 flex items-baseline justify-between">
        <span className="font-mono text-sm text-text-primary">
          pLDDT <span className="font-bold" style={{ color }}>{v.toFixed(1)}</span>
        </span>
        <span className="text-xs text-text-muted">confiança {label}</span>
      </div>
      <div
        className="relative h-2.5 w-full overflow-hidden rounded-full bg-bg-base"
        role="meter"
        aria-valuenow={v}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={`pLDDT ${v.toFixed(1)} — confiança ${label}`}
      >
        <div
          className="h-full rounded-full transition-all"
          style={{ width: `${v}%`, backgroundColor: color }}
        />
      </div>
      <div className="mt-1 flex justify-between font-mono text-[10px] text-text-muted/70">
        <span>0</span>
        <span>50</span>
        <span>70</span>
        <span>90</span>
        <span>100</span>
      </div>
    </div>
  );
}
