# 🤖 Universal Claude + Colab Integration

## 📍 Location
This universal integration is now at: `/var/projects/UNIVERSAL_COLAB_CLAUDE_INTEGRATION.py`

## 🎯 Purpose
A reusable Google Colab integration that works with ANY Claude Coder project, not just movie booking.

## 🚀 How to Use

### 1. In Any Claude Project
```bash
# Claude can access the universal integration
cat /var/projects/UNIVERSAL_COLAB_CLAUDE_INTEGRATION.py
```

### 2. In Google Colab
1. Copy the contents of `UNIVERSAL_COLAB_CLAUDE_INTEGRATION.py`
2. Update these variables:
   ```python
   PROJECT_NAME = "your_project_name"  # e.g., "movie_booking", "web_scraper", etc.
   SERVICE_ACCOUNT_FOLDER_ID = "1tzHn4J3QntSLJlJNXcNJe3cLdILGEb3Z"  # Your folder ID
   ```
3. Run the cell - processor starts!

### 3. Send Commands from Claude
```python
# Example commands Claude can send:
{
    "id": "cmd_123",
    "type": "execute_code",
    "code": "print('Hello from any project!')"
}
```

## 📂 Shared Resources

```
/var/projects/
├── UNIVERSAL_COLAB_CLAUDE_INTEGRATION.py  # The universal integration
├── COLAB_INTEGRATION_README.md           # This file
├── eng-flux-459812-q6-e05c54813553.json  # Service account (if exists)
├── movie-booking-app/                    # Example project using it
├── leetcode/                             # Another project
└── [your-project]/                       # Any future project
```

## ✨ Features

- **Project Agnostic** - Works with any project
- **Multiple Projects** - One Colab can serve many Claude instances
- **Command Types**:
  - `execute_code` - Run Python code
  - `install_package` - Install packages
  - `shell_command` - Run shell commands
  - `ai_query` - AI queries (with API key)
  - `data_analysis` - Analyze data
  - `custom` - Your custom commands

## 🔧 Customization

Each project can customize by:
1. Changing `PROJECT_NAME`
2. Adding project-specific handlers in `handle_custom_command()`
3. Adding API keys as needed

## 🎯 Benefits

1. **One Integration** - Maintain one file for all projects
2. **No Duplication** - Share across Claude instances
3. **Easy Updates** - Update once, use everywhere
4. **Consistent Pattern** - Same approach for all projects

---

This universal integration is now available at the projects root level for any Claude Coder instance to use!