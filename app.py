import argparse
import csv
from db import init_db, add_item, adjust_qty, search, all_items

def print_items(rows):
    if not rows:
        print("No items found.")
        return
    print(f"{'SKU':<12} {'NAME':<22} {'QTY':<6} {'LOC':<10} {'UPDATED'}")
    print("-" * 75)
    for r in rows:
        print(f"{r['sku']:<12} {r['name'][:22]:<22} {r['qty']:<6} {r['location'][:10]:<10} {r['updated_at']}")

def export_csv(path):
    rows = all_items()
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sku", "name", "qty", "location", "updated_at"])
        for r in rows:
            w.writerow([r["sku"], r["name"], r["qty"], r["location"], r["updated_at"]])
    print(f"Exported {len(rows)} items to {path}")

def main():
    init_db()

    parser = argparse.ArgumentParser(prog="inventory", description="Inventory Management Application")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("--sku", required=True)
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--qty", type=int, default=0)
    p_add.add_argument("--location", default="N/A")

    p_adj = sub.add_parser("adjust")
    p_adj.add_argument("--sku", required=True)
    p_adj.add_argument("--delta", type=int, required=True)

    p_search = sub.add_parser("search")
    p_search.add_argument("--q", required=True)

    p_list = sub.add_parser("list")

    p_export = sub.add_parser("export")
    p_export.add_argument("--out", default="inventory_report.csv")

    args = parser.parse_args()

    if args.cmd == "add":
        add_item(args.sku, args.name, args.qty, args.location)
        print("Item added.")
    elif args.cmd == "adjust":
        changed = adjust_qty(args.sku, args.delta)
        print("Updated." if changed else "SKU not found.")
    elif args.cmd == "search":
        print_items(search(args.q))
    elif args.cmd == "list":
        print_items(all_items())
    elif args.cmd == "export":
        export_csv(args.out)

if __name__ == "__main__":
    main()
