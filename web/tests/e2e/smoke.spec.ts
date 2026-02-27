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
