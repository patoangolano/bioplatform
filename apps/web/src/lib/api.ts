// Typed fetch client for the Quackai BioLab platform REST API.
// Same-origin base path /api/v1 by default; overridable via VITE_API_BASE.

const BASE: string = (import.meta.env.VITE_API_BASE as string) || "/api/v1";
const TOKEN_KEY = "qbl_token";

export function getToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

export function setToken(token: string): void {
  try {
    localStorage.setItem(TOKEN_KEY, token);
  } catch {
    /* storage unavailable */
  }
}

export function clearToken(): void {
  try {
    localStorage.removeItem(TOKEN_KEY);
  } catch {
    /* storage unavailable */
  }
}

export class ApiError extends Error {
  status: number;
  detail: unknown;
  constructor(status: number, detail: unknown, message?: string) {
    super(message || `Erro ${status}`);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

/** Best-effort extraction of a human message from a FastAPI error body. */
export function errorMessage(err: unknown, fallback = "Algo deu errado."): string {
  if (err instanceof ApiError) {
    const d = err.detail;
    if (typeof d === "string") return d;
    if (d && typeof d === "object") {
      const obj = d as Record<string, unknown>;
      if (typeof obj.detail === "string") return obj.detail;
      if (typeof obj.message === "string") return obj.message;
      if (typeof obj.error === "string") return obj.error;
    }
    return err.message || fallback;
  }
  if (err instanceof Error) return err.message;
  return fallback;
}

type RequestOptions = {
  method?: string;
  body?: unknown;
  form?: URLSearchParams;
  auth?: boolean;
  signal?: AbortSignal;
};

async function request<T>(path: string, opts: RequestOptions = {}): Promise<T> {
  const { method = "GET", body, form, auth = true, signal } = opts;
  const headers: Record<string, string> = {};

  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  let payload: BodyInit | undefined;
  if (form) {
    headers["Content-Type"] = "application/x-www-form-urlencoded";
    payload = form.toString();
  } else if (body !== undefined) {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);
  }

  let res: Response;
  try {
    res = await fetch(`${BASE}${path}`, { method, headers, body: payload, signal });
  } catch (e) {
    if (e instanceof DOMException && e.name === "AbortError") throw e;
    throw new ApiError(0, null, "Sem conexão com o servidor. Verifique sua rede.");
  }

  if (res.status === 204) return undefined as T;

  const text = await res.text();
  let data: unknown = null;
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = text;
    }
  }

  if (!res.ok) {
    const detail =
      data && typeof data === "object" && "detail" in data
        ? (data as Record<string, unknown>).detail
        : data;
    throw new ApiError(res.status, detail);
  }

  return data as T;
}

export const api = {
  get: <T>(path: string, opts?: RequestOptions) => request<T>(path, { ...opts, method: "GET" }),
  post: <T>(path: string, body?: unknown, opts?: RequestOptions) =>
    request<T>(path, { ...opts, method: "POST", body }),
  postForm: <T>(path: string, form: URLSearchParams, opts?: RequestOptions) =>
    request<T>(path, { ...opts, method: "POST", form }),
  raw: request,
};
