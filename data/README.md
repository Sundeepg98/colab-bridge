# 📊 Data Directory

This directory contains runtime data, caches, and temporary files for Colab Bridge.

## 📁 File Structure

```
data/
├── README.md              # This file
├── cache/                 # Cached responses and temporary data
├── requests/              # Local backup of requests (optional)
├── responses/             # Local backup of responses (optional)
└── metrics/               # Usage metrics and analytics
```

## 🔄 File Types

### Cache Files
- **Purpose**: Speed up repeated requests
- **Format**: JSON files with request/response pairs
- **Cleanup**: Automatically cleaned after 24 hours

### Request/Response Backups
- **Purpose**: Local backup of Google Drive communication
- **Format**: JSON files matching Drive file names
- **Usage**: Debugging and audit trail

### Metrics
- **Purpose**: Track usage patterns and performance
- **Format**: JSON/CSV files with timestamps
- **Privacy**: No sensitive data, only metadata

## 🧹 Maintenance

Files in this directory are automatically managed:

- **Auto-cleanup**: Files older than 24 hours are removed
- **Size limits**: Directory size is monitored
- **Compression**: Old files may be compressed

## 🔍 Debugging

Use files in this directory to:
- Debug failed requests
- Analyze performance patterns
- Audit request history
- Monitor system health

## 🚨 Privacy

This directory may contain:
- ✅ **Safe**: Request metadata, timestamps, status codes
- ❌ **Sensitive**: Code content, output data, error details

**Note**: Sensitive data is only stored temporarily and is automatically cleaned up.