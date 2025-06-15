# 🔐 Credentials Directory

This directory contains sensitive authentication files for Colab Bridge.

## 📁 File Structure

```
credentials/
├── README.md                    # This file
├── your-service-account.json    # Google Cloud service account (KEEP PRIVATE!)
├── example.json                 # Example service account structure
└── .gitkeep                     # Keeps directory in git
```

## 🔒 Security Notes

- **NEVER commit actual credential files to git**
- All `.json` files are automatically ignored by `.gitignore`
- Only `example.json` and `template.json` files are allowed in git
- Store credentials securely and use environment variables when possible

## 📋 Setup Instructions

1. **Download your service account JSON** from Google Cloud Console
2. **Place it in this directory** with a descriptive name
3. **Update your config** to point to the correct file path
4. **Verify permissions** - file should be readable only by you

```bash
# Set proper permissions
chmod 600 credentials/your-service-account.json
```

## 🛡️ Best Practices

- Use different service accounts for different environments
- Rotate credentials regularly
- Monitor service account usage in Google Cloud Console
- Use least-privilege permissions (only Google Drive API access needed)

## 🚨 If Credentials Are Compromised

1. **Immediately disable** the service account in Google Cloud Console
2. **Generate new credentials**
3. **Update all applications** using the old credentials
4. **Review access logs** for unauthorized usage