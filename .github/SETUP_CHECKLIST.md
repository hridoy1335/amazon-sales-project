# GitHub Actions Setup Checklist

## ✅ Workflow Status: FIXED & READY

The workflow is now **production-ready** with all issues fixed.

## Required GitHub Secrets (7 Total)

Configure these in: **GitHub Repository → Settings → Secrets and variables → Actions**

### 1. Workspace Connection (Shared)
- [ ] `DATABRICKS_HOST` - Your Databricks workspace URL
  - Example: `https://adb-1234567890123456.7.azuredatabricks.net`

### 2. DEV Environment
- [ ] `DATABRICKS_DEV_CLIENT_ID` - Dev service principal application ID
- [ ] `DATABRICKS_DEV_CLIENT_SECRET` - Dev service principal secret

### 3. QA Environment
- [ ] `DATABRICKS_QA_CLIENT_ID` - QA service principal application ID
- [ ] `DATABRICKS_QA_CLIENT_SECRET` - QA service principal secret

### 4. PROD Environment
- [ ] `DATABRICKS_PROD_CLIENT_ID` - Prod service principal application ID
- [ ] `DATABRICKS_PROD_CLIENT_SECRET` - Prod service principal secret

## Project Structure Required

```
prod-amazon-sales-project/
├── .github/
│   └── workflows/
│       └── blank.yml          ✅ Ready
├── notebooks/                  📁 Your notebooks here
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── jobs/                       📁 Job definitions (optional)
│   └── *.json
├── tests/                      📁 Tests (optional)
└── requirements.txt            📁 Dependencies (optional)
```

## Workflow Behavior

### Triggers

| Branch | Action | Result |
|--------|--------|--------|
| `develop` | Push | Deploy to DEV → QA |
| `main` | Push | Deploy to DEV → QA → PROD |
| Any | Pull Request | Validate only (lint + test) |
| Manual | Workflow Dispatch | Deploy to selected environment |

### Deployment Flow

```
Code Push
    ↓
Validate (lint + pytest)
    ↓
Deploy to DEV
    ↓
Deploy to QA
    ↓
Deploy to PROD (main branch only)
```

### What Gets Deployed

1. **Notebooks** → `/Workspace/Users/deployment/{env}/notebooks`
2. **Jobs** → Creates/updates from `./jobs/*.json` files

## Testing the Workflow

### Step 1: Test Validation
```bash
git checkout -b feature/test
git push origin feature/test
# Creates a pull request → Runs validation only
```

### Step 2: Test DEV/QA Deployment
```bash
git checkout develop
git merge feature/test
git push origin develop
# Deploys to DEV → QA automatically
```

### Step 3: Test PROD Deployment
```bash
git checkout main
git merge develop
git push origin main
# Deploys to DEV → QA → PROD
```

### Manual Deployment
1. Go to **Actions** tab in GitHub
2. Select **Databricks CI/CD** workflow
3. Click **Run workflow**
4. Select environment (dev/qa/prod)
5. Click **Run workflow**

## Verification Commands

After setting up secrets, verify they're configured:

```bash
# List secrets (values hidden)
gh secret list

# Expected output:
# DATABRICKS_HOST
# DATABRICKS_DEV_CLIENT_ID
# DATABRICKS_DEV_CLIENT_SECRET
# DATABRICKS_QA_CLIENT_ID
# DATABRICKS_QA_CLIENT_SECRET
# DATABRICKS_PROD_CLIENT_ID
# DATABRICKS_PROD_CLIENT_SECRET
```

## Common Issues & Solutions

### ❌ Authentication Failed
**Cause:** Wrong CLIENT_ID or CLIENT_SECRET
**Fix:** Verify secrets in GitHub match service principal credentials

### ❌ Permission Denied
**Cause:** Service principal lacks workspace access
**Fix:** Grant workspace permissions to service principal

### ❌ Job Deployment Failed
**Cause:** Invalid job JSON or notebooks don't exist
**Fix:** Validate JSON syntax and ensure notebooks are in the repository

### ❌ Notebooks Not Found
**Cause:** `./notebooks` directory doesn't exist in repository
**Fix:** Create notebooks directory and add your notebooks

## Next Steps

1. ✅ Configure all 7 GitHub secrets
2. ✅ Create service principals in Databricks (3 total)
3. ✅ Grant workspace permissions to service principals
4. ✅ Add your notebooks to `./notebooks` directory
5. ✅ (Optional) Add job definitions to `./jobs` directory
6. ✅ Push to `develop` branch to test deployment
7. ✅ Verify deployment in Databricks workspace
8. ✅ Merge to `main` for production deployment

## Workflow is Ready! 🚀

Your GitHub Actions CI/CD pipeline is configured correctly and ready to use.
