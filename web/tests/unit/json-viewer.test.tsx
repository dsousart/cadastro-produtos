import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { JsonViewer } from "../../components/json-viewer";

describe("JsonViewer", () => {
  it("renderiza preview quando inicia colapsado", () => {
    render(
      <JsonViewer
        title="Payload"
        value={{ sku: "CAM-001", status: "generated" }}
        initiallyCollapsed
      />,
    );

    expect(screen.getByRole("heading", { name: "Payload" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Expandir" })).toBeInTheDocument();
    expect(screen.queryByText(/"sku": "CAM-001"/)).not.toBeInTheDocument();
  });

  it("renderiza JSON completo quando nao inicia colapsado", () => {
    render(<JsonViewer title="Resposta" value={{ ok: true }} />);
    expect(screen.getByText(/"ok": true/)).toBeInTheDocument();
  });
});
