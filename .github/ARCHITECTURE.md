# Architecture Overview

## Single Workspace, Multi-Catalog Design

```
┌─────────────────────────────────────────────────────────────┐
│         Databricks Workspace (Single Instance)              │
│  https://your-workspace.azuredatabricks.net                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
  ┌──────────┐          ┌──────────┐          ┌──────────┐
  │   DEV    │          │    QA    │          │   PROD   │
  │ Catalog  │          │ Catalog  │          │ Catalog  │
  └──────────┘          └──────────┘          └──────────┘
      │                     │                     │
      │                     │                     │
 dev_amazon            qa_amazon            prod_amazon
      │                     │                     │
      └─────────────────────┴─────────────────────┘
                              │
                              ▼
                    Unity Catalog Tables
            (bronze, silver, gold schemas)
```

## Catalog Structure

Each environment has its own isolated catalog:

### dev_amazon
```
dev_amazon
├── bronze
│   ├── sales_data
│   └── customer_data
├── silver
│   ├── cleaned_sales
│   └── enriched_customers
└── gold
    ├── daily_revenue
    └── customer_metrics
```

### qa_amazon
```
qa_amazon
├── bronze
├── silver
└── gold
```

### prod_amazon
```
prod_amazon
├── bronze
├── silver
└── gold
```

## Deployment Flow

```
GitHub Repository
       │
       ├─ develop branch → Deploy to dev_amazon
       │                   (DEV Service Principal)
       │
       ├─ develop branch → Deploy to qa_amazon
       │                   (QA Service Principal)
       │
       └─ main branch    → Deploy to prod_amazon
                           (PROD Service Principal)
```

## Service Principals

| Service Principal | Access | Catalog | Purpose |
|------------------|--------|---------|---------|
| github-actions-dev | READ/WRITE | dev_amazon | Development deployments |
| github-actions-qa | READ/WRITE | qa_amazon | QA testing |
| github-actions-prod | READ/WRITE | prod_amazon | Production deployments |

## Benefits

✅ **Cost Efficiency** - Single workspace reduces infrastructure costs
✅ **Simplified Management** - One workspace to manage and monitor
✅ **Data Isolation** - Catalogs provide complete data separation
✅ **Security** - Service principals ensure environment isolation
✅ **Easy Promotion** - Same workspace, different catalog references

## GitHub Secrets Required

1. `DATABRICKS_HOST` - Single workspace URL (shared)
2. `DATABRICKS_DEV_CLIENT_ID` / `DATABRICKS_DEV_CLIENT_SECRET`
3. `DATABRICKS_QA_CLIENT_ID` / `DATABRICKS_QA_CLIENT_SECRET`
4. `DATABRICKS_PROD_CLIENT_ID` / `DATABRICKS_PROD_CLIENT_SECRET`

**Total: 7 secrets** (vs 9 in multi-workspace setup)

## Notebook Best Practices

Always use the catalog parameter:

```python
# Get catalog from job parameter
catalog = dbutils.widgets.get("catalog")

# Set as default
spark.sql(f"USE CATALOG {catalog}")

# Use in queries
df = spark.table(f"{catalog}.bronze.sales_data")
```

## Job Configuration

Jobs use the `{{catalog}}` placeholder which gets replaced during deployment:

```json
{
  "notebook_task": {
    "notebook_path": "/Workspace/Users/deployment/notebooks/etl",
    "base_parameters": {
      "catalog": "{{catalog}}"
    }
  }
}
```

The CI/CD pipeline automatically substitutes:
* DEV deployment: `{{catalog}}` → `dev_amazon`
* QA deployment: `{{catalog}}` → `qa_amazon`
* PROD deployment: `{{catalog}}` → `prod_amazon`
