"use client";

import React from "react";
import { FormEvent, useMemo, useState } from "react";
import { JsonViewer } from "./json-viewer";
import { ApiClientError, postJson } from "../lib/api-client";

type FormState = {
  sku: string;
  nome_produto: string;
  descricao_bruta: string;
  marca: string;
  categoria: string;
  subcategoria: string;
  tamanhos_csv: string;
  cores_csv: string;
  composicao: string;
  tecido: string;
  modelagem: string;
  acabamento: string;
  colecao: string;
  preco: string;
  usuario: string;
};

const initialState: FormState = {
  sku: "CAM-001-WEB",
  nome_produto: "Camisa Oxford",
  descricao_bruta: "Camisa social em algodao com toque macio.",
  marca: "Lumen",
  categoria: "camisa",
  subcategoria: "social",
  tamanhos_csv: "P, M, G",
  cores_csv: "Azul Marinho, Branco",
  composicao: "100% algodao",
  tecido: "oxford",
  modelagem: "regular",
  acabamento: "costuras reforcadas",
  colecao: "essenciais",
  preco: "299.9",
  usuario: "demo-web",
};

function toPayload(state: FormState) {
  const toList = (value: string) =>
    value
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);

  return {
    sku: state.sku.trim(),
    nome_produto: state.nome_produto.trim(),
    descricao_bruta: state.descricao_bruta.trim(),
    marca: state.marca.trim(),
    categoria: state.categoria.trim(),
    subcategoria: state.subcategoria.trim(),
    tamanhos: toList(state.tamanhos_csv),
    cores: toList(state.cores_csv),
    composicao: state.composicao.trim(),
    tecido: state.tecido.trim(),
    modelagem: state.modelagem.trim(),
    acabamento: state.acabamento.trim(),
    colecao: state.colecao.trim(),
    preco: Number(state.preco),
    promocao: null,
    imagens: [],
    guidelines_marca: { termos_proibidos: [] },
    regras_categoria: { tamanhos_validos: [], cores_validas: [] },
    restricoes_legais: { claims_proibidos: [] },
    usuario: state.usuario.trim(),
    versao_pipeline: "1.0.0",
  };
}

type ProductGeneratorFormProps = {
  onCreated?: (payload: { productId?: string | null; sku?: string | null }) => void;
};

export function ProductGeneratorForm({ onCreated }: ProductGeneratorFormProps) {
  const [form, setForm] = useState<FormState>(initialState);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [responseStatus, setResponseStatus] = useState<number | null>(null);
  const [responseBody, setResponseBody] = useState<unknown | null>(null);

  const payloadPreview = useMemo(() => toPayload(form), [form]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setError(null);
    setResponseStatus(null);

    try {
      const body = await postJson<Record<string, unknown>, unknown>("/api/products", payloadPreview);
      setResponseStatus(201);
      setResponseBody(body);
      if (body && typeof body === "object") {
        const metadata =
          "metadata" in (body as Record<string, unknown>)
            ? ((body as Record<string, unknown>).metadata as Record<string, unknown> | null)
            : null;
        onCreated?.({
          productId:
            metadata && typeof metadata.product_id === "string" ? metadata.product_id : null,
          sku:
            "input_payload" in (body as Record<string, unknown>)
              ? null
              : payloadPreview.sku,
        });
      }
    } catch (submitError) {
      if (submitError instanceof ApiClientError) {
        setResponseStatus(submitError.status);
        setError(submitError.message);
        setResponseBody({ error: submitError.code ?? "api_error", message: submitError.message });
      } else {
        setError(submitError instanceof Error ? submitError.message : "Erro inesperado.");
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  function update<K extends keyof FormState>(key: K, value: FormState[K]) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  return (
    <section className="panel">
      <div className="section-head">
        <h2>Gerar produto (Wave 2 - primeiro fluxo)</h2>
        <p>
          Formulario inicial para enviar payload para `POST /api/v1/products` via proxy do Next
          (`/api/products`).
        </p>
      </div>

      <form className="form-grid" onSubmit={handleSubmit}>
        <label>
          SKU
          <input value={form.sku} onChange={(e) => update("sku", e.target.value)} required />
        </label>
        <label>
          Nome do produto
          <input
            value={form.nome_produto}
            onChange={(e) => update("nome_produto", e.target.value)}
            required
          />
        </label>
        <label className="full">
          Descricao bruta
          <textarea
            rows={4}
            value={form.descricao_bruta}
            onChange={(e) => update("descricao_bruta", e.target.value)}
            required
          />
        </label>
        <label>
          Marca
          <input value={form.marca} onChange={(e) => update("marca", e.target.value)} required />
        </label>
        <label>
          Categoria
          <input
            value={form.categoria}
            onChange={(e) => update("categoria", e.target.value)}
            required
          />
        </label>
        <label>
          Subcategoria
          <input
            value={form.subcategoria}
            onChange={(e) => update("subcategoria", e.target.value)}
            required
          />
        </label>
        <label>
          Tamanhos (CSV)
          <input
            value={form.tamanhos_csv}
            onChange={(e) => update("tamanhos_csv", e.target.value)}
            required
          />
        </label>
        <label>
          Cores (CSV)
          <input
            value={form.cores_csv}
            onChange={(e) => update("cores_csv", e.target.value)}
            required
          />
        </label>
        <label>
          Composicao
          <input
            value={form.composicao}
            onChange={(e) => update("composicao", e.target.value)}
            required
          />
        </label>
        <label>
          Tecido
          <input
            value={form.tecido}
            onChange={(e) => update("tecido", e.target.value)}
            required
          />
        </label>
        <label>
          Modelagem
          <input
            value={form.modelagem}
            onChange={(e) => update("modelagem", e.target.value)}
            required
          />
        </label>
        <label>
          Acabamento
          <input
            value={form.acabamento}
            onChange={(e) => update("acabamento", e.target.value)}
            required
          />
        </label>
        <label>
          Colecao
          <input
            value={form.colecao}
            onChange={(e) => update("colecao", e.target.value)}
            required
          />
        </label>
        <label>
          Preco
          <input
            type="number"
            step="0.01"
            min="0"
            value={form.preco}
            onChange={(e) => update("preco", e.target.value)}
            required
          />
        </label>
        <label>
          Usuario
          <input
            value={form.usuario}
            onChange={(e) => update("usuario", e.target.value)}
            required
          />
        </label>

        <div className="full form-actions">
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Gerando..." : "Gerar produto"}
          </button>
          {responseStatus !== null ? <span>Status HTTP: {responseStatus}</span> : null}
          {error ? <span className="warn">{error}</span> : null}
        </div>
      </form>

      <div className="two-col">
        <div>
          <JsonViewer title="Payload enviado (preview)" value={payloadPreview} />
        </div>
        <div>
          <JsonViewer
            title="Resposta da API"
            value={responseBody ?? { info: "Sem resposta ainda" }}
            initiallyCollapsed
          />
        </div>
      </div>
    </section>
  );
}
