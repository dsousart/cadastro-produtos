"use client";

import Link from "next/link";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { GenerationJobsPanel } from "./generation-jobs-panel";
import { ProductGeneratorForm } from "./product-generator-form";
import { ProductsListPanel } from "./products-list-panel";

type Wave2DashboardProps = {
  health: unknown;
  activeTab: DashboardTab;
  focusProductId?: string | null;
  initialProductQuery?: {
    q?: string;
    status?: string;
    min_score?: string;
    sort_by?: "created_at" | "score_qualidade" | "sku" | "nome_produto";
    sort_dir?: "asc" | "desc";
    limit?: number;
    offset?: number;
  };
};

type DashboardTab = "gerar" | "produtos" | "jobs" | "health";

export function Wave2Dashboard({
  health,
  activeTab,
  focusProductId = null,
  initialProductQuery,
}: Wave2DashboardProps) {
  const router = useRouter();

  useEffect(() => {
    try {
      window.localStorage.setItem("wave2.dashboard.activeTab", activeTab);
    } catch {
      // ignore localStorage errors
    }
  }, [activeTab]);

  return (
    <>
      <section className="panel">
        <h2>Proximos blocos da Wave 2</h2>
        <ul>
          <li>Formulario de geracao (`POST /api/v1/products`) - base implementada</li>
          <li>Tabela paginada de produtos (`GET /api/v1/products`) - base implementada</li>
          <li>Painel de jobs (`generation-jobs` + polling de status) - base implementada</li>
          <li>Estados de erro/loading e observabilidade basica de UX</li>
        </ul>
      </section>

      <section className="panel">
        <div className="tabs-head">
          <h2>Workspace Operacional</h2>
          <div className="tabs-nav" role="tablist" aria-label="Navegacao Wave 2">
            <Link
              href="/gerar"
              role="tab"
              aria-selected={activeTab === "gerar"}
              className={activeTab === "gerar" ? "tab-button is-active" : "tab-button"}
            >
              Gerar
            </Link>
            <Link
              href="/produtos"
              role="tab"
              aria-selected={activeTab === "produtos"}
              className={activeTab === "produtos" ? "tab-button is-active" : "tab-button"}
            >
              Produtos
            </Link>
            <Link
              href="/jobs"
              role="tab"
              aria-selected={activeTab === "jobs"}
              className={activeTab === "jobs" ? "tab-button is-active" : "tab-button"}
            >
              Jobs
            </Link>
            <Link
              href="/health"
              role="tab"
              aria-selected={activeTab === "health"}
              className={activeTab === "health" ? "tab-button is-active" : "tab-button"}
            >
              Health
            </Link>
          </div>
        </div>

        {activeTab === "gerar" ? (
          <ProductGeneratorForm
            onCreated={({ productId }) => {
              const target = productId ? `/produtos?focus=${encodeURIComponent(productId)}` : "/produtos";
              router.push(target);
            }}
          />
        ) : null}

        {activeTab === "produtos" ? (
          <ProductsListPanel
            refreshSignal={0}
            focusProductId={focusProductId}
            initialQuery={initialProductQuery}
          />
        ) : null}

        {activeTab === "jobs" ? (
          <GenerationJobsPanel
            onJobCompleted={({ productIds }) => {
              const productId = productIds[0] ?? null;
              const target = productId ? `/produtos?focus=${encodeURIComponent(productId)}` : "/produtos";
              router.push(target);
            }}
          />
        ) : null}

        {activeTab === "health" ? (
          <section className="panel panel-inner">
            <h2>Health payload (amostra)</h2>
            <pre>{JSON.stringify(health, null, 2)}</pre>
          </section>
        ) : null}
      </section>
    </>
  );
}
