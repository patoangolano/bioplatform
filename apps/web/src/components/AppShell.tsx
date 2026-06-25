import { useState } from "react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import clsx from "clsx";
import {
  LayoutDashboard,
  FlaskConical,
  Dna,
  Search,
  ShieldCheck,
  LogOut,
  Menu,
  X,
} from "lucide-react";
import { useAuth } from "../lib/auth";
import HealthPulse from "./HealthPulse";
import Logo from "./Logo";

const NAV = [
  { to: "/", label: "Painel", icon: LayoutDashboard, end: true },
  { to: "/submit", label: "Submeter", icon: FlaskConical, end: false },
  { to: "/sequences", label: "Sequências", icon: Dna, end: false },
  { to: "/blast", label: "BLAST", icon: Search, end: false },
  { to: "/admin", label: "Admin", icon: ShieldCheck, end: false },
];

function NavItems({ onNavigate }: { onNavigate?: () => void }) {
  return (
    <nav className="flex flex-col gap-1" aria-label="Navegação principal">
      {NAV.map(({ to, label, icon: Icon, end }) => (
        <NavLink
          key={to}
          to={to}
          end={end}
          onClick={onNavigate}
          className={({ isActive }) =>
            clsx(
              "group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors",
              isActive
                ? "bg-accent/10 text-accent shadow-glow-sm"
                : "text-text-muted hover:bg-bg-surface-2/60 hover:text-text-primary",
            )
          }
        >
          <Icon size={18} strokeWidth={2} aria-hidden="true" />
          {label}
        </NavLink>
      ))}
    </nav>
  );
}

function Brand() {
  return (
    <div className="flex items-center gap-2.5">
      <Logo />
      <div className="leading-tight">
        <p className="font-display text-[15px] font-extrabold tracking-tight text-text-primary">
          Quackai <span className="text-accent">BioLab</span>
        </p>
        <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-text-muted">
          translational ops
        </p>
      </div>
    </div>
  );
}

export default function AppShell() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [drawer, setDrawer] = useState(false);

  const onLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen md:flex">
      {/* Desktop sidebar */}
      <aside className="sticky top-0 hidden h-screen w-64 shrink-0 flex-col border-r border-border bg-bg-surface/60 p-4 backdrop-blur-sm md:flex">
        <div className="mb-7 px-1">
          <Brand />
        </div>
        <NavItems />
        <div className="mt-auto rounded-xl border border-border bg-bg-base/50 p-3">
          <p className="truncate font-mono text-xs text-text-muted" title={user?.email}>
            {user?.email}
          </p>
          {user?.is_admin && (
            <span className="mt-1 inline-block rounded bg-accent/15 px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wide text-accent">
              admin
            </span>
          )}
        </div>
      </aside>

      {/* Mobile drawer */}
      {drawer && (
        <div className="fixed inset-0 z-40 md:hidden" role="dialog" aria-modal="true">
          <div
            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
            onClick={() => setDrawer(false)}
          />
          <div className="absolute left-0 top-0 h-full w-72 border-r border-border bg-bg-surface p-4">
            <div className="mb-7 flex items-center justify-between">
              <Brand />
              <button
                className="btn-ghost p-2"
                onClick={() => setDrawer(false)}
                aria-label="Fechar menu"
              >
                <X size={18} />
              </button>
            </div>
            <NavItems onNavigate={() => setDrawer(false)} />
          </div>
        </div>
      )}

      <div className="flex min-w-0 flex-1 flex-col">
        {/* Topbar */}
        <header className="sticky top-0 z-30 flex h-14 items-center gap-3 border-b border-border bg-bg-base/80 px-4 backdrop-blur-md">
          <button
            className="btn-ghost p-2 md:hidden"
            onClick={() => setDrawer(true)}
            aria-label="Abrir menu"
          >
            <Menu size={18} />
          </button>
          <div className="md:hidden">
            <Brand />
          </div>
          <div className="ml-auto flex items-center gap-4">
            <HealthPulse />
            <span
              className="hidden max-w-[180px] truncate font-mono text-xs text-text-muted sm:inline"
              title={user?.email}
            >
              {user?.email}
            </span>
            <button onClick={onLogout} className="btn-ghost px-3 py-1.5 text-sm" aria-label="Sair">
              <LogOut size={16} aria-hidden="true" />
              <span className="hidden sm:inline">Sair</span>
            </button>
          </div>
        </header>

        <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-6 sm:px-6 lg:py-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
