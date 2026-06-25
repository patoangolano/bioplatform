import { useEffect, useRef, useState } from "react";
import clsx from "clsx";
import { api } from "../lib/api";

type Health = "ok" | "down" | "checking";

/** Polls GET /health every 20s and renders a pulsing status dot. */
export default function HealthPulse() {
  const [state, setState] = useState<Health>("checking");
  const timer = useRef<number | undefined>(undefined);

  useEffect(() => {
    let alive = true;
    const check = async () => {
      try {
        await api.get<unknown>("/health", { auth: false });
        if (alive) setState("ok");
      } catch {
        if (alive) setState("down");
      }
    };
    void check();
    timer.current = window.setInterval(check, 20_000);
    return () => {
      alive = false;
      if (timer.current) window.clearInterval(timer.current);
    };
  }, []);

  const color =
    state === "ok" ? "bg-accent" : state === "down" ? "bg-danger" : "bg-warning";
  const label =
    state === "ok" ? "API online" : state === "down" ? "API indisponível" : "verificando";

  return (
    <span
      className="inline-flex items-center gap-2 font-mono text-xs text-text-muted"
      title={label}
      role="status"
      aria-live="polite"
    >
      <span className="relative flex h-2.5 w-2.5">
        <span
          className={clsx(
            "absolute inline-flex h-full w-full rounded-full opacity-75",
            color,
            state === "ok" && "animate-pulseDot",
          )}
        />
        <span className={clsx("relative inline-flex h-2.5 w-2.5 rounded-full", color)} />
      </span>
      <span className="hidden sm:inline">{label}</span>
    </span>
  );
}
