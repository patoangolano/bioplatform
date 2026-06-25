import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center text-center">
      <p className="font-mono text-5xl font-bold text-accent">404</p>
      <h1 className="mt-3 text-xl font-bold">Página não encontrada</h1>
      <p className="mt-1 text-text-muted">A rota que você tentou abrir não existe.</p>
      <Link to="/" className="btn-primary mt-5">
        Voltar ao painel
      </Link>
    </div>
  );
}
