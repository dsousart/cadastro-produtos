import { Wave2Dashboard } from "../../components/wave2-dashboard";
import { getHealthSample } from "../../lib/health";

type ProdutosPageProps = {
  searchParams?: Promise<Record<string, string | string[] | undefined>>;
};

export default async function ProdutosPage({ searchParams }: ProdutosPageProps) {
  const health = await getHealthSample();
  const params = searchParams ? await searchParams : undefined;
  const valueOf = (key: string) => {
    const value = params?.[key];
    return Array.isArray(value) ? value[0] : value;
  };
  const toInt = (value: string | undefined, fallback: number) => {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : fallback;
  };

  const initialProductQuery = {
    q: valueOf("q"),
    status: valueOf("status"),
    min_score: valueOf("min_score"),
    sort_by: valueOf("sort_by") as "created_at" | "score_qualidade" | "sku" | "nome_produto" | undefined,
    sort_dir: valueOf("sort_dir") as "asc" | "desc" | undefined,
    limit: toInt(valueOf("limit"), 10),
    offset: toInt(valueOf("offset"), 0),
  };

  return (
    <Wave2Dashboard
      health={health}
      activeTab="produtos"
      focusProductId={valueOf("focus") ?? null}
      initialProductQuery={initialProductQuery}
    />
  );
}
