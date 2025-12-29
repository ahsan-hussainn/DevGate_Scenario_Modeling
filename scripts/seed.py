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
        ON CONFLICT (region_name) DO NOTHING;
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
        ON CONFLICT (product_name) DO NOTHING;
        """,
        products
    )


def main():
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        seed_regions(cur)
        seed_products(cur)

        conn.commit()
        print("✅ Base data seeded successfully.")

    except Exception as e:
        if conn:
            conn.rollback()
        print("❌ Error while seeding base data:")
        print(e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    main()