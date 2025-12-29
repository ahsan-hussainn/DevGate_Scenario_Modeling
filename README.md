# DP – Scenario Modeling (Python + Supabase)

This repository demonstrates a **simple, production-oriented scenario modeling solution** using open-source technologies.  
The objective is to show how **predictive scenarios can be evaluated by changing assumptions (inputs) without reloading base data**, which is a common requirement in real-world forecasting and planning systems.

---
## Technologies Used
- **PostgreSQL (Supabase)** – relational database
- **Python** – data loading and scenario execution
- **psycopg2** – PostgreSQL connectivity
- **GitHub** – version control

## Repository Structure
```text
DP_Scenario_Modeling/
├── ddl/
│   └── schema.sql          # Database schema (tables, PKs, FKs)
│
├── scripts/
│   ├── db.py               # Database connection logic
│   ├── seed.py             # Load base/master data
│   └── run_scenario.py     # Execute scenario calculations
│
├── erd/
│   └── erd.png             # Data model diagram
│
├── README.md
└── requirements.txt
```


---

### Scripts & Execution Order

1. **`db.py`**  
   Centralizes database connection logic and is reused by all scripts.

2. **`seed.py`**  
   Loads **base/master data** such as regions and products.  
   This script is intended to be run **once or rarely**.

3. **`run_scenario.py`**  
   Creates a new scenario, applies scenario-specific inputs, runs calculations, and persists results.

**Execution order:**
```bash
python seed.py
python run_scenario.py
```
---
### 1. Entity Relationship Diagram (ERD)
<img width="770" height="675" alt="data_model_ERD" src="https://github.com/user-attachments/assets/93c8f75d-9190-49d6-b5e0-b554c9857bc2" />
---
### 2. Data Model
The model is designed around three independent dimensions:
- **Region** – where demand occurs
- **Product** – what is being demanded
- **Scenario** – under which assumptions calculations are performed

## Base Tables
- **region** → stores base population per region
- **product** → stores base demand factor and multiplier per product

These tables represent stable, slow-changing master data.

## Scenario Tables
- **scenario** → scenario metadata (one row per what-if run)
- **scenario_parameters** → scenario-specific input overrides
- **scenario_results** → precomputed outputs per scenario

The effective grain of the model is:
Scenario × Region × Product
This allows multiple scenarios to coexist without overwriting historical data.
---

### 3. Handling Scenario Changes (Key Design Explanation)
**Problem Statement**
Input parameters such as population, demand factor, and multiplier can change frequently (e.g., “What if population increases by 10%?”).
The system must recompute predictions without reloading base data.

## Impact on the Data Model
Changes in inputs do not affect base tables:
- **region**
- **product**

Instead, all variability is isolated into:
- **scenario**
- **scenario_parameters**

Each new set of assumptions results in a new scenario, ensuring:
- **no data overwrite**
- **full traceability**
- **easy comparison across scenarios**

### Precompute vs Recompute
**Stored (Precomputed)**
Scenario outputs are persisted in scenario_results, including:
- effective population
- calculated demand
- calculated units

**Storing results enables**:
- fast reads for downstream applications
- reproducibility
- historical analysis

**Recomputed**
- Calculations are rerun only when a new scenario is created
- Base data is reused and never reloaded

## Scenario Representation & Persistence
Each scenario is persisted as:
1. A record in scenario (metadata)
2. One or more records in scenario_parameters (input overrides)
3. Multiple records in scenario_results (computed outputs)

This append-only design supports:
- auditability
- scenario comparison
- downstream predictive consumption
---
### 4. Table Output Snapshots

**Scenario**
<img width="1541" height="630" alt="scenarios" src="https://github.com/user-attachments/assets/ed8ce907-3409-41c7-bff9-e020bc114f49" />
**Scenario Parameters**
<img width="1542" height="675" alt="scenario_params" src="https://github.com/user-attachments/assets/e34ba3df-e8fa-4bc9-99bf-142a58cb7ba8" />
**Scenario Results**
<img width="1530" height="852" alt="scenario_results" src="https://github.com/user-attachments/assets/319ea2fd-2026-45f5-8db6-ddba01770b2e" />

## Configuration & Error Handling
- Database credentials are managed using environment variables via `python-dotenv`
- A `.env` file is used locally and excluded from version control
- Scripts include basic transaction handling (`commit / rollback`) to prevent partial writes
- Base data tables enforce uniqueness constraints to ensure idempotent seeding
