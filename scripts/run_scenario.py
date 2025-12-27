from db import get_connection


def create_scenario(cur, name, description):
    cur.execute(
        """
        INSERT INTO scenario (scenario_name, description)
        VALUES (%s, %s)
        RETURNING scenario_id;
        """,
        (name, description)
    )
    return cur.fetchone()[0]


def insert_scenario_parameters(cur, scenario_id, params):
    """
    params: list of tuples
    (product_id, population_override, demand_factor_override, multiplier_override)
    """
    cur.executemany(
        """
        INSERT INTO scenario_parameters (
            scenario_id,
            product_id,
            population_override,
            demand_factor_override,
            multiplier_override
        )
        VALUES (%s, %s, %s, %s, %s);
        """,
        [(scenario_id, *p) for p in params]
    )


def run_calculations(cur, scenario_id):
    cur.execute(
        """
        INSERT INTO scenario_results (
            scenario_id,
            region_id,
            product_id,
            effective_population,
            calculated_demand,
            calculated_units
        )
        SELECT
            s.scenario_id,
            r.region_id,
            p.product_id,
            COALESCE(sp.population_override, r.base_population) AS effective_population,
            COALESCE(sp.demand_factor_override, p.base_demand_factor)
                * COALESCE(sp.population_override, r.base_population) AS calculated_demand,
            COALESCE(sp.demand_factor_override, p.base_demand_factor)
                * COALESCE(sp.population_override, r.base_population)
                * COALESCE(sp.multiplier_override, p.base_multiplier) AS calculated_units
        FROM scenario s
        JOIN region r ON 1 = 1
        JOIN product p ON 1 = 1
        LEFT JOIN scenario_parameters sp
            ON sp.scenario_id = s.scenario_id
           AND sp.product_id = p.product_id
        WHERE s.scenario_id = %s;
        """,
        (scenario_id,)
    )


def main():
    conn = get_connection()
    cur = conn.cursor()

    # ---- Scenario metadata ----
    scenario_name = "Population +10%, Demand -5%"
    description = "What-if analysis: increased population, reduced demand"

    scenario_id = create_scenario(cur, scenario_name, description)

    # ---- Scenario parameters (per product) ----
    scenario_params = [
        # product_id, population_override, demand_factor_override, multiplier_override
        (1, None, 0.0475, None),  # Product A
        (2, None, 0.0285, None),  # Product B
    ]

    insert_scenario_parameters(cur, scenario_id, scenario_params)

    # ---- Run calculations ----
    run_calculations(cur, scenario_id)

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Scenario {scenario_id} executed successfully.")


if __name__ == "__main__":
    main()
