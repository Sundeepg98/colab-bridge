# 🚀 Neon PostgreSQL - Quick Setup Guide

## Step 1: Sign Up (1 minute)

1. **Go to**: https://console.neon.tech/signup
2. **Choose**: Sign up with GitHub (fastest) or Email
3. **Confirm** your email if needed

## Step 2: Get Connection String (30 seconds)

After signup, you'll see your dashboard:

1. **Look for**: "Connection Details" box (usually green/blue)
2. **Click**: "Show password" link
3. **Copy**: The entire connection string

It looks like this:
```
postgresql://username:password@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb
```

## Step 3: Run Setup (1 minute)

```bash
python3 neon_setup_guide.py
```

Then paste your connection string when prompted.

## 🎯 Quick Tips

- **Can't find connection string?** 
  - It's on the main dashboard
  - Or go to: Settings → Connection strings

- **Which connection type?**
  - Use "Direct connection" (not pooled) for now

- **Forgot to copy password?**
  - Click your database name
  - Go to "Connection strings" 
  - Click "Show password"

## 📊 What You Get FREE

- ✅ **3GB storage** (enough for ~1 million records)
- ✅ **Always-on** database
- ✅ **Automatic backups**
- ✅ **SSL encryption**
- ✅ **Connection pooling**
- ✅ **Database branching**

## 🆘 Common Issues

**"Connection failed"**
- Make sure you copied the ENTIRE string including password
- Password might be hidden - click "Show password"

**"Invalid connection string"**
- Don't include quotes around the string
- Make sure it starts with `postgresql://`

**"Authentication failed"**
- The password is case-sensitive
- Try copying again from Neon dashboard

---

Ready? Run: `python3 neon_setup_guide.py`