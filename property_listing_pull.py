#!/usr/bin/env python3
"""Pull property listing data from a configurable HTTP API endpoint.

This script is intentionally provider-agnostic so you can point it at the
property API your team uses (MLS proxy, internal service, third-party vendor).

Example:
    python property_listing_pull.py \
      --base-url "https://example.com/api/listings" \
      --api-key "$PROPERTY_API_KEY" \
      --city "Austin" \
      --state "TX" \
      --pages 3 \
      --out listings.json
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

import requests


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pull property listing data")
    parser.add_argument(
        "--base-url",
        required=True,
        help="Listing search endpoint (e.g., https://example.com/api/listings)",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("PROPERTY_API_KEY"),
        help="API key. If omitted, PROPERTY_API_KEY env var is used.",
    )
    parser.add_argument("--city", default=None, help="City filter")
    parser.add_argument("--state", default=None, help="State/region filter")
    parser.add_argument("--min-price", type=int, default=None)
    parser.add_argument("--max-price", type=int, default=None)
    parser.add_argument("--beds", type=int, default=None, help="Minimum bedrooms")
    parser.add_argument("--baths", type=float, default=None, help="Minimum bathrooms")
    parser.add_argument("--page-size", type=int, default=50)
    parser.add_argument("--pages", type=int, default=1, help="How many pages to pull")
    parser.add_argument(
        "--format",
        choices=("json", "csv"),
        default="json",
        help="Output format",
    )
    parser.add_argument("--out", default="property_listings.json", help="Output file path")
    parser.add_argument(
        "--api-key-header",
        default="X-API-Key",
        help="Header name for API key auth",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=20,
        help="Per-request timeout in seconds",
    )
    return parser.parse_args()


def build_query_params(args: argparse.Namespace, page: int) -> Dict[str, Any]:
    params: Dict[str, Any] = {
        "page": page,
        "limit": args.page_size,
    }
    optional = {
        "city": args.city,
        "state": args.state,
        "min_price": args.min_price,
        "max_price": args.max_price,
        "beds": args.beds,
        "baths": args.baths,
    }
    params.update({k: v for k, v in optional.items() if v is not None})
    return params


def normalize_payload(payload: Any) -> List[Dict[str, Any]]:
    """Normalize common API payload shapes into a list of listing dicts."""
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]

    if isinstance(payload, dict):
        for key in ("results", "listings", "data", "properties", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]

    return []


def fetch_listings(args: argparse.Namespace) -> List[Dict[str, Any]]:
    headers = {"Accept": "application/json"}
    if args.api_key:
        headers[args.api_key_header] = args.api_key

    all_listings: List[Dict[str, Any]] = []

    for page in range(1, args.pages + 1):
        params = build_query_params(args, page)
        resp = requests.get(args.base_url, headers=headers, params=params, timeout=args.timeout)
        resp.raise_for_status()

        payload = resp.json()
        current = normalize_payload(payload)
        if not current:
            break

        all_listings.extend(current)

    return all_listings


def flatten_record(record: Dict[str, Any], parent_key: str = "") -> Dict[str, Any]:
    flattened: Dict[str, Any] = {}
    for key, value in record.items():
        full_key = f"{parent_key}.{key}" if parent_key else str(key)
        if isinstance(value, dict):
            flattened.update(flatten_record(value, full_key))
        elif isinstance(value, list):
            flattened[full_key] = json.dumps(value, ensure_ascii=False)
        else:
            flattened[full_key] = value
    return flattened


def write_json(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    flat_rows = [flatten_record(row) for row in rows]
    fieldnames = sorted({k for row in flat_rows for k in row.keys()})

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flat_rows)


def main() -> int:
    args = parse_args()
    output_path = Path(args.out)

    try:
        listings = fetch_listings(args)
    except requests.HTTPError as exc:
        print(f"HTTP error while pulling listings: {exc}", file=sys.stderr)
        return 1
    except requests.RequestException as exc:
        print(f"Request failure while pulling listings: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Invalid JSON payload: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        write_json(output_path, listings)
    else:
        write_csv(output_path, listings)

    print(f"Saved {len(listings)} listing(s) to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
