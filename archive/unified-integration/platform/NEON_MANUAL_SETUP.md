# 🚀 Neon PostgreSQL - Manual Setup Guide

You already have a Neon project created! Here's how to get your connection string:

## Your Project Details
- **Project Name**: ai-integration-platform  
- **Project ID**: spring-paper-60199096
- **Region**: US East (AWS)

## Get Your Connection String (1 minute)

1. **Go to your Neon Dashboard**:
   ```
   https://console.neon.tech/app/projects/spring-paper-60199096
   ```

2. **Sign in** with the account that owns API key: `napi_s8buji2qmt4...`

3. **On the Dashboard**, you'll see a box with:
   - "Connection string" or "Connection Details"
   - Click **"Show password"** if the password is hidden
   - **Copy the entire connection string**

4. **The connection string looks like**:
   ```
   postgresql://neondb_owner:ActualPasswordHere@ep-purple-pine-a58z5kj2.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

## Configure Your App (30 seconds)

Once you have the connection string:

1. **Update your .env file** - Replace the DATABASE_URL line with your actual connection string:
   ```
   DATABASE_URL=postgresql://neondb_owner:YourActualPassword@ep-purple-pine-a58z5kj2.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

2. **Run the setup script**:
   ```bash
   python3 finalize_neon_setup.py
   ```

## Alternative: Reset Password via Dashboard

If you can't find the password:

1. Go to your project dashboard
2. Click on "Roles" in the left menu
3. Click on `neondb_owner`
4. Click "Reset password"
5. Copy the new password
6. Update your connection string

---

**Direct link to your project**: https://console.neon.tech/app/projects/spring-paper-60199096