import { NextRequest, NextResponse } from "next/server";

import { apiBaseUrl } from "../../../../lib/api";

type RouteParams = {
  params: Promise<{ productId: string }>;
};

export async function GET(_request: NextRequest, context: RouteParams) {
  const { productId } = await context.params;

  try {
    const upstream = await fetch(`${apiBaseUrl}/api/v1/products/${productId}`, {
      method: "GET",
      cache: "no-store",
    });
    const text = await upstream.text();
    return new NextResponse(text, {
      status: upstream.status,
      headers: { "Content-Type": upstream.headers.get("content-type") || "application/json" },
    });
  } catch (error) {
    return NextResponse.json(
      {
        error: "upstream_unavailable",
        message:
          error instanceof Error ? error.message : "Falha ao conectar com a API backend.",
      },
      { status: 502 },
    );
  }
}
