# Databricks Asset Bundle (DAB) Setup Guide

## 🎯 Overview

This project uses **Databricks Declarative Automation Bundles (DAB)** for CI/CD deployment across multiple environments.

## 📁 Project Structure

```
prod-amazon-sales-project/
├── databricks.yml              # Main DAB configuration
├── resources/
│   └── jobs.yml                # Job definitions
├── notebooks/
│   ├── 01_data_ingestion.py
│   ├── 02_data_transformation.py
│   ├── 03_data_quality.py
│   ├── 04_analytics.py
│   └── adhoc_analysis.py
├── src/
│   ├── __init__.py
│   └── utils.py                # Utility functions
├── tests/
│   ├── __init__.py
│   └── test_utils.py           # Unit tests
├── .github/
│   └── workflows/
│       └── amazon.yml          # CI/CD workflow
└── requirements.txt
```

## 🔧 Configuration

### databricks.yml

The main configuration file defines:
- **Bundle name**: `prod-amazon-sales-project`
- **Target environments**: dev, qa, prod
- **Variables**: catalog, schema names per environment
- **Workspace root**: `~/.bundle/${bundle.name}/${bundle.target}`

### Target Environments

| Environment | Mode | Cluster Config | Availability |
|-------------|------|----------------|--------------|
| **dev** | development | 1 worker, SPOT | Cost-optimized |
| **qa** | production | 2 workers, ON_DEMAND | Stable testing |
| **prod** | production | 2-8 workers (autoscale), ON_DEMAND | Production-ready |

### Variables by Environment

| Variable | dev | qa | prod |
|----------|-----|-----|------|
| `catalog` | dev_catalog | qa_catalog | prod_catalog |
| `schema` | amazon_sales_dev | amazon_sales_qa | amazon_sales_prod |

## 🚀 GitHub Actions Workflow

### Branch Strategy

```
dev branch  → Deploys to DEV environment
qa branch   → Deploys to QA environment
main branch → Deploys to PROD environment
```

### Required GitHub Secrets

Set these secrets in your GitHub repository settings:

1. **DATABRICKS_HOST**
   - Format: `https://your-workspace.cloud.databricks.com`
   - Get from: Workspace URL

2. **DATABRICKS_TOKEN**
   - Format: `dapi1234567890abcdef...`
   - Generate from: User Settings → Access Tokens

### Setting GitHub Secrets

Navigate to your repository on GitHub:
1. Go to: Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add DATABRICKS_HOST with your workspace URL
4. Add DATABRICKS_TOKEN with your access token

### Workflow Stages

1. **Validate**: Checks bundle configuration
2. **Deploy**: Deploys to target environment based on branch

## 💻 Local Development

### Prerequisites

```bash
# Install Databricks CLI
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

# Verify installation
databricks --version
```

### Authentication

```bash
# Set environment variables
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi1234567890abcdef..."
```

### Local Commands

```bash
# Validate bundle
databricks bundle validate -t dev

# Deploy to dev
databricks bundle deploy -t dev

# Run a job
databricks bundle run amazon_sales_etl_pipeline -t dev
```

## 📋 Jobs Defined

### 1. Amazon Sales ETL Pipeline

**Schedule**: Daily at 2 AM UTC

**Tasks**:
1. `ingest_raw_data` - Ingest raw data from sources
2. `transform_data` - Transform and clean data
3. `quality_checks` - Run data quality validations
4. `generate_analytics` - Generate analytics and reports

**Parameters**:
- `catalog`: Target catalog name
- `schema`: Target schema name
- `env`: Environment (dev/qa/prod)

### 2. Amazon Sales Ad-hoc Processing

**Schedule**: Manual trigger only

**Purpose**: Ad-hoc analysis and exploration

## 🔄 Deployment Workflow

### Development Cycle

```bash
# 1. Make changes locally
vim notebooks/01_data_ingestion.py

# 2. Validate bundle
databricks bundle validate -t dev

# 3. Deploy to dev
databricks bundle deploy -t dev

# 4. Test the job
databricks bundle run amazon_sales_etl_pipeline -t dev

# 5. Commit and push
git add .
git commit -m "Updated data ingestion logic"
git push origin dev
```

### Promotion Path

```
Local Dev → dev branch → qa branch → main branch
            ↓            ↓            ↓
          DEV Env     QA Env      PROD Env
```

## 🧪 Testing

```bash
# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## 📊 Monitoring

### Databricks UI

1. Navigate to **Workflows** in Databricks UI
2. Find jobs prefixed with your environment:
   - `Amazon Sales ETL Pipeline - dev`
   - `Amazon Sales ETL Pipeline - qa`
   - `Amazon Sales ETL Pipeline - prod`

## 🔒 Security Best Practices

1. **Never commit secrets** to version control
2. **Use GitHub Environments** for approval gates (especially prod)
3. **Rotate tokens** regularly
4. **Use service principals** for production (recommended)
5. **Enable audit logs** in Databricks workspace

## 🐛 Troubleshooting

### Error: "databricks.yml not found"

**Solution**: Ensure you're in the project root directory

```bash
cd prod-amazon-sales-project
ls databricks.yml  # Should exist
```

### Error: "Invalid authentication"

**Solution**: Check your credentials

```bash
echo $DATABRICKS_HOST
echo $DATABRICKS_TOKEN  # Should start with 'dapi'
```

### Error: "Notebook not found"

**Solution**: Ensure notebooks are committed to Git

```bash
git add notebooks/
git commit -m "Add notebooks"
git push
```

## 📚 Additional Resources

- [Databricks Asset Bundles Documentation](https://docs.databricks.com/dev-tools/bundles/)
- [Databricks CLI Reference](https://docs.databricks.com/dev-tools/cli/)
- [GitHub Actions for Databricks](https://github.com/databricks/setup-cli)

## 🤝 Contributing

1. Create a feature branch from `dev`
2. Make your changes
3. Test locally with `databricks bundle deploy -t dev`
4. Create a pull request to `dev` branch
5. After approval, merge and deploy

## 📝 Notes

- The bundle uses **token authentication** (DATABRICKS_HOST + DATABRICKS_TOKEN)
- Job clusters are **ephemeral** - created on demand, terminated after completion
- All resources are tagged with `managed-by: dab` for tracking
- Bundle mode `development` (dev) creates isolated resources
- Bundle mode `production` (qa, prod) enforces production safeguards
