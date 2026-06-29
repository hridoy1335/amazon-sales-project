# 🚀 Quick Start Guide

## What Was Fixed

### ✅ Created Files

1. **databricks.yml** - Main DAB configuration
2. **resources/jobs.yml** - Job definitions  
3. **notebooks/** - Placeholder notebooks for ETL pipeline
4. **src/** - Python source code utilities
5. **tests/** - Unit tests
6. **DAB_SETUP.md** - Comprehensive setup documentation

### ✅ Updated Files

1. **.github/workflows/amazon.yml** - Enhanced with:
   - Bundle structure verification
   - Proper authentication using DATABRICKS_HOST and DATABRICKS_TOKEN
   - Conditional validation based on branch
   - Improved deployment messages

## Project Structure

```
prod-amazon-sales-project/
├── databricks.yml              ← Main DAB config
├── resources/
│   └── jobs.yml                ← Job definitions
├── notebooks/
│   ├── 01_data_ingestion.py
│   └── 02_data_transformation.py
├── src/
│   ├── __init__.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_utils.py
└── .github/
    └── workflows/
        └── amazon.yml          ← CI/CD workflow
```

## GitHub Secrets Setup

Before pushing, set these secrets in GitHub:

1. Go to: **Settings → Secrets and variables → Actions**
2. Add two repository secrets:

   * **DATABRICKS_HOST**
     - Value: `https://your-workspace.cloud.databricks.com`
   
   * **DATABRICKS_TOKEN**
     - Value: `dapi1234567890abcdef...`
     - Generate from: User Settings → Access Tokens

## Deployment Flow

```
dev branch  → GitHub Actions → DEV environment
qa branch   → GitHub Actions → QA environment  
main branch → GitHub Actions → PROD environment
```

## Test Locally

```bash
# 1. Set credentials
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi1234567890abcdef..."

# 2. Validate
databricks bundle validate -t dev

# 3. Deploy
databricks bundle deploy -t dev

# 4. Run job
databricks bundle run amazon_sales_etl_pipeline -t dev
```

## Push to GitHub

```bash
# Add all files
git add .

# Commit
git commit -m "Add Databricks Asset Bundle configuration"

# Push to dev branch
git push origin dev
```

The GitHub Actions workflow will automatically:
1. ✅ Validate the bundle
2. ✅ Deploy to DEV environment
3. ✅ Make jobs available in Databricks UI

## What Happens in Databricks

After deployment, you'll see in Databricks UI:

* **Workflows** → Job: "Amazon Sales ETL Pipeline - dev"
* **Workspace** → `~/.bundle/prod-amazon-sales-project/dev/`

## Customization

### Update Job Schedule

Edit `resources/jobs.yml`:

```yaml
schedule:
  quartz_cron_expression: "0 0 8 ? * * *"  # 8 AM daily
  timezone_id: "America/New_York"
```

### Add More Notebooks

Add new tasks in `resources/jobs.yml`:

```yaml
- task_key: new_task
  depends_on:
    - task_key: previous_task
  job_cluster_key: main
  notebook_task:
    notebook_path: ./notebooks/new_notebook
    base_parameters:
      catalog: ${var.catalog}
      schema: ${var.schema}
```

### Change Cluster Size

Update `databricks.yml` target settings:

```yaml
targets:
  dev:
    resources:
      jobs:
        amazon_sales_*:
          job_clusters:
            - job_cluster_key: main
              new_cluster:
                num_workers: 4  # Increase workers
```

## Troubleshooting

### "databricks.yml not found"

Ensure you're in the project root:
```bash
cd prod-amazon-sales-project
pwd  # Should show the project root
```

### GitHub Actions Failing

Check:
1. ✅ Secrets are set correctly
2. ✅ Token hasn't expired
3. ✅ Workspace URL is correct (no trailing slash)

### Local Validation Fails

```bash
# Re-authenticate
databricks configure --token

# Then try again
databricks bundle validate -t dev
```

## Next Steps

1. ✅ Commit and push files
2. ✅ Set GitHub secrets
3. ✅ Customize notebooks for your use case
4. ✅ Update catalog/schema names in databricks.yml
5. ✅ Test deployment to dev
6. ✅ Promote to qa → main when ready

## Documentation

* **DAB_SETUP.md** - Comprehensive setup guide
* **QUICK_START.md** - This file
* **.github/workflows/amazon.yml** - CI/CD workflow

## Support

* [Databricks Asset Bundles Docs](https://docs.databricks.com/dev-tools/bundles/)
* [Databricks CLI Docs](https://docs.databricks.com/dev-tools/cli/)

---

**Ready to deploy!** 🎉
