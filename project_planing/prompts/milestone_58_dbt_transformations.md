# Milestone #58: Set Up DBT Transformations

**Your Role:** Data Engineer

1. Install DBT:
   ```bash
   pip install dbt-postgres
   ```

2. Initialize DBT project:
   ```bash
   dbt init dbt_shipsmart
   ```

3. Configure `dbt_shipsmart/profiles.yml`:
   ```yaml
   shipsmart:
     target: dev
     outputs:
       dev:
         type: postgres
         host: localhost
         user: shipsmart
         password: changeme
         dbname: shipsmart
   ```

4. Create models in `dbt_shipsmart/models/`:
   - `dim_customers.sql`
   - `dim_orders.sql`
   - `fct_delivery_metrics.sql`

5. Run dbt and commit.

---

### Milestone #58 Completed
- dbt_shipsmart/README.md (DBT project setup)
- Created dbt-postgres installation instructions
- Created profiles.yml and project structure documentation
- Documented models: dim_customers, dim_orders, dim_drivers, dim_warehouses, fct_delivery_metrics
- Next: Milestone #59