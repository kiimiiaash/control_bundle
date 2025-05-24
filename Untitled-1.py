import math
import pandas as pd



inventory_df = pd.read_excel("/Users/kimiash/Desktop/control_bundle/inventory.xlsx")
bundle_df = pd.read_excel("/Users/kimiash/Desktop/control_bundle/bundle_items.xlsx")
bundle_warehouses_df = pd.read_excel("/Users/kimiash/Desktop/control_bundle/bundle_warehouses.xlsx")


# Extract list of warehouses
warehouses = inventory_df.columns[1:]

# Convert inventory to dict for easier access
inventory_data = {}
for _, row in inventory_df.iterrows():
    pid = row["product_id"]
    inventory_data[pid] = row.drop("product_id").to_dict()

# Final result holder
all_results = []

# For each warehouse
for warehouse in warehouses:
    # Get only bundles active in this warehouse
    active_bundles = bundle_warehouses_df[bundle_warehouses_df["warehouse"] == warehouse]["bundle_id"].unique()

    current_stock = {pid: stock.get(warehouse, 0) for pid, stock in inventory_data.items()}
    bundle_counts = {bundle_id: 0 for bundle_id in active_bundles}

    while True:
        made_any = False

        for bundle_id in active_bundles:
            items = bundle_df[bundle_df["bundle_id"] == bundle_id]
            can_build = True

            for _, row in items.iterrows():
                pid = row["product_id"]
                ratio = row["ratio"]
                if current_stock.get(pid, 0) < ratio:
                    can_build = False
                    break

            if can_build:
                made_any = True
                bundle_counts[bundle_id] += 1
                for _, row in items.iterrows():
                    pid = row["product_id"]
                    ratio = row["ratio"]
                    current_stock[pid] -= ratio

        if not made_any:
            break

    # Save result
    for bundle_id, count in bundle_counts.items():
        all_results.append({
            "warehouse": warehouse,
            "bundle_id": bundle_id,
            "max_bundle_possible": count
        })
# Save to Excel
result_df = pd.DataFrame(all_results)
result_df.to_excel("fair_bundle_distribution.xlsx", index=False)

print("🎉 فایل fair_bundle_distribution.xlsx ساخته شد! تقسیم منصفانه انجام شد ✨")