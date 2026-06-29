# GitHub Actions Workflow Guide

## ✅ Automatic Deployment Configuration

This workflow automatically deploys to the correct environment based on the branch you push to.

## Branch → Environment Mapping

| Branch | Environment | Action |
|--------|-------------|--------|
| `dev` | DEV | Automatic deployment on push |
| `qa` | QA | Automatic deployment on push |
| `main` | PROD | Automatic deployment on push |

## How It Works

### 1. Push to DEV
```bash
git checkout dev
git add .
git commit -m "Add new feature"
git push origin dev
```
**Result:** Automatically deploys to DEV environment ✅

### 2. Push to QA
```bash
git checkout qa
git merge dev
git push origin qa
```
**Result:** Automatically deploys to QA environment ✅

### 3. Push to PROD
```bash
git checkout main
git merge qa
git push origin main
```
**Result:** Automatically deploys to PROD environment ✅

## Deployment Flow

```
Code Change
    ↓
Push to Branch
    ↓
Validate (lint + test)
    ↓
Deploy to Environment
    ✅ Done
```

## Required GitHub Secrets

Configure these in: **Settings → Secrets and variables → Actions**

| Secret Name | Description |
|------------|-------------|
| `DATABRICKS_HOST` | Workspace URL (shared) |
| `DATABRICKS_DEV_TOKEN` | PAT for DEV environment |
| `DATABRICKS_QA_TOKEN` | PAT for QA environment |
| `DATABRICKS_PROD_TOKEN` | PAT for PROD environment |

## What Gets Deployed

* **Notebooks** → `/Workspace/Users/deployment/{env}/notebooks`
* **Jobs** → Created/updated from `./jobs/*.json`

## Pull Request Behavior

When you create a PR:
```bash
git checkout -b feature/new-feature
git push origin feature/new-feature
# Create PR to dev, qa, or main
```

**Result:** Only runs validation (lint + test), NO deployment ✅

## Development Workflow Example

```bash
# 1. Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/new-dashboard

# 2. Make changes
# ... edit files ...

# 3. Test locally
pytest tests/

# 4. Push to dev
git checkout dev
git merge feature/new-dashboard
git push origin dev
# ✅ Auto-deploys to DEV

# 5. Test in DEV, then promote to QA
git checkout qa
git merge dev
git push origin qa
# ✅ Auto-deploys to QA

# 6. Test in QA, then promote to PROD
git checkout main
git merge qa
git push origin main
# ✅ Auto-deploys to PROD
```

## Key Features

✅ **Fully automatic** - No manual workflow dispatch needed
✅ **Branch-based** - Push to branch = deploy to environment
✅ **Parallel environments** - Each branch deploys independently
✅ **Validation first** - Linting and testing before deployment
✅ **PAT authentication** - Simple token-based auth
✅ **PR validation only** - Pull requests don't deploy

## Monitoring Deployments

1. Go to **Actions** tab in GitHub repository
2. See workflow runs for each push
3. Click on a run to see detailed logs
4. Each environment deployment shown separately

## Troubleshooting

### Deployment didn't trigger
* Verify you pushed to `dev`, `qa`, or `main` branch
* Check Actions tab for workflow run
* Ensure all secrets are configured

### Authentication failed
* Verify `DATABRICKS_HOST` is correct
* Check that environment token exists (`DATABRICKS_DEV_TOKEN`, etc.)
* Ensure token hasn't expired

### Job deployment failed
* Check that `./jobs/` directory exists with valid JSON files
* Verify job JSON syntax is correct
* Check logs in Actions tab for error details

## No Manual Intervention Required

This workflow is designed to be fully automatic:
* ✅ Push to dev → deploys to DEV
* ✅ Push to qa → deploys to QA
* ✅ Push to main → deploys to PROD
* ❌ No manual clicks needed
* ❌ No workflow dispatch
* ❌ No approval gates (add via GitHub Environments if needed)
