"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { usePathname, useSearchParams } from "next/navigation";

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
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const [productsHref, setProductsHref] = useState("/produtos");
  const searchParamsKey = searchParams.toString();

  useEffect(() => {
    if (pathname !== "/produtos") return;
    const nextHref = searchParamsKey ? `/produtos?${searchParamsKey}` : "/produtos";
    setProductsHref(nextHref);
    try {
      window.localStorage.setItem("wave2.products.lastView", nextHref);
    } catch {
      // ignore localStorage errors
    }
  }, [pathname, searchParamsKey]);

  useEffect(() => {
    if (pathname === "/produtos") return;
    try {
      const savedHref = window.localStorage.getItem("wave2.products.lastView");
      if (savedHref && savedHref.startsWith("/produtos")) {
        setProductsHref(savedHref);
      }
    } catch {
      // ignore localStorage errors
    }
  }, [pathname]);

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
        <h2>Como usar este workspace</h2>
        <ul>
          <li>Use <strong>Gerar</strong> para criar novos produtos.</li>
          <li>Use <strong>Jobs</strong> para acompanhar processamento em lote.</li>
          <li>Use <strong>Produtos</strong> para revisar resultado, score e detalhes.</li>
          <li>Use <strong>Health</strong> para diagnosticar ambiente local (API/banco).</li>
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
              href={productsHref}
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
