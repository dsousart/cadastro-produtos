import argparse
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from core.bk_validator import scan_base


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate BK markdown files")
    parser.add_argument(
        "--base",
        default=os.path.join(os.getcwd(), "base_conhecimento"),
        help="Base conhecimento path",
    )
    parser.add_argument("--out", help="Optional JSON report output path")
    args = parser.parse_args()

    report = scan_base(args.base)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2)

    summary = report.get("summary", {})
    files = report.get("files", {})

    print(
        "BK validation summary: "
        f"scanned={summary.get('files_scanned', 0)} "
        f"files_with_errors={summary.get('files_with_errors', 0)} "
        f"files_with_warnings={summary.get('files_with_warnings', 0)} "
        f"errors={summary.get('error_count', 0)} "
        f"warnings={summary.get('warning_count', 0)}"
    )

    if files:
        print("BK validation findings:")
        for path, result in files.items():
            print(f"- {path}")
            for issue in result.get("errors", []):
                print(f"  [ERRO] {issue}")
            for issue in result.get("warnings", []):
                print(f"  [AVISO] {issue}")

    if summary.get("error_count", 0) > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
