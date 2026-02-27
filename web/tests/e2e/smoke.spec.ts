import { expect, test } from "@playwright/test";

test("produtos: carrega dashboard com estado vazio guiado", async ({ page }) => {
  await page.route("**/api/products**", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        items: [],
        pagination: { total: 0, limit: 10, offset: 0 },
      }),
    });
  });

  await page.goto("/produtos");
  await expect(page.getByRole("heading", { name: "Workspace Operacional" })).toBeVisible();
  await expect(page.getByText("Nenhum produto disponivel nesta visao.")).toBeVisible();
  await expect(page.getByRole("button", { name: "Ir para Gerar" })).toBeVisible();
});

test("gerar: carrega formulario principal", async ({ page }) => {
  await page.goto("/gerar");
  await expect(
    page.getByRole("heading", { name: "Gerar produto (Wave 2 - primeiro fluxo)" }),
  ).toBeVisible();
  await expect(page.getByRole("button", { name: "Gerar produto" })).toBeVisible();
});

test("health: exibe painel de health na rota dedicada", async ({ page }) => {
  await page.goto("/health");
  await expect(page.getByRole("heading", { name: "Health payload (amostra)" })).toBeVisible();
});

test("produtos: aplica estado inicial de query params", async ({ page }) => {
  await page.route("**/api/products**", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        items: [],
        pagination: { total: 0, limit: 5, offset: 0 },
      }),
    });
  });

  await page.goto("/produtos?q=camisa&status=approved&min_score=85&sort_by=sku&sort_dir=asc&limit=5&offset=0");
  await expect(page.getByLabel("Busca (SKU / nome / marca)")).toHaveValue("camisa");
  await expect(page.getByLabel("Status")).toHaveValue("approved");
  await expect(page.getByLabel("Min score")).toHaveValue("85");
  await expect(page.getByLabel("Ordenar por")).toHaveValue("sku");
  await expect(page.getByLabel("Direcao")).toHaveValue("asc");
  await expect(page.getByLabel("Limite")).toHaveValue("5");
});

test("tabs: preserva contexto de filtros ao voltar para produtos", async ({ page }) => {
  await page.route("**/api/products**", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        items: [],
        pagination: { total: 0, limit: 5, offset: 0 },
      }),
    });
  });

  await page.goto("/produtos?q=camisa&status=approved&limit=5");
  await expect(page.getByLabel("Busca (SKU / nome / marca)")).toHaveValue("camisa");
  await expect(page.getByLabel("Status")).toHaveValue("approved");

  await page.locator('a[href="/jobs"]').click();
  await expect(page).toHaveURL(/\/jobs$/);

  const produtosTab = page.getByRole("tab", { name: "Produtos" });
  await expect(produtosTab).toHaveAttribute("href", /q=camisa/);
  await produtosTab.click();

  await expect(page).toHaveURL(/\/produtos\?/);
  await expect(page.getByLabel("Busca (SKU / nome / marca)")).toHaveValue("camisa");
  await expect(page.getByLabel("Status")).toHaveValue("approved");
});

test("produtos: resetar visao limpa query e retorna defaults", async ({ page }) => {
  await page.route("**/api/products**", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        items: [],
        pagination: { total: 0, limit: 5, offset: 0 },
      }),
    });
  });

  await page.goto("/produtos?q=camisa&status=approved&min_score=85&sort_by=sku&sort_dir=asc&limit=5&offset=10");
  await page.getByRole("button", { name: "Resetar visao" }).click();

  await expect(page).toHaveURL(/\/produtos\?status=generated&sort_by=created_at&sort_dir=desc&limit=10&offset=0/);
  await expect(page.getByLabel("Busca (SKU / nome / marca)")).toHaveValue("");
  await expect(page.getByLabel("Status")).toHaveValue("generated");
  await expect(page.getByLabel("Min score")).toHaveValue("");
  await expect(page.getByLabel("Ordenar por")).toHaveValue("created_at");
  await expect(page.getByLabel("Direcao")).toHaveValue("desc");
  await expect(page.getByLabel("Limite")).toHaveValue("10");
});

test("produtos: copiar link da visao mostra feedback", async ({ page }) => {
  await page.addInitScript(() => {
    const writeText = async () => {};
    Object.defineProperty(navigator, "clipboard", {
      configurable: true,
      value: { writeText },
    });
  });

  await page.route("**/api/products**", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        items: [],
        pagination: { total: 0, limit: 10, offset: 0 },
      }),
    });
  });

  await page.goto("/produtos?q=camisa&status=approved");
  await page.getByRole("button", { name: "Copiar link da visao" }).click();
  await expect(page.getByText("Link da visao atual copiado.")).toBeVisible();
});

test("produtos: presets de link aplicam filtros esperados", async ({ page }) => {
  await page.route("**/api/products**", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        items: [],
        pagination: { total: 0, limit: 10, offset: 0 },
      }),
    });
  });

  await page.goto("/produtos");

  await page.getByRole("button", { name: "Link: Revisao editorial" }).click();
  await expect(page).toHaveURL(/\/produtos\?(?=.*status=generated)(?=.*q=camisa)/);

  await page.getByRole("button", { name: "Link: Aprovados" }).click();
  await expect(page).toHaveURL(/\/produtos\?.*status=approved/);

  await page.getByRole("button", { name: "Link: Score alto" }).click();
  await expect(page).toHaveURL(/\/produtos\?(?=.*status=generated)(?=.*min_score=85)/);
});

test("e2e: gerar -> jobs -> produtos com focus atualizado", async ({ page }) => {
  await page.route("**/api/products", async (route) => {
    if (route.request().method() !== "POST") {
      await route.continue();
      return;
    }
    await route.fulfill({
      status: 201,
      contentType: "application/json",
      body: JSON.stringify({
        metadata: { product_id: "prod-from-gerar-001" },
      }),
    });
  });

  await page.route("**/api/generation-jobs", async (route) => {
    if (route.request().method() !== "POST") {
      await route.continue();
      return;
    }
    await route.fulfill({
      status: 202,
      contentType: "application/json",
      body: JSON.stringify({
        job_id: "job-e2e-flow-001",
        status: "pending",
        total_items: 1,
        message: "accepted",
      }),
    });
  });

  await page.route("**/api/generation-jobs/job-e2e-flow-001", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        id: "job-e2e-flow-001",
        status: "completed",
        total_items: 1,
        completed_items: 1,
        failed_items: 0,
        results: [{ index: 0, sku: "CAM-E2E-001", status: "completed", product_id: "prod-from-job-001" }],
      }),
    });
  });

  await page.route("**/api/products?**", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        items: [
          {
            id: "prod-from-gerar-001",
            sku: "CAM-GERAR-001",
            nome_produto: "Camisa Gerar",
            marca: "Lumen",
            status: "generated",
            score_qualidade: 88,
            created_at: "2026-02-27T10:00:00Z",
          },
          {
            id: "prod-from-job-001",
            sku: "CAM-JOB-001",
            nome_produto: "Camisa Job",
            marca: "Lumen",
            status: "generated",
            score_qualidade: 91,
            created_at: "2026-02-27T10:05:00Z",
          },
        ],
        pagination: { total: 2, limit: 10, offset: 0 },
      }),
    });
  });

  await page.route("**/api/products/*", async (route) => {
    const url = new URL(route.request().url());
    const productId = url.pathname.split("/").pop() ?? "unknown";
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        id: productId,
        sku: productId === "prod-from-job-001" ? "CAM-JOB-001" : "CAM-GERAR-001",
        nome_produto: productId === "prod-from-job-001" ? "Camisa Job" : "Camisa Gerar",
        marca: "Lumen",
        status: "generated",
        score_qualidade: productId === "prod-from-job-001" ? 91 : 88,
        input_payload: {},
        output_payload: {},
        created_at: "2026-02-27T10:00:00Z",
        updated_at: "2026-02-27T10:06:00Z",
      }),
    });
  });

  await page.goto("/gerar");
  await page.getByRole("button", { name: "Gerar produto" }).click();
  await expect(page).toHaveURL(/\/produtos\?(?=.*focus=prod-from-gerar-001)/);

  await page.getByRole("tab", { name: "Jobs" }).click();
  await expect(page).toHaveURL(/\/jobs$/);
  await page.getByRole("button", { name: "Criar generation-job" }).first().click();

  await expect(page).toHaveURL(/\/produtos\?(?=.*focus=prod-from-job-001)/);
  await expect(page.locator(".detail-summary-grid code").first()).toHaveText("prod-from-job-001");
});

test("e2e: gerar sem product_id redireciona com fallback por SKU e abre detalhe", async ({ page }) => {
  await page.route("**/api/products", async (route) => {
    if (route.request().method() !== "POST") {
      await route.continue();
      return;
    }
    await route.fulfill({
      status: 201,
      contentType: "application/json",
      body: JSON.stringify({
        input_payload: { sku: "CAM-001-WEB" },
      }),
    });
  });

  await page.route("**/api/products?**", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        items: [
          {
            id: "prod-sku-fallback-001",
            sku: "CAM-001-WEB",
            nome_produto: "Camisa Oxford",
            marca: "Lumen",
            status: "generated",
            score_qualidade: 84,
            created_at: "2026-02-27T10:00:00Z",
          },
        ],
        pagination: { total: 1, limit: 10, offset: 0 },
      }),
    });
  });

  await page.route("**/api/products/prod-sku-fallback-001", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        id: "prod-sku-fallback-001",
        sku: "CAM-001-WEB",
        nome_produto: "Camisa Oxford",
        marca: "Lumen",
        status: "generated",
        score_qualidade: 84,
        input_payload: {},
        output_payload: {},
        created_at: "2026-02-27T10:00:00Z",
        updated_at: "2026-02-27T10:06:00Z",
      }),
    });
  });

  await page.goto("/gerar");
  await page.getByRole("button", { name: "Gerar produto" }).click();

  await expect(page).toHaveURL(/\/produtos\?(?=.*q=CAM-001-WEB)(?=.*focus_sku=CAM-001-WEB)/);
  await expect(page.locator(".detail-summary-grid code").first()).toHaveText("prod-sku-fallback-001");
});

test("jobs: cria job e completa polling", async ({ page }) => {
  let pollCount = 0;

  await page.route("**/api/generation-jobs", async (route) => {
    if (route.request().method() !== "POST") {
      await route.continue();
      return;
    }
    await route.fulfill({
      status: 202,
      contentType: "application/json",
      body: JSON.stringify({
        job_id: "job-smoke-001",
        status: "pending",
        total_items: 1,
        message: "accepted",
      }),
    });
  });

  await page.route("**/api/generation-jobs/job-smoke-001", async (route) => {
    pollCount += 1;
    const completed = pollCount >= 2;
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        id: "job-smoke-001",
        status: completed ? "completed" : "running",
        total_items: 1,
        completed_items: completed ? 1 : 0,
        failed_items: 0,
        results: completed
          ? [{ index: 0, sku: "CAM-JOB-WEB-1", status: "completed", product_id: "prod-001" }]
          : [],
      }),
    });
  });

  await page.goto("/jobs");
  await expect(page.getByText("Nenhum generation-job iniciado.")).toBeVisible();
  await page.getByRole("button", { name: "Criar generation-job" }).first().click();
  await expect(page.getByText("Status atual:")).toBeVisible();
  await expect(page.getByText("completed")).toBeVisible();
});

test("produtos: exibe erro de API quando listagem falha", async ({ page }) => {
  await page.route("**/api/products**", async (route) => {
    await route.fulfill({
      status: 500,
      contentType: "application/json",
      body: JSON.stringify({
        message: "Erro interno na listagem",
      }),
    });
  });

  await page.goto("/produtos");
  await expect(page.getByText("Erro interno na listagem")).toBeVisible();
});

test("produtos: atualiza status editorial pelo detalhe", async ({ page }) => {
  await page.route("**/api/products?**", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        items: [
          {
            id: "prod-editorial-001",
            sku: "CAM-EDITORIAL-001",
            nome_produto: "Camisa Editorial",
            marca: "Lumen",
            status: "generated",
            score_qualidade: 88,
            created_at: "2026-02-27T10:00:00Z",
          },
        ],
        pagination: { total: 1, limit: 10, offset: 0 },
      }),
    });
  });

  await page.route("**/api/products/prod-editorial-001", async (route) => {
    if (route.request().method() === "PATCH") {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          id: "prod-editorial-001",
          status: "approved",
          updated_at: "2026-02-27T10:10:00Z",
        }),
      });
      return;
    }
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        id: "prod-editorial-001",
        sku: "CAM-EDITORIAL-001",
        nome_produto: "Camisa Editorial",
        marca: "Lumen",
        status: "generated",
        score_qualidade: 88,
        input_payload: {},
        output_payload: {},
        created_at: "2026-02-27T10:00:00Z",
        updated_at: "2026-02-27T10:00:01Z",
      }),
    });
  });

  await page.goto("/produtos");
  await page.locator("button.table-inline-button").first().click();
  await page.getByRole("button", { name: "Aprovar" }).click();

  await expect(page.getByText("Status atualizado: Aprovado.")).toBeVisible();
  await expect(page.getByText("approved")).toBeVisible();
});

test("gerar: exibe erro de API quando criacao falha", async ({ page }) => {
  await page.route("**/api/products", async (route) => {
    if (route.request().method() !== "POST") {
      await route.continue();
      return;
    }
    await route.fulfill({
      status: 500,
      contentType: "application/json",
      body: JSON.stringify({
        message: "Erro ao criar produto",
        error: "create_failed",
      }),
    });
  });

  await page.goto("/gerar");
  await page.getByRole("button", { name: "Gerar produto" }).click();
  await expect(page.locator(".form-actions .warn")).toHaveText("Erro ao criar produto");
  await expect(page.getByText("Status HTTP: 500")).toBeVisible();
});

test("produtos: exibe erro quando backend esta indisponivel", async ({ page }) => {
  await page.route("**/api/products**", async (route) => {
    await route.abort("failed");
  });

  await page.goto("/produtos");
  await expect(page.getByText("Failed to fetch")).toBeVisible();
});

test("gerar: exibe erro quando backend esta indisponivel", async ({ page }) => {
  await page.route("**/api/products", async (route) => {
    if (route.request().method() !== "POST") {
      await route.continue();
      return;
    }
    await route.abort("failed");
  });

  await page.goto("/gerar");
  await page.getByRole("button", { name: "Gerar produto" }).click();
  await expect(page.locator(".form-actions .warn")).toHaveText("Failed to fetch");
});

test("jobs: exibe erro quando polling retorna 500", async ({ page }) => {
  await page.route("**/api/generation-jobs", async (route) => {
    if (route.request().method() !== "POST") {
      await route.continue();
      return;
    }
    await route.fulfill({
      status: 202,
      contentType: "application/json",
      body: JSON.stringify({
        job_id: "job-smoke-fail-500",
        status: "pending",
        total_items: 1,
        message: "accepted",
      }),
    });
  });

  await page.route("**/api/generation-jobs/job-smoke-fail-500", async (route) => {
    await route.fulfill({
      status: 500,
      contentType: "application/json",
      body: JSON.stringify({
        message: "Falha ao consultar job",
      }),
    });
  });

  await page.goto("/jobs");
  await page.getByRole("button", { name: "Criar generation-job" }).first().click();
  await expect(page.locator(".form-actions .warn")).toHaveText("Falha ao consultar job");
});

test("jobs: exibe erro quando polling falha por rede", async ({ page }) => {
  await page.route("**/api/generation-jobs", async (route) => {
    if (route.request().method() !== "POST") {
      await route.continue();
      return;
    }
    await route.fulfill({
      status: 202,
      contentType: "application/json",
      body: JSON.stringify({
        job_id: "job-smoke-fail-network",
        status: "pending",
        total_items: 1,
        message: "accepted",
      }),
    });
  });

  await page.route("**/api/generation-jobs/job-smoke-fail-network", async (route) => {
    await route.abort("failed");
  });

  await page.goto("/jobs");
  await page.getByRole("button", { name: "Criar generation-job" }).first().click();
  await expect(page.locator(".form-actions .warn")).toHaveText("Failed to fetch");
});
