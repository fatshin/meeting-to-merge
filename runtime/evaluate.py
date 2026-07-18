from __future__ import annotations

import json
import sys

import product


def main() -> int:
    payload = {field.name: field.value for field in product.PRODUCT.fields}
    result = product.analyze(payload)
    passed, checks = product.acceptance(result)
    print(json.dumps({
        "product": product.PRODUCT.name,
        "passed": passed,
        "checks": checks,
        "headline": result["headline"],
    }, indent=2, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())

