# GitHub Actions CI/CD Setup Guide

This guide explains how to configure the GitHub Actions workflow for Databricks deployment across dev, qa, and prod environments.

## Prerequisites

* Databricks workspace for each environment (dev, qa, prod)
* Service Principal created in each Databricks workspace
* GitHub repository with admin access

## Step 1: Create Databricks Service Principals

For each environment (dev, qa, prod), create a service principal:

### Using Databricks CLI:
```bash
# Login to Databricks
databricks auth login --host https://your-workspace.cloud.databricks.com

# Create service principal
databricks service-principals create --display-name "github-actions-dev"

# Note the application_id (client_id) from the output
```

### Using Databricks UI:
1. Go to **Settings** → **Identity and Access**
2. Click **Service Principals** tab
3. Click **Add Service Principal**
4. Enter name: `github-actions-dev` (or qa/prod)
5. Click **Add**
6. Copy the **Application ID** (this is your CLIENT_ID)

### Generate Client Secret:
1. Click on the service principal you just created
2. Go to **OAuth secrets** tab
3. Click **Generate secret**
4. Copy the **Secret** value (you won't see it again!)
5. Save both CLIENT_ID and CLIENT_SECRET securely

### Grant Permissions:
```bash
# Grant workspace access
databricks permissions update workspace /Workspace/Users/deployment/dev \
  --service-principal <application-id> \
  --permission-level CAN_MANAGE

# Grant cluster create permission (if needed)
databricks permissions update cluster-policies <policy-id> \
  --service-principal <application-id> \
  --permission-level CAN_USE
```

## Step 2: Configure GitHub Secrets

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**

### Add Repository Secrets:

#### DEV Environment:
* `DATABRICKS_DEV_HOST`: `https://your-workspace.cloud.databricks.com`
* `DATABRICKS_DEV_CLIENT_ID`: Service principal application ID for dev
* `DATABRICKS_DEV_CLIENT_SECRET`: Service principal secret for dev

#### QA Environment:
* `DATABRICKS_QA_HOST`: `https://your-workspace.cloud.databricks.com`
* `DATABRICKS_QA_CLIENT_ID`: Service principal application ID for qa
* `DATABRICKS_QA_CLIENT_SECRET`: Service principal secret for qa

#### PROD Environment:
* `DATABRICKS_PROD_HOST`: `https://your-workspace.cloud.databricks.com`
* `DATABRICKS_PROD_CLIENT_ID`: Service principal application ID for prod
* `DATABRICKS_PROD_CLIENT_SECRET`: Service principal secret for prod

## Step 3: Configure GitHub Environments (Optional but Recommended)

GitHub Environments allow you to add protection rules and approval gates:

1. Go to **Settings** → **Environments**
2. Create three environments: `dev`, `qa`, `prod`

### For Production Environment:
* Click **prod** environment
* Check **Required reviewers**
* Add team members who should approve prod deployments
* Set **Wait timer** if you want a delay before deployment
* Add **Branch protection** to restrict to `main` branch only

## Step 4: Project Structure

Organize your repository as follows:

```
prod-amazon-sales-project/
├── .github/
│   ├── workflows/
│   │   └── blank.yml          # Main CI/CD workflow
│   └── SETUP.md               # This file
├── notebooks/
│   ├── bronze/
│   │   └── ingestion.py
│   ├── silver/
│   │   └── transformations.py
│   └── gold/
│       └── aggregations.py
├── jobs/
│   ├── data-ingestion-job.json
│   ├── transformation-job.json
│   └── reporting-job.json
├── tests/
│   ├── test_transformations.py
│   └── test_aggregations.py
├── requirements.txt
└── README.md
```

## Step 5: Create Job Definition Files

Example job definition (`jobs/data-ingestion-job.json`):

```json
{
  "name": "data-ingestion-job",
  "tasks": [
    {
      "task_key": "ingest_data",
      "notebook_task": {
        "notebook_path": "/Workspace/Users/deployment/notebooks/bronze/ingestion",
        "base_parameters": {}
      },
      "new_cluster": {
        "spark_version": "13.3.x-scala2.12",
        "node_type_id": "i3.xlarge",
        "num_workers": 2
      }
    }
  ],
  "schedule": {
    "quartz_cron_expression": "0 0 2 * * ?",
    "timezone_id": "America/New_York"
  }
}
```

## Step 6: Testing the Workflow

### Test DEV deployment:
1. Create a feature branch: `git checkout -b feature/test-deployment`
2. Make changes and push: `git push origin feature/test-deployment`
3. Merge to `develop` branch
4. Workflow will automatically deploy to DEV

### Test QA deployment:
* After successful DEV deployment, the workflow automatically promotes to QA
* Validate in QA environment

### Test PROD deployment:
1. Merge `develop` to `main` branch
2. If you configured environment protection, approve the deployment
3. Workflow deploys to PROD

### Manual deployment:
1. Go to **Actions** tab in GitHub
2. Select **Databricks CI/CD Pipeline** workflow
3. Click **Run workflow**
4. Select environment and branch
5. Click **Run workflow**

## Step 7: Monitoring and Troubleshooting

### View Workflow Runs:
* Go to **Actions** tab
* Click on a workflow run to see details
* Expand each job to see logs

### Common Issues:

**Authentication Failed:**
* Verify CLIENT_ID and CLIENT_SECRET are correct
* Ensure service principal has proper permissions
* Check that HOST URL is correct (include https://)

**Permission Denied:**
* Grant service principal workspace access
* Add to necessary groups
* Grant cluster creation permissions if needed

**Job Deployment Failed:**
* Verify job JSON syntax
* Check that referenced notebooks exist
* Ensure cluster configuration is valid

## Security Best Practices

1. **Use GitHub Environments** with approval gates for production
2. **Rotate secrets regularly** (every 90 days)
3. **Limit service principal permissions** to only what's needed
4. **Use branch protection rules** to prevent direct pushes to main
5. **Enable audit logging** in Databricks
6. **Review access regularly** and remove unused service principals

## Additional Resources

* [Databricks Service Principals Documentation](https://docs.databricks.com/administration-guide/users-groups/service-principals.html)
* [GitHub Actions Documentation](https://docs.github.com/en/actions)
* [Databricks CLI Reference](https://docs.databricks.com/dev-tools/cli/index.html)
