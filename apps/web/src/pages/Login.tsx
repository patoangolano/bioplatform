import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../lib/auth";
import { errorMessage } from "../lib/api";
import SequenceStrip from "../components/SequenceStrip";
import Logo from "../components/Logo";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      await login(email, password);
      navigate("/");
    } catch (err) {
      setError(errorMessage(err, "Não foi possível entrar. Verifique e-mail e senha."));
    } finally {
      setBusy(false);
    }
  };

  return (
    <AuthLayout subtitle="Entre para submeter sequências e executar análises multi-fonte.">
      <form onSubmit={onSubmit} className="space-y-4" noValidate>
        <div>
          <label className="label" htmlFor="email">
            E-mail
          </label>
          <input
            id="email"
            type="email"
            autoComplete="email"
            required
            className="input"
            placeholder="voce@laboratorio.org"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label className="label" htmlFor="password">
            Senha
          </label>
          <input
            id="password"
            type="password"
            autoComplete="current-password"
            required
            className="input"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {error && (
          <p className="rounded-lg border border-danger/40 bg-danger/10 px-3 py-2 text-sm text-danger">
            {error}
          </p>
        )}
        <button type="submit" disabled={busy} className="btn-primary w-full shadow-glow">
          {busy ? "Entrando…" : "Entrar"}
        </button>
      </form>
      <p className="mt-5 text-center text-sm text-text-muted">
        Ainda não tem conta?{" "}
        <Link to="/register" className="font-medium text-accent hover:underline">
          Criar conta
        </Link>
      </p>
    </AuthLayout>
  );
}

export function AuthLayout({
  children,
  subtitle,
}: {
  children: React.ReactNode;
  subtitle: string;
}) {
  return (
    <div className="flex min-h-screen items-center justify-center px-4 py-10">
      <div className="w-full max-w-md">
        <div className="mb-6 flex flex-col items-center text-center">
          <Logo size={44} />
          <h1 className="mt-3 font-display text-2xl font-extrabold tracking-tight">
            Quackai <span className="text-accent">BioLab</span>
          </h1>
          <p className="mt-1 max-w-sm text-sm text-text-muted">{subtitle}</p>
        </div>
        <SequenceStrip className="mb-6" max={48} seed={42} />
        <div className="card p-6">{children}</div>
      </div>
    </div>
  );
}
