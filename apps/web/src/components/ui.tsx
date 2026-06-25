import clsx from "clsx";
import type { ReactNode } from "react";

export function Card({
  children,
  className,
  style,
}: {
  children: ReactNode;
  className?: string;
  style?: React.CSSProperties;
}) {
  return (
    <div className={clsx("card p-5", className)} style={style}>
      {children}
    </div>
  );
}

export function CardTitle({
  icon,
  children,
  badge,
}: {
  icon?: ReactNode;
  children: ReactNode;
  badge?: ReactNode;
}) {
  return (
    <div className="mb-4 flex items-center gap-2.5">
      {icon && <span className="text-accent">{icon}</span>}
      <h3 className="text-base font-bold text-text-primary">{children}</h3>
      {badge && <span className="ml-auto">{badge}</span>}
    </div>
  );
}

export function Mono({ children, className }: { children: ReactNode; className?: string }) {
  return <span className={clsx("font-mono", className)}>{children}</span>;
}

export function Empty({
  title,
  hint,
  icon,
}: {
  title: string;
  hint?: string;
  icon?: ReactNode;
}) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-border bg-bg-base/40 px-6 py-12 text-center">
      {icon && <div className="mb-3 text-text-muted/70">{icon}</div>}
      <p className="font-medium text-text-primary">{title}</p>
      {hint && <p className="mt-1 max-w-sm text-sm text-text-muted">{hint}</p>}
    </div>
  );
}

export function Banner({
  tone = "danger",
  title,
  children,
}: {
  tone?: "danger" | "warning" | "ok";
  title: string;
  children?: ReactNode;
}) {
  const toneMap = {
    danger: "border-danger/50 bg-danger/10 text-danger",
    warning: "border-warning/50 bg-warning/10 text-warning",
    ok: "border-accent/50 bg-accent/10 text-accent",
  } as const;
  return (
    <div className={clsx("rounded-xl border p-4", toneMap[tone])}>
      <p className="font-semibold">{title}</p>
      {children && <div className="mt-1 text-sm text-text-primary/90">{children}</div>}
    </div>
  );
}

export function Skeleton({ className }: { className?: string }) {
  return <div className={clsx("animate-pulse rounded-lg bg-bg-surface-2/70", className)} />;
}
