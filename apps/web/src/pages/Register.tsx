import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../lib/auth";
import { errorMessage } from "../lib/api";
import { AuthLayout } from "./Login";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    if (password.length < 8) {
      setError("A senha precisa ter ao menos 8 caracteres.");
      return;
    }
    setBusy(true);
    try {
      await register(email, password, fullName || undefined);
      navigate("/");
    } catch (err) {
      setError(errorMessage(err, "Não foi possível criar a conta."));
    } finally {
      setBusy(false);
    }
  };

  return (
    <AuthLayout subtitle="Crie sua conta para começar a analisar sequências.">
      <form onSubmit={onSubmit} className="space-y-4" noValidate>
        <div>
          <label className="label" htmlFor="fullName">
            Nome completo <span className="text-text-muted/60">(opcional)</span>
          </label>
          <input
            id="fullName"
            type="text"
            autoComplete="name"
            className="input"
            placeholder="Ada Lovelace"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
          />
        </div>
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
            Senha <span className="text-text-muted/60">(mín. 8 caracteres)</span>
          </label>
          <input
            id="password"
            type="password"
            autoComplete="new-password"
            required
            minLength={8}
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
          {busy ? "Criando conta…" : "Criar conta"}
        </button>
      </form>
      <p className="mt-5 text-center text-sm text-text-muted">
        Já tem conta?{" "}
        <Link to="/login" className="font-medium text-accent hover:underline">
          Entrar
        </Link>
      </p>
    </AuthLayout>
  );
}
