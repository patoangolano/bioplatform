-- Migration: 001_initial_schema
-- Description: Schema inicial da bioplatform
-- Date: 2026-06-21

BEGIN;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Sequences submetidas para análise
CREATE TABLE sequences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    raw_sequence TEXT NOT NULL,
    sequence_type VARCHAR(10) NOT NULL CHECK (sequence_type IN ('DNA', 'RNA', 'protein')),
    description TEXT,
    organism VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Jobs de análise
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sequence_id UUID REFERENCES sequences(id),
    job_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    parameters JSONB NOT NULL DEFAULT '{}',
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    error_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Resultados de análises
CREATE TABLE results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES jobs(id),
    result_type VARCHAR(50) NOT NULL,
    data JSONB NOT NULL,
    confidence FLOAT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Registros de proveniência
CREATE TABLE provenance_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    result_id UUID REFERENCES results(id),
    source_tool VARCHAR(100) NOT NULL,
    tool_version VARCHAR(50),
    parameters JSONB NOT NULL DEFAULT '{}',
    input_hash VARCHAR(64) NOT NULL,
    output_hash VARCHAR(64) NOT NULL,
    classification VARCHAR(20) NOT NULL CHECK (classification IN ('observation', 'inference', 'hypothesis')),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_sequence_id ON jobs(sequence_id);
CREATE INDEX idx_results_job_id ON results(job_id);
CREATE INDEX idx_provenance_result_id ON provenance_records(result_id);
CREATE INDEX idx_sequences_type ON sequences(sequence_type);

COMMIT;
