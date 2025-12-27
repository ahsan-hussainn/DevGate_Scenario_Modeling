-- REGION

CREATE TABLE region (
    region_id SERIAL PRIMARY KEY,
    region_name TEXT NOT NULL,
    base_population INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PRODUCT

CREATE TABLE product (
    product_id SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    base_demand_factor NUMERIC(10,4) NOT NULL,
    base_multiplier NUMERIC(10,4) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SCENARIO

CREATE TABLE scenario (
    scenario_id SERIAL PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SCENARIO PARAMETERS

CREATE TABLE scenario_parameters (
    param_id SERIAL PRIMARY KEY,
    scenario_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    population_override INTEGER,
    demand_factor_override NUMERIC(10,4),
    multiplier_override NUMERIC(10,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_scenario
        FOREIGN KEY (scenario_id) REFERENCES scenario (scenario_id),
    CONSTRAINT fk_product
        FOREIGN KEY (product_id) REFERENCES product (product_id),
    CONSTRAINT uq_scenario_product
        UNIQUE (scenario_id, product_id)
);

-- SCENARIO RESULTS

CREATE TABLE scenario_results (
    result_id SERIAL PRIMARY KEY,
    scenario_id INTEGER NOT NULL,
    region_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    effective_population INTEGER NOT NULL,
    calculated_demand NUMERIC(14,4) NOT NULL,
    calculated_units NUMERIC(14,4) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sr_scenario
        FOREIGN KEY (scenario_id) REFERENCES scenario (scenario_id),
    CONSTRAINT fk_sr_region
        FOREIGN KEY (region_id) REFERENCES region (region_id),
    CONSTRAINT fk_sr_product
        FOREIGN KEY (product_id) REFERENCES product (product_id),
    CONSTRAINT uq_result_grain
        UNIQUE (scenario_id, region_id, product_id)
);