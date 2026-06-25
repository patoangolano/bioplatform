// Domain types. Analysis sub-objects are loosely-typed dicts from the API;
// they are modeled defensively so the UI never crashes on missing fields.

export type SequenceType = "DNA" | "RNA" | "protein";

export interface UserRead {
  id: number | string;
  email: string;
  full_name?: string | null;
  is_active?: boolean;
  is_admin?: boolean;
  created_at?: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface SequenceResponse {
  id: number | string;
  description?: string | null;
  sequence_type: SequenceType;
  raw_sequence: string;
  organism?: string | null;
  created_at?: string;
}

// Loose record helper — analysis fields are unknown-shaped dicts.
export type Loose = Record<string, unknown>;

export interface AnalysisResult {
  uniprot_matches?: Loose[];
  literature?: Loose[];
  interpro_domains?: Loose[];
  alphafold_structures?: Loose[];
  string_interactions?: Loose[];
  provenance?: Loose[];
  biosafety?: Loose;
  [key: string]: unknown;
}

export interface SequenceWithAnalysis {
  sequence: SequenceResponse;
  analysis?: AnalysisResult | null;
}

export interface BiosafetyBlock {
  error?: string;
  risk_level?: string;
  flags?: string[];
  recommendation?: string;
}

export interface BlastSubmitResponse {
  job_id: string;
  status: string;
  message?: string;
}

export interface BlastJob {
  job_id: string;
  status: string;
  started_at?: string | null;
  completed_at?: string | null;
  error_message?: string | null;
  results?: unknown;
}

export interface AdminStats {
  total_users?: number;
  total_sequences?: number;
  total_jobs?: number;
  active_jobs?: number;
  completed_jobs?: number;
  failed_jobs?: number;
}

// --- defensive field accessors ---
export function str(o: Loose, ...keys: string[]): string | undefined {
  for (const k of keys) {
    const v = o[k];
    if (typeof v === "string" && v.trim()) return v;
    if (typeof v === "number") return String(v);
  }
  return undefined;
}

export function num(o: Loose, ...keys: string[]): number | undefined {
  for (const k of keys) {
    const v = o[k];
    if (typeof v === "number" && !Number.isNaN(v)) return v;
    if (typeof v === "string" && v.trim() && !Number.isNaN(Number(v))) return Number(v);
  }
  return undefined;
}

export function arr(o: Loose, ...keys: string[]): string[] {
  for (const k of keys) {
    const v = o[k];
    if (Array.isArray(v)) return v.filter((x) => typeof x === "string") as string[];
  }
  return [];
}
