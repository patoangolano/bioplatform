import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { Navigate, useLocation } from "react-router-dom";
import { api, clearToken, getToken, setToken } from "./api";
import type { TokenResponse, UserRead } from "./types";

interface AuthState {
  user: UserRead | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName?: string) => Promise<void>;
  logout: () => void;
  refresh: () => Promise<void>;
}

const AuthContext = createContext<AuthState | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserRead | null>(null);
  const [loading, setLoading] = useState(true);

  const loadMe = useCallback(async () => {
    if (!getToken()) {
      setUser(null);
      setLoading(false);
      return;
    }
    try {
      const me = await api.get<UserRead>("/auth/me");
      setUser(me);
    } catch {
      clearToken();
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadMe();
  }, [loadMe]);

  const login = useCallback(
    async (email: string, password: string) => {
      const form = new URLSearchParams();
      form.set("username", email);
      form.set("password", password);
      const tok = await api.postForm<TokenResponse>("/auth/login", form, { auth: false });
      setToken(tok.access_token);
      const me = await api.get<UserRead>("/auth/me");
      setUser(me);
    },
    [],
  );

  const register = useCallback(
    async (email: string, password: string, fullName?: string) => {
      await api.post<UserRead>(
        "/auth/register",
        { email, password, ...(fullName ? { full_name: fullName } : {}) },
        { auth: false },
      );
      await login(email, password);
    },
    [login],
  );

  const logout = useCallback(() => {
    clearToken();
    setUser(null);
  }, []);

  const value = useMemo<AuthState>(
    () => ({ user, loading, login, register, logout, refresh: loadMe }),
    [user, loading, login, register, logout, loadMe],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth precisa estar dentro de AuthProvider");
  return ctx;
}

export function ProtectedRoute({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-bg-base">
        <div className="flex items-center gap-3 font-mono text-sm text-text-muted">
          <span className="h-2 w-2 animate-pulseDot rounded-full bg-accent" />
          carregando sessão…
        </div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  return <>{children}</>;
}
