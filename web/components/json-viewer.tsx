"use client";

import React from "react";
import { useEffect, useMemo, useState } from "react";

type JsonViewerProps = {
  title: string;
  value: unknown;
  initiallyCollapsed?: boolean;
  previewMaxChars?: number;
};

function buildPreview(value: unknown, maxChars: number) {
  const json = JSON.stringify(value);
  if (!json) return "null";
  if (json.length <= maxChars) return json;
  return `${json.slice(0, maxChars)}...`;
}

export function JsonViewer({
  title,
  value,
  initiallyCollapsed = false,
  previewMaxChars = 220,
}: JsonViewerProps) {
  const [collapsed, setCollapsed] = useState(initiallyCollapsed);
  const preview = useMemo(() => buildPreview(value, previewMaxChars), [previewMaxChars, value]);

  useEffect(() => {
    setCollapsed(initiallyCollapsed);
  }, [initiallyCollapsed]);

  return (
    <div className="json-viewer">
      <div className="json-viewer-head">
        <h3>{title}</h3>
        <button
          type="button"
          className="copy-inline-button"
          onClick={() => setCollapsed((prev) => !prev)}
        >
          {collapsed ? "Expandir" : "Colapsar"}
        </button>
      </div>
      {collapsed ? (
        <pre className="json-preview">{preview}</pre>
      ) : (
        <pre>{JSON.stringify(value, null, 2)}</pre>
      )}
    </div>
  );
}
