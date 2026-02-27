export class ApiClientError extends Error {
  status: number;
  code?: string;

  constructor(message: string, status: number, code?: string) {
    super(message);
    this.name = "ApiClientError";
    this.status = status;
    this.code = code;
  }
}

function extractErrorMessage(body: unknown, fallback: string) {
  if (body && typeof body === "object") {
    const obj = body as Record<string, unknown>;
    if (Array.isArray(obj.detail) && obj.detail.length > 0) {
      const first = obj.detail[0];
      if (first && typeof first === "object") {
        const issue = first as Record<string, unknown>;
        const loc = Array.isArray(issue.loc) ? issue.loc.join(".") : "";
        const msg = typeof issue.msg === "string" ? issue.msg : "";
        if (msg && loc) return `${msg} (campo: ${loc})`;
        if (msg) return msg;
      }
    }
    if (typeof obj.detail === "string" && obj.detail) return obj.detail;
    if (typeof obj.message === "string" && obj.message) return obj.message;
    if (typeof obj.error === "string" && obj.error) return obj.error;
  }
  return fallback;
}

async function parseResponseBody(response: Response) {
  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) return response.json();
  const text = await response.text();
  return { message: text || response.statusText };
}

export async function requestJson<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, init);
  const body = await parseResponseBody(response);

  if (!response.ok) {
    const message = extractErrorMessage(body, `Request failed (${response.status}).`);
    const code =
      body && typeof body === "object" && typeof (body as Record<string, unknown>).error === "string"
        ? ((body as Record<string, unknown>).error as string)
        : undefined;
    throw new ApiClientError(message, response.status, code);
  }

  return body as T;
}

export async function getJson<T>(url: string): Promise<T> {
  return requestJson<T>(url, { method: "GET", cache: "no-store" });
}

export async function postJson<TRequest, TResponse>(
  url: string,
  payload: TRequest,
): Promise<TResponse> {
  return requestJson<TResponse>(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function patchJson<TRequest, TResponse>(
  url: string,
  payload: TRequest,
): Promise<TResponse> {
  return requestJson<TResponse>(url, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}
