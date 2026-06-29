# GitHub Secrets Configuration Reference

## Authentication Method: Personal Access Token (PAT)

This project uses **PAT (Personal Access Token)** authentication for simplicity and ease of setup.

## How to Add Secrets in GitHub

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Enter the name and value
5. Click **Add secret**

## Required Secrets (4 Total)

### Workspace Connection (Shared)

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `DATABRICKS_HOST` | Your Databricks workspace URL | `https://adb-1234567890123456.7.azuredatabricks.net` |

### DEV Environment

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `DATABRICKS_DEV_TOKEN` | Personal Access Token for dev | `dapi1234567890abcdef...` |

### QA Environment

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `DATABRICKS_QA_TOKEN` | Personal Access Token for qa | `dapi2345678901bcdefg...` |

### PROD Environment

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `DATABRICKS_PROD_TOKEN` | Personal Access Token for prod | `dapi3456789012cdefgh...` |

## How to Get These Values

### DATABRICKS_HOST
1. Go to your Databricks workspace in a browser
2. Copy the URL from the address bar
3. Example: `https://adb-1234567890123456.7.azuredatabricks.net`

### Create Personal Access Tokens

You can either:
- Create **3 separate PAT tokens** (one for each environment) - RECOMMENDED
- Create **1 PAT token** and use it for all environments (simpler but less secure)

#### Method 1: Separate PAT for Each Environment (Recommended)

**Create DEV Token:**
1. Log into your Databricks workspace
2. Click your username (top right) → **Settings**
3. Go to **Developer** → **Access tokens**
4. Click **Generate new token**
5. Enter comment: `github-actions-dev`
6. Set lifetime: 90 days (recommended) or as needed
7. Click **Generate**
8. Copy the token immediately (you won't see it again!)
9. Save as `DATABRICKS_DEV_TOKEN` in GitHub secrets

**Repeat for QA and PROD:**
- Create token with comment `github-actions-qa` → Save as `DATABRICKS_QA_TOKEN`
- Create token with comment `github-actions-prod` → Save as `DATABRICKS_PROD_TOKEN`

#### Method 2: Single PAT for All Environments (Simpler)

1. Create one PAT token with comment `github-actions-all`
2. Copy the token
3. Add it as THREE GitHub secrets with the same value:
   - `DATABRICKS_DEV_TOKEN`
   - `DATABRICKS_QA_TOKEN`
   - `DATABRICKS_PROD_TOKEN`

**Note:** Using separate tokens is more secure because:
- You can revoke individual environment tokens if compromised
- You can set different expiration dates
- You can track which token is used for what

## Grant Permissions

The user/token owner needs the following permissions:

**Workspace Access:**
- Can create and edit notebooks
- Can create and manage jobs
- Access to `/Workspace/Users/deployment/` folder

**Unity Catalog Access (if using catalogs):**
- USE CATALOG on dev_amazon, qa_amazon, prod_amazon
- CREATE TABLE/VIEW/FUNCTION on relevant schemas
- SELECT/MODIFY on tables

## Verification

After adding all secrets:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. You should see **4 secrets** listed
3. Values will be hidden (shown as `***`)

## Security Best Practices

✅ **Use separate tokens** for each environment when possible
✅ **Set expiration dates** on tokens (90 days recommended)
✅ **Rotate tokens regularly** - GitHub will notify you before expiration
✅ **Use minimal permissions** - grant only what's needed for deployments
✅ **Store tokens securely** - only in GitHub Secrets, never in code
✅ **Revoke tokens** immediately if compromised

## Troubleshooting

**Authentication Failed:**
* Verify TOKEN is correct (no extra spaces)
* Check HOST URL is correct and includes `https://`
* Ensure token hasn't expired
* Verify token owner has workspace access

**Permission Denied:**
* Grant workspace folder permissions to token owner
* Verify user has necessary catalog/schema permissions
* Check job creation permissions

**Token Expired:**
* Create a new token in Databricks
* Update the GitHub secret with new token value
* Set a calendar reminder to renew before expiration

## Token Rotation Schedule

Set reminders to rotate tokens:

| Token | Create Date | Expiration | Action |
|-------|-------------|------------|--------|
| DEV | YYYY-MM-DD | YYYY-MM-DD | Renew before expiration |
| QA | YYYY-MM-DD | YYYY-MM-DD | Renew before expiration |
| PROD | YYYY-MM-DD | YYYY-MM-DD | Renew before expiration |
