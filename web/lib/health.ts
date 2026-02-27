import { apiBaseUrl } from "./api";

export async function getHealthSample() {
  try {
    const response = await fetch(`${apiBaseUrl}/healthz`, { cache: "no-store" });
    if (!response.ok) {
      return { ok: false, status: response.status };
    }
    return { ok: true, body: await response.json() };
  } catch (error) {
    return {
      ok: false,
      error: error instanceof Error ? error.message : "unknown_error",
    };
  }
}
