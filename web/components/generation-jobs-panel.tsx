"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { JsonViewer } from "./json-viewer";
import { ApiClientError, getJson, postJson } from "../lib/api-client";

type JobCreateResponse = {
  job_id: string;
  status: "pending" | "running" | "completed" | "failed";
  total_items: number;
  message: string;
};

type JobStatusResponse = {
  id: string;
  status: "pending" | "running" | "completed" | "failed";
  total_items: number;
  completed_items: number;
  failed_items: number;
  error_message?: string | null;
  results: Array<{
    index: number;
    sku?: string | null;
    status: "completed" | "failed";
    product_id?: string | null;
    error?: string | null;
  }>;
};

function buildSampleBatchPayload() {
  return {
    items: [
      {
        sku: `CAM-JOB-WEB-1`,
        nome_produto: "Camisa Oxford Batch",
        descricao_bruta: "Camisa social em algodao com toque macio.",
        marca: "Lumen",
        categoria: "camisa",
        subcategoria: "social",
        tamanhos: ["P", "M", "G"],
        cores: ["Azul Marinho", "Branco"],
        composicao: "100% algodao",
        tecido: "oxford",
        modelagem: "regular",
        acabamento: "costuras reforcadas",
        colecao: "essenciais",
        preco: 299.9,
        promocao: null,
        imagens: [],
        guidelines_marca: { termos_proibidos: [] },
        regras_categoria: { tamanhos_validos: [], cores_validas: [] },
        restricoes_legais: { claims_proibidos: [] },
        usuario: "demo-web",
        versao_pipeline: "1.0.0",
      },
    ],
  };
}

type GenerationJobsPanelProps = {
  onJobCompleted?: (payload: { jobId: string; productIds: string[] }) => void;
};

export function GenerationJobsPanel({ onJobCompleted }: GenerationJobsPanelProps) {
  const [autoPollingEnabled, setAutoPollingEnabled] = useState(true);
  const [statusJsonCollapsed, setStatusJsonCollapsed] = useState(true);
  const [payloadText, setPayloadText] = useState(() =>
    JSON.stringify(buildSampleBatchPayload(), null, 2),
  );
  const [createStatus, setCreateStatus] = useState<number | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<JobStatusResponse | null>(null);
  const [loadingCreate, setLoadingCreate] = useState(false);
  const [loadingPoll, setLoadingPoll] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copyFeedback, setCopyFeedback] = useState<string | null>(null);
  const [batchCount, setBatchCount] = useState(3);
  const timerRef = useRef<number | null>(null);

  const shouldPoll = useMemo(
    () =>
      autoPollingEnabled &&
      !!jobStatus &&
      (jobStatus.status === "pending" || jobStatus.status === "running"),
    [autoPollingEnabled, jobStatus],
  );

  useEffect(() => {
    try {
      const savedAutoPolling = window.localStorage.getItem("wave2.jobs.autoPollingEnabled");
      const savedStatusCollapsed = window.localStorage.getItem("wave2.jobs.statusJsonCollapsed");
      if (savedAutoPolling !== null) {
        setAutoPollingEnabled(savedAutoPolling === "true");
      }
      if (savedStatusCollapsed !== null) {
        setStatusJsonCollapsed(savedStatusCollapsed === "true");
      }
    } catch {
      // localStorage may be unavailable in some environments; ignore.
    }
  }, []);

  useEffect(() => {
    try {
      window.localStorage.setItem("wave2.jobs.autoPollingEnabled", String(autoPollingEnabled));
    } catch {}
  }, [autoPollingEnabled]);

  useEffect(() => {
    try {
      window.localStorage.setItem("wave2.jobs.statusJsonCollapsed", String(statusJsonCollapsed));
    } catch {}
  }, [statusJsonCollapsed]);

  async function createJob() {
    setLoadingCreate(true);
    setError(null);
    setCreateStatus(null);
    setJobStatus(null);

    try {
      const parsed = JSON.parse(payloadText);
      const create = await postJson<unknown, JobCreateResponse>("/api/generation-jobs", parsed);
      setCreateStatus(202);
      setJobId(create.job_id);
    } catch (submitError) {
      if (submitError instanceof ApiClientError) {
        setCreateStatus(submitError.status);
        setError(submitError.message);
      } else {
        setError(submitError instanceof Error ? submitError.message : "Erro inesperado.");
      }
    } finally {
      setLoadingCreate(false);
    }
  }

  function generateBatchFromBase() {
    try {
      const parsed = JSON.parse(payloadText) as { items?: Array<Record<string, unknown>> };
      const base = parsed.items?.[0];
      if (!base || typeof base !== "object") {
        setError("Payload base invalido para gerar lote.");
        return;
      }

      const requestedCount = Math.min(20, Math.max(1, Number(batchCount) || 1));
      const nextItems = Array.from({ length: requestedCount }, (_, index) => {
        const cloned = structuredClone(base);
        const baseSku = typeof cloned.sku === "string" ? cloned.sku : "ITEM";
        cloned.sku = `${baseSku.replace(/-\\d+$/, "")}-${String(index + 1).padStart(2, "0")}`;
        if (typeof cloned.nome_produto === "string") {
          cloned.nome_produto = `${cloned.nome_produto} #${index + 1}`;
        }
        return cloned;
      });

      setPayloadText(JSON.stringify({ items: nextItems }, null, 2));
      setError(null);
    } catch {
      setError("JSON invalido no payload. Corrija antes de gerar lote.");
    }
  }

  async function copyToClipboard(label: string, value: string) {
    try {
      await navigator.clipboard.writeText(value);
      setCopyFeedback(`${label} copiado.`);
      window.setTimeout(() => setCopyFeedback(null), 1500);
    } catch {
      setCopyFeedback(`Falha ao copiar ${label}.`);
      window.setTimeout(() => setCopyFeedback(null), 1500);
    }
  }

  const pollJob = useCallback(async (currentJobId: string) => {
    setLoadingPoll(true);
    try {
      const parsed = await getJson<JobStatusResponse>(`/api/generation-jobs/${currentJobId}`);
      setJobStatus(parsed);
      if (parsed.status === "completed") {
        const productIds = parsed.results
          .map((item) => item.product_id)
          .filter((id): id is string => typeof id === "string" && id.length > 0);
        onJobCompleted?.({ jobId: parsed.id, productIds });
      }
    } catch (pollError) {
      if (pollError instanceof ApiClientError) {
        setError(pollError.message);
      } else {
        setError(pollError instanceof Error ? pollError.message : "Erro inesperado no polling.");
      }
    } finally {
      setLoadingPoll(false);
    }
  }, [onJobCompleted]);

  useEffect(() => {
    if (!jobId) return;
    void pollJob(jobId);
  }, [jobId, pollJob]);

  useEffect(() => {
    if (!jobId || !shouldPoll) return;
    timerRef.current = window.setTimeout(() => {
      void pollJob(jobId);
    }, 800);
    return () => {
      if (timerRef.current) window.clearTimeout(timerRef.current);
    };
  }, [jobId, pollJob, shouldPoll, jobStatus?.completed_items, jobStatus?.failed_items]);

  return (
    <section className="panel">
      <div className="section-head">
        <h2>Generation Jobs (criacao + polling)</h2>
        <p>
          Painel inicial para `POST /api/v1/generation-jobs` e acompanhamento de status por polling.
        </p>
      </div>

      <div className="form-actions">
        <button type="button" onClick={createJob} disabled={loadingCreate}>
          {loadingCreate ? "Criando job..." : "Criar generation-job"}
        </button>
        <button
          type="button"
          onClick={() => void (jobId ? pollJob(jobId) : Promise.resolve())}
          disabled={!jobId || loadingPoll}
        >
          {loadingPoll ? "Consultando..." : "Atualizar status"}
        </button>
        {createStatus !== null ? <span>Status create: {createStatus}</span> : null}
        {jobId ? (
          <span className="inline-copy">
            Job ID: <code>{jobId}</code>
            <button
              type="button"
              className="copy-inline-button"
              onClick={() => void copyToClipboard("Job ID", jobId)}
            >
              Copiar
            </button>
          </span>
        ) : null}
        {jobStatus ? (
          <span className="inline-status">
            <span className={`pulse-dot ${shouldPoll || loadingPoll ? "is-active" : ""}`} />
            Status atual: <strong>{jobStatus.status}</strong>
            {shouldPoll ? " (polling ativo)" : ""}
          </span>
        ) : null}
        {copyFeedback ? <span className="ok">{copyFeedback}</span> : null}
        {error ? <span className="warn">{error}</span> : null}
      </div>

      <div className="jobs-preferences">
        <label className="toggle-inline">
          <input
            type="checkbox"
            checked={autoPollingEnabled}
            onChange={(e) => setAutoPollingEnabled(e.target.checked)}
          />
          Polling automatico
        </label>
        <label className="toggle-inline">
          <input
            type="checkbox"
            checked={statusJsonCollapsed}
            onChange={(e) => setStatusJsonCollapsed(e.target.checked)}
          />
          Status JSON inicia colapsado
        </label>
      </div>

      {!jobId ? (
        <div className="empty-guidance">
          <strong>Nenhum generation-job iniciado.</strong>
          <p>Revise o payload e execute o primeiro job para acompanhar o processamento em lote.</p>
          <div className="empty-guidance-actions">
            <button type="button" onClick={() => setPayloadText(JSON.stringify(buildSampleBatchPayload(), null, 2))}>
              Restaurar payload base
            </button>
            <button type="button" onClick={createJob} disabled={loadingCreate}>
              {loadingCreate ? "Criando..." : "Criar primeiro job"}
            </button>
          </div>
        </div>
      ) : null}

      <div className="batch-helper">
        <strong>Helper de lote</strong>
        <label>
          Quantidade (1-20)
          <input
            type="number"
            min="1"
            max="20"
            value={batchCount}
            onChange={(e) => setBatchCount(Math.min(20, Math.max(1, Number(e.target.value) || 1)))}
          />
        </label>
        <button type="button" className="table-inline-button" onClick={generateBatchFromBase}>
          Gerar lote a partir do 1o item
        </button>
        <span className="muted-inline">
          Duplica o item base e incrementa `sku` / sufixo no nome.
        </span>
      </div>

      <div className="two-col">
        <div>
          <h3>Payload do job (JSON)</h3>
          <textarea
            className="json-textarea"
            rows={18}
            value={payloadText}
            onChange={(e) => setPayloadText(e.target.value)}
          />
        </div>
        <div>
          <JsonViewer
            title="Status do job"
            value={jobStatus ?? { info: "Nenhum job consultado" }}
            initiallyCollapsed={statusJsonCollapsed}
          />
        </div>
      </div>

      {jobStatus ? (
        <div className="job-results-summary">
          <div className="section-head">
            <h3>Resumo dos resultados do job</h3>
            <p>
              Itens processados ({jobStatus.completed_items} concluidos / {jobStatus.failed_items}{" "}
              falhos).
            </p>
          </div>

          {jobStatus.results.length === 0 ? (
            <p className="muted-inline">Sem resultados ainda (job em andamento ou sem itens).</p>
          ) : (
            <div className="table-wrap">
              <table className="products-table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>SKU</th>
                    <th>Status</th>
                    <th>Product ID</th>
                    <th>Erro</th>
                  </tr>
                </thead>
                <tbody>
                  {jobStatus.results.map((result) => (
                    <tr key={`${result.index}-${result.sku ?? "no-sku"}`}>
                      <td>{result.index}</td>
                      <td>{result.sku ?? "-"}</td>
                      <td>
                        <span
                          className={`badge ${
                            result.status === "completed" ? "badge-ok" : "badge-danger"
                          }`}
                        >
                          {result.status}
                        </span>
                      </td>
                      <td>
                        {result.product_id ? (
                          <span className="inline-copy">
                            <code>{result.product_id}</code>
                            <button
                              type="button"
                              className="copy-inline-button"
                              onClick={() => void copyToClipboard("Product ID", result.product_id!)}
                            >
                              Copiar
                            </button>
                          </span>
                        ) : (
                          "-"
                        )}
                      </td>
                      <td className="job-error-cell">{result.error ?? "-"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      ) : null}
    </section>
  );
}
