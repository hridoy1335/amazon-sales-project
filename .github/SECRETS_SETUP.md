# GitHub Secrets Configuration - Step by Step

## Required Secrets: 4 Total

Your workflow needs these secrets to authenticate with Databricks:

| Secret Name | Description | Where to Get |
|------------|-------------|--------------|
| `DATABRICKS_HOST` | Workspace URL | Your browser address bar |
| `DATABRICKS_DEV_TOKEN` | PAT for dev | Generate in Databricks |
| `DATABRICKS_QA_TOKEN` | PAT for qa | Generate in Databricks |
| `DATABRICKS_PROD_TOKEN` | PAT for prod | Generate in Databricks |

---

## Step 1: Get Your Databricks Workspace URL

1. Open your Databricks workspace in a browser
2. Copy the URL from the address bar
3. Example: `https://adb-1234567890123456.7.azuredatabricks.net`
4. Keep this - you'll need it for `DATABRICKS_HOST`

---

## Step 2: Generate Personal Access Tokens (PAT)

### Option A: Create 3 Separate Tokens (RECOMMENDED)

This is more secure - you can revoke individual tokens if needed.

**For DEV Token:**
1. In Databricks, click your **username** (top-right) → **Settings**
2. Go to **Developer** → **Access tokens**
3. Click **Generate new token**
4. Fill in:
   - **Comment:** `github-actions-dev`
   - **Lifetime:** 90 days (or your preference)
5. Click **Generate**
6. **COPY THE TOKEN IMMEDIATELY** - you won't see it again!
7. Save it somewhere temporarily (you'll add to GitHub next)

**For QA Token:**
1. Click **Generate new token** again
2. Fill in:
   - **Comment:** `github-actions-qa`
   - **Lifetime:** 90 days
3. Click **Generate**
4. Copy and save the token

**For PROD Token:**
1. Click **Generate new token** again
2. Fill in:
   - **Comment:** `github-actions-prod`
   - **Lifetime:** 90 days
3. Click **Generate**
4. Copy and save the token

### Option B: Use 1 Token for All Environments (SIMPLER)

Less secure, but easier to manage.

1. Generate one token with comment `github-actions-all`
2. Copy the token
3. You'll use this same token value for all 3 environment secrets

---

## Step 3: Add Secrets to GitHub

1. Go to your GitHub repository
2. Click **Settings** (top navigation)
3. In left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**

### Add Secret 1: DATABRICKS_HOST

1. Click **New repository secret**
2. **Name:** `DATABRICKS_HOST`
3. **Value:** Your workspace URL (from Step 1)
   ```
   https://adb-1234567890123456.7.azuredatabricks.net
   ```
4. Click **Add secret**

### Add Secret 2: DATABRICKS_DEV_TOKEN

1. Click **New repository secret**
2. **Name:** `DATABRICKS_DEV_TOKEN`
3. **Value:** Paste the DEV token you generated
   ```
   dapi1234567890abcdefghijklmnopqrstuvwxyz
   ```
4. Click **Add secret**

### Add Secret 3: DATABRICKS_QA_TOKEN

1. Click **New repository secret**
2. **Name:** `DATABRICKS_QA_TOKEN`
3. **Value:** Paste the QA token you generated
4. Click **Add secret**

### Add Secret 4: DATABRICKS_PROD_TOKEN

1. Click **New repository secret**
2. **Name:** `DATABRICKS_PROD_TOKEN`
3. **Value:** Paste the PROD token you generated
4. Click **Add secret**

---

## Step 4: Verify Secrets Are Added

1. Still in **Settings → Secrets and variables → Actions**
2. You should see 4 secrets listed:
   ```
   ✅ DATABRICKS_HOST
   ✅ DATABRICKS_DEV_TOKEN
   ✅ DATABRICKS_QA_TOKEN
   ✅ DATABRICKS_PROD_TOKEN
   ```
3. Values will show as `***` (hidden for security)

---

## Step 5: Test the Workflow

Now test that everything works:

```bash
# 1. Make a small change
echo "# Test" >> README.md
git add README.md
git commit -m "Test deployment"

# 2. Push to dev branch
git push origin dev

# 3. Check GitHub Actions
# Go to Actions tab in your repository
# You should see the workflow running
```

**Expected behavior:**
- ✅ Workflow starts automatically
- ✅ Validation job runs
- ✅ Deploy-dev job runs
- ✅ Notebooks deployed to `/Workspace/Users/deployment/dev/notebooks`

---

## Quick Reference Card

Copy this for future reference:

```
Repository: prod-amazon-sales-project
GitHub Path: Settings → Secrets and variables → Actions

Secret 1: DATABRICKS_HOST
Value: https://adb-XXXX.X.azuredatabricks.net

Secret 2: DATABRICKS_DEV_TOKEN
Value: dapiXXXXXXXXXXXXXXXX (created in Databricks)

Secret 3: DATABRICKS_QA_TOKEN
Value: dapiXXXXXXXXXXXXXXXX (created in Databricks)

Secret 4: DATABRICKS_PROD_TOKEN
Value: dapiXXXXXXXXXXXXXXXX (created in Databricks)
```

---

## Token Management

### Set Reminders to Renew Tokens

If you set 90-day expiration:

| Token | Renewal Date | Action |
|-------|--------------|--------|
| DEV | (Date + 90 days) | Generate new token, update GitHub secret |
| QA | (Date + 90 days) | Generate new token, update GitHub secret |
| PROD | (Date + 90 days) | Generate new token, update GitHub secret |

### How to Update an Expired Token

1. Generate new token in Databricks (same steps as above)
2. Go to GitHub → Settings → Secrets and variables → Actions
3. Click on the secret name (e.g., `DATABRICKS_DEV_TOKEN`)
4. Click **Update secret**
5. Paste the new token value
6. Click **Update secret**

---

## Troubleshooting

### "Error: Invalid credentials"
- ✅ Check token hasn't expired (go to Databricks → Settings → Access tokens)
- ✅ Verify token is copied correctly (no extra spaces)
- ✅ Regenerate token if needed

### "Error: Host not found"
- ✅ Verify `DATABRICKS_HOST` includes `https://`
- ✅ Check URL is copied correctly from browser
- ✅ No trailing slash at the end

### Workflow doesn't run
- ✅ Verify all 4 secrets exist in GitHub
- ✅ Check you pushed to `dev`, `qa`, or `main` branch
- ✅ Look at Actions tab for error messages

### Can't find Settings tab
- ✅ Make sure you're viewing your repository (not someone else's)
- ✅ You need admin access to the repository
- ✅ Settings is in the top navigation bar

---

## Security Best Practices

✅ **Never commit tokens to git** - always use GitHub Secrets
✅ **Use separate tokens** for each environment when possible
✅ **Set expiration dates** - 90 days is recommended
✅ **Rotate regularly** - update before expiration
✅ **Revoke immediately** if token is compromised
✅ **Monitor usage** - check Databricks audit logs periodically

---

## You're All Set! 🚀

Once all 4 secrets are configured:
1. Push to `dev` → deploys to DEV
2. Push to `qa` → deploys to QA
3. Push to `main` → deploys to PROD

Everything is automatic - no manual steps required!
