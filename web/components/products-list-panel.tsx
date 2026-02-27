"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useCallback, useEffect, useMemo, useState } from "react";
import { JsonViewer } from "./json-viewer";
import { ApiClientError, getJson } from "../lib/api-client";

type ProductRow = {
  id: string;
  sku: string;
  nome_produto: string;
  marca: string;
  status: string;
  score_qualidade: number | null;
  created_at: string;
};

type ProductsResponse = {
  items: ProductRow[];
  pagination: {
    total: number;
    limit: number;
    offset: number;
  };
};

type ProductDetail = {
  id: string;
  sku: string;
  nome_produto: string;
  marca: string;
  status: string;
  score_qualidade: number | null;
  tenant_id?: string | null;
  generation_job_id?: string | null;
  input_payload: Record<string, unknown>;
  output_payload?: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
};

type ProductsListPanelProps = {
  refreshSignal?: number;
  focusProductId?: string | null;
  initialQuery?: {
    q?: string;
    status?: string;
    min_score?: string;
    sort_by?: "created_at" | "score_qualidade" | "sku" | "nome_produto";
    sort_dir?: "asc" | "desc";
    limit?: number;
    offset?: number;
  };
};

function getStatusBadgeClass(status: string) {
  const normalized = status.toLowerCase();
  if (normalized === "generated" || normalized === "completed") return "badge badge-ok";
  if (normalized === "failed" || normalized === "error") return "badge badge-danger";
  if (normalized === "pending" || normalized === "running") return "badge badge-warn";
  return "badge";
}

function getScoreBadgeClass(score: number | null) {
  if (score === null) return "badge";
  if (score >= 85) return "badge badge-ok";
  if (score >= 70) return "badge badge-warn";
  return "badge badge-danger";
}

export function ProductsListPanel({
  refreshSignal = 0,
  focusProductId = null,
  initialQuery,
}: ProductsListPanelProps) {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const hasUrlPrefs = !!(
    initialQuery?.q ||
    initialQuery?.status ||
    initialQuery?.min_score ||
    initialQuery?.sort_by ||
    initialQuery?.sort_dir ||
    typeof initialQuery?.limit === "number" ||
    typeof initialQuery?.offset === "number"
  );

  const [items, setItems] = useState<ProductRow[]>([]);
  const [searchTerm, setSearchTerm] = useState(initialQuery?.q ?? "");
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState(initialQuery?.q ?? "");
  const [statusFilter, setStatusFilter] = useState(initialQuery?.status ?? "generated");
  const [minScore, setMinScore] = useState(initialQuery?.min_score ?? "");
  const [sortBy, setSortBy] = useState<"created_at" | "score_qualidade" | "sku" | "nome_produto">(
    initialQuery?.sort_by ?? "created_at",
  );
  const [sortDir, setSortDir] = useState<"asc" | "desc">(initialQuery?.sort_dir ?? "desc");
  const [limit, setLimit] = useState(initialQuery?.limit ?? 10);
  const [offset, setOffset] = useState(initialQuery?.offset ?? 0);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastResponseStatus, setLastResponseStatus] = useState<number | null>(null);

  const [selectedProductId, setSelectedProductId] = useState<string | null>(null);
  const [selectedProduct, setSelectedProduct] = useState<ProductDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState<string | null>(null);
  const [copyFeedback, setCopyFeedback] = useState<string | null>(null);
  const [shareFeedback, setShareFeedback] = useState<string | null>(null);

  const canPrev = offset > 0;
  const canNext = offset + limit < total;
  const hasSearchFilter = debouncedSearchTerm.trim().length > 0;
  const hasAdvancedFilters =
    minScore.trim().length > 0 ||
    (statusFilter.trim().length > 0 && statusFilter.trim().toLowerCase() !== "generated");

  useEffect(() => {
    if (hasUrlPrefs) return;
    try {
      const saved = window.localStorage.getItem("wave2.products.listPrefs");
      if (!saved) return;
      const prefs = JSON.parse(saved) as Partial<{
        searchTerm: string;
        statusFilter: string;
        minScore: string;
        sortBy: "created_at" | "score_qualidade" | "sku" | "nome_produto";
        sortDir: "asc" | "desc";
        limit: number;
      }>;
      if (typeof prefs.searchTerm === "string") setSearchTerm(prefs.searchTerm);
      if (typeof prefs.statusFilter === "string") setStatusFilter(prefs.statusFilter);
      if (typeof prefs.minScore === "string") setMinScore(prefs.minScore);
      if (
        prefs.sortBy &&
        ["created_at", "score_qualidade", "sku", "nome_produto"].includes(prefs.sortBy)
      ) {
        setSortBy(prefs.sortBy);
      }
      if (prefs.sortDir && ["asc", "desc"].includes(prefs.sortDir)) {
        setSortDir(prefs.sortDir);
      }
      if (typeof prefs.limit === "number" && Number.isFinite(prefs.limit)) {
        setLimit(Math.min(50, Math.max(1, prefs.limit)));
      }
    } catch {
      // ignore localStorage parse/access issues
    }
  }, [hasUrlPrefs]);

  useEffect(() => {
    try {
      window.localStorage.setItem(
        "wave2.products.listPrefs",
        JSON.stringify({
          searchTerm,
          statusFilter,
          minScore,
          sortBy,
          sortDir,
          limit,
        }),
      );
    } catch {
      // ignore localStorage write failures
    }
  }, [searchTerm, statusFilter, minScore, sortBy, sortDir, limit]);

  useEffect(() => {
    const params = new URLSearchParams();
    if (searchTerm.trim()) params.set("q", searchTerm.trim());
    if (statusFilter.trim()) params.set("status", statusFilter.trim());
    if (minScore.trim()) params.set("min_score", minScore.trim());
    params.set("sort_by", sortBy);
    params.set("sort_dir", sortDir);
    params.set("limit", String(limit));
    params.set("offset", String(offset));
    if (selectedProductId) params.set("focus", selectedProductId);
    else if (focusProductId) params.set("focus", focusProductId);

    const next = params.toString();
    const current = searchParams.toString();
    if (next !== current) {
      router.replace(next ? `${pathname}?${next}` : pathname, { scroll: false });
    }
  }, [
    focusProductId,
    limit,
    minScore,
    offset,
    pathname,
    router,
    searchParams,
    searchTerm,
    selectedProductId,
    sortBy,
    sortDir,
    statusFilter,
  ]);

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

  async function copyCurrentViewLink() {
    try {
      const current = `${window.location.origin}${pathname}${
        searchParams.toString() ? `?${searchParams.toString()}` : ""
      }`;
      await navigator.clipboard.writeText(current);
      setShareFeedback("Link da visao atual copiado.");
      window.setTimeout(() => setShareFeedback(null), 1800);
    } catch {
      setShareFeedback("Falha ao copiar link da visao atual.");
      window.setTimeout(() => setShareFeedback(null), 1800);
    }
  }

  function applyPreset(preset: "generated" | "highScore" | "clear") {
    setOffset(0);
    if (preset === "generated") {
      setStatusFilter("generated");
      setMinScore("");
      setSearchTerm("");
      return;
    }
    if (preset === "highScore") {
      setStatusFilter("generated");
      setMinScore("80");
      return;
    }
    setStatusFilter("");
    setMinScore("");
    setSearchTerm("");
  }

  function applyLinkPreset(preset: "editorial" | "approved" | "highScore") {
    setOffset(0);
    setSortBy("created_at");
    setSortDir("desc");
    if (preset === "approved") {
      setStatusFilter("approved");
      setMinScore("");
      setSearchTerm("");
    } else if (preset === "highScore") {
      setStatusFilter("generated");
      setMinScore("85");
      setSearchTerm("");
    } else {
      setStatusFilter("generated");
      setMinScore("");
      setSearchTerm("camisa");
    }

    setShareFeedback(`Preset aplicado: ${preset}.`);
    window.setTimeout(() => setShareFeedback(null), 1400);
  }

  function resetView() {
    setSearchTerm("");
    setDebouncedSearchTerm("");
    setStatusFilter("generated");
    setMinScore("");
    setSortBy("created_at");
    setSortDir("desc");
    setLimit(10);
    setOffset(0);
    setSelectedProductId(null);
    setSelectedProduct(null);
    setDetailError(null);
    router.push(pathname);
    setShareFeedback("Visao resetada.");
    window.setTimeout(() => setShareFeedback(null), 1400);
  }

  const queryString = useMemo(() => {
    const params = new URLSearchParams();
    params.set("limit", String(limit));
    params.set("offset", String(offset));
    if (statusFilter.trim()) params.set("status", statusFilter.trim());
    if (minScore.trim()) params.set("min_score", minScore.trim());
    if (debouncedSearchTerm.trim()) params.set("q", debouncedSearchTerm.trim());
    params.set("sort_by", sortBy);
    params.set("sort_dir", sortDir);
    return params.toString();
  }, [debouncedSearchTerm, limit, offset, sortBy, sortDir, statusFilter, minScore]);

  const loadProducts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const parsed = await getJson<ProductsResponse>(`/api/products?${queryString}`);
      setLastResponseStatus(200);
      setItems(parsed.items || []);
      setTotal(parsed.pagination?.total || 0);
    } catch (loadError) {
      setItems([]);
      setTotal(0);
      if (loadError instanceof ApiClientError) {
        setLastResponseStatus(loadError.status);
        setError(loadError.message);
      } else {
        setError(loadError instanceof Error ? loadError.message : "Erro inesperado.");
      }
    } finally {
      setLoading(false);
    }
  }, [queryString]);

  const loadProductDetail = useCallback(async (productId: string) => {
    setSelectedProductId(productId);
    setDetailLoading(true);
    setDetailError(null);
    try {
      const body = await getJson<ProductDetail>(`/api/products/${productId}`);
      setSelectedProduct(body);
    } catch (err) {
      setSelectedProduct(null);
      if (err instanceof ApiClientError) {
        setDetailError(err.message);
      } else {
        setDetailError(err instanceof Error ? err.message : "Erro inesperado.");
      }
    } finally {
      setDetailLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadProducts();
  }, [loadProducts, refreshSignal]);

  useEffect(() => {
    if (!focusProductId) return;
    void loadProductDetail(focusProductId);
  }, [focusProductId, loadProductDetail]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setDebouncedSearchTerm(searchTerm);
    }, 250);
    return () => window.clearTimeout(timer);
  }, [searchTerm]);

  return (
    <section className="panel">
      <div className="section-head">
        <h2>Produtos gerados (listagem paginada)</h2>
        <p>Consulta `GET /api/v1/products` via proxy do Next (`/api/products`).</p>
        {error && lastResponseStatus === 503 ? (
          <p className="warn">
            Listagem indisponivel sem banco configurado. Ative a conexao da API com PostgreSQL para consultar produtos.
          </p>
        ) : null}
      </div>

      <div className="filters-grid">
        <label>
          Busca (SKU / nome / marca)
          <input
            value={searchTerm}
            onChange={(e) => {
              setOffset(0);
              setSearchTerm(e.target.value);
            }}
            placeholder="Ex.: CAM-001 ou Oxford"
          />
        </label>
        <label>
          Status
          <input
            value={statusFilter}
            onChange={(e) => {
              setOffset(0);
              setStatusFilter(e.target.value);
            }}
          />
        </label>
        <label>
          Min score
          <input
            type="number"
            step="1"
            min="0"
            max="100"
            value={minScore}
            onChange={(e) => {
              setOffset(0);
              setMinScore(e.target.value);
            }}
            placeholder="80"
          />
        </label>
        <label>
          Limite
          <input
            type="number"
            min="1"
            max="50"
            value={limit}
            onChange={(e) => {
              setOffset(0);
              setLimit(Math.min(50, Math.max(1, Number(e.target.value) || 10)));
            }}
          />
        </label>
        <label>
          Ordenar por
          <select
            value={sortBy}
            onChange={(e) => {
              setOffset(0);
              setSortBy(
                e.target.value as "created_at" | "score_qualidade" | "sku" | "nome_produto",
              );
            }}
          >
            <option value="created_at">Criado em</option>
            <option value="score_qualidade">Score</option>
            <option value="sku">SKU</option>
            <option value="nome_produto">Nome</option>
          </select>
        </label>
        <label>
          Direcao
          <select
            value={sortDir}
            onChange={(e) => {
              setOffset(0);
              setSortDir(e.target.value as "asc" | "desc");
            }}
          >
            <option value="desc">Desc</option>
            <option value="asc">Asc</option>
          </select>
        </label>
        <div className="filters-actions">
          <div className="filter-presets">
            <button type="button" onClick={() => applyPreset("generated")} disabled={loading}>
              Preset: Generated
            </button>
            <button type="button" onClick={() => applyPreset("highScore")} disabled={loading}>
              Preset: Score {"\u2265"} 80
            </button>
            <button type="button" onClick={() => applyPreset("clear")} disabled={loading}>
              Limpar filtros
            </button>
          </div>
          <div className="filter-presets">
            <button type="button" onClick={() => applyLinkPreset("editorial")}>
              Link: Revisao editorial
            </button>
            <button type="button" onClick={() => applyLinkPreset("approved")}>
              Link: Aprovados
            </button>
            <button type="button" onClick={() => applyLinkPreset("highScore")}>
              Link: Score alto
            </button>
          </div>
          <button
            type="button"
            onClick={() => {
              setOffset(0);
              void loadProducts();
            }}
            disabled={loading}
          >
            {loading ? "Atualizando..." : "Atualizar"}
          </button>
          <button type="button" onClick={() => void copyCurrentViewLink()}>
            Copiar link da visao
          </button>
          <button type="button" onClick={resetView}>
            Resetar visao
          </button>
          {lastResponseStatus !== null ? <span>Status HTTP: {lastResponseStatus}</span> : null}
          {shareFeedback ? <span className="ok">{shareFeedback}</span> : null}
          {error ? <span className="warn">{error}</span> : null}
        </div>
      </div>

      <div className="table-wrap">
        <table className="products-table">
          <thead>
            <tr>
              <th>SKU</th>
              <th>Produto</th>
              <th>Status</th>
              <th>Score</th>
              <th>Criado em</th>
              <th>Acoes</th>
            </tr>
          </thead>
          <tbody>
            {items.length === 0 ? (
              <tr>
                <td colSpan={6} className="empty-row">
                  {loading
                    ? "Carregando..."
                    : debouncedSearchTerm.trim()
                      ? "Nenhum item encontrado para a busca."
                      : "Nenhum item encontrado."}
                </td>
              </tr>
            ) : (
              items.map((item) => (
                <tr
                  key={item.id}
                  className={selectedProductId === item.id ? "row-selected" : undefined}
                  onClick={() => void loadProductDetail(item.id)}
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" || e.key === " ") {
                      e.preventDefault();
                      void loadProductDetail(item.id);
                    }
                  }}
                >
                  <td>{item.sku}</td>
                  <td>{item.nome_produto}</td>
                  <td>
                    <span className={getStatusBadgeClass(item.status)}>{item.status}</span>
                  </td>
                  <td>
                    <span className={getScoreBadgeClass(item.score_qualidade)}>
                      {item.score_qualidade ?? "-"}
                    </span>
                  </td>
                  <td>{new Date(item.created_at).toLocaleString("pt-BR")}</td>
                  <td>
                    <button
                      type="button"
                      className="table-inline-button"
                      onClick={(e) => {
                        e.stopPropagation();
                        void loadProductDetail(item.id);
                      }}
                    >
                      Ver detalhe
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {!loading && items.length === 0 ? (
        <div className="empty-guidance">
          <strong>Nenhum produto disponivel nesta visao.</strong>
          <p>
            {hasSearchFilter || hasAdvancedFilters
              ? "Ajuste ou limpe os filtros para ampliar os resultados."
              : "Gere o primeiro produto para iniciar a operacao."}
          </p>
          <div className="empty-guidance-actions">
            <button type="button" onClick={() => applyPreset("clear")}>
              Limpar filtros
            </button>
            <button type="button" onClick={() => router.push("/gerar")}>
              Ir para Gerar
            </button>
            {lastResponseStatus === 503 ? (
              <button type="button" onClick={() => router.push("/health")}>
                Ver Health
              </button>
            ) : null}
          </div>
        </div>
      ) : null}

      <div className="pagination-row">
        <span>
          Total API: <strong>{total}</strong> • Offset: <strong>{offset}</strong> • Limite:{" "}
          <strong>{limit}</strong>
        </span>
        <div className="pager-actions">
          <button
            type="button"
            disabled={!canPrev || loading}
            onClick={() => setOffset((prev) => Math.max(0, prev - limit))}
          >
            Anterior
          </button>
          <button
            type="button"
            disabled={!canNext || loading}
            onClick={() => setOffset((prev) => prev + limit)}
          >
            Proxima
          </button>
        </div>
      </div>

      <div className="detail-panel">
        <div className="section-head">
          <h3>Detalhe de produto</h3>
          <p>Clique em uma linha para consultar `GET /api/v1/products/{'{id}'}`.</p>
        </div>
        {copyFeedback ? <p className="ok">{copyFeedback}</p> : null}
        {detailError ? <p className="warn">{detailError}</p> : null}
        {selectedProduct ? (
          <div className="detail-summary-grid">
            <div>
              <span>ID</span>
              <strong className="copy-value">
                <code>{selectedProduct.id}</code>
                <button
                  type="button"
                  className="copy-inline-button"
                  onClick={() => void copyToClipboard("Product ID", selectedProduct.id)}
                >
                  Copiar
                </button>
              </strong>
            </div>
            <div>
              <span>SKU</span>
              <strong className="copy-value">
                <code>{selectedProduct.sku}</code>
                <button
                  type="button"
                  className="copy-inline-button"
                  onClick={() => void copyToClipboard("SKU", selectedProduct.sku)}
                >
                  Copiar
                </button>
              </strong>
            </div>
            <div>
              <span>Status</span>
              <strong>
                <span className={getStatusBadgeClass(selectedProduct.status)}>
                  {selectedProduct.status}
                </span>
              </strong>
            </div>
            <div>
              <span>Score</span>
              <strong>
                <span className={getScoreBadgeClass(selectedProduct.score_qualidade)}>
                  {selectedProduct.score_qualidade ?? "-"}
                </span>
              </strong>
            </div>
          </div>
        ) : null}
        <JsonViewer
          title="Detalhe completo"
          value={
            detailLoading
              ? { info: "Carregando detalhe..." }
              : selectedProduct ?? { info: "Nenhum produto selecionado" }
          }
          initiallyCollapsed
          previewMaxChars={260}
        />

        {selectedProduct ? (
          <div className="two-col detail-json-grid">
            <JsonViewer
              title="input_payload"
              value={selectedProduct.input_payload}
              initiallyCollapsed
              previewMaxChars={220}
            />
            <JsonViewer
              title="output_payload"
              value={selectedProduct.output_payload ?? { info: "Sem output_payload" }}
              initiallyCollapsed
              previewMaxChars={220}
            />
          </div>
        ) : null}
      </div>
    </section>
  );
}
