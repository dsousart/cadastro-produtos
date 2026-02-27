import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { ProductGeneratorForm } from "../../components/product-generator-form";

const postJsonMock = vi.fn();

vi.mock("../../lib/api-client", () => ({
  postJson: (...args: unknown[]) => postJsonMock(...args),
  ApiClientError: class ApiClientError extends Error {
    status: number;
    code?: string;
    constructor(message: string, status: number, code?: string) {
      super(message);
      this.status = status;
      this.code = code;
    }
  },
}));

describe("ProductGeneratorForm", () => {
  beforeEach(() => {
    postJsonMock.mockReset();
  });

  it("submete payload e dispara onCreated com productId", async () => {
    const onCreated = vi.fn();
    postJsonMock.mockResolvedValueOnce({ metadata: { product_id: "prod-123" } });

    render(<ProductGeneratorForm onCreated={onCreated} />);

    await userEvent.click(screen.getByRole("button", { name: "Gerar produto" }));

    expect(postJsonMock).toHaveBeenCalledTimes(1);
    expect(postJsonMock).toHaveBeenCalledWith(
      "/api/products",
      expect.objectContaining({
        sku: "CAM-001-WEB",
        nome_produto: "Camisa Oxford",
      }),
    );
    expect(onCreated).toHaveBeenCalledWith({ productId: "prod-123", sku: "CAM-001-WEB" });
    expect(screen.getByText("Status HTTP: 201")).toBeInTheDocument();
  });

  it("mostra erro quando request falha", async () => {
    postJsonMock.mockRejectedValueOnce(new Error("Falha de rede"));

    render(<ProductGeneratorForm />);
    await userEvent.click(screen.getByRole("button", { name: "Gerar produto" }));

    expect(screen.getByText("Falha de rede")).toBeInTheDocument();
  });
});
