from db import get_connection


def seed_regions(cur):
    regions = [
        ("North", 1_000_000),
        ("South", 750_000),
        ("East", 500_000)
    ]

    cur.executemany(
        """
        INSERT INTO region (region_name, base_population)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING;
        """,
        regions
    )


def seed_products(cur):
    products = [
        ("Product A", 0.05, 1.2),
        ("Product B", 0.03, 1.5)
    ]

    cur.executemany(
        """
        INSERT INTO product (product_name, base_demand_factor, base_multiplier)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING;
        """,
        products
    )


def main():
    conn = get_connection()
    cur = conn.cursor()

    seed_regions(cur)
    seed_products(cur)

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Base data seeded successfully.")


if __name__ == "__main__":
    main()