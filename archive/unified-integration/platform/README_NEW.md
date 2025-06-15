# AI Platform

A comprehensive platform for integrating and managing multiple AI services including chatbots (GPT-4, Claude, Cohere) and content simulators (Stable Diffusion, DALL-E, Midjourney, RunwayML).

## 🚀 Features

### Multi-Service Integration
- **Chatbots**: OpenAI GPT-4/3.5, Anthropic Claude, Cohere, Meta LLaMA
- **Image Simulators**: Stable Diffusion, DALL-E 3, Midjourney  
- **Video Simulators**: RunwayML, Sora (coming soon)
- **Audio Simulators**: ElevenLabs
- **Multi-Modal**: Replicate, Hugging Face

### Intelligent Management
- 🔄 **Dynamic Routing**: Automatically route to best service
- 💰 **Cost Optimization**: Use cheapest service that meets requirements
- 🛡️ **Fallback System**: Automatic failover when services are down
- 📊 **Usage Tracking**: Real-time cost and usage monitoring
- 🔔 **Smart Alerts**: Proactive notifications for issues

### User-Centric Design
- 👤 **User-Managed Integrations**: Users add their own API keys
- 💳 **Transparent Billing**: See exact costs from each platform
- 🎯 **Clear Error Attribution**: Know if issues are yours/ours/theirs
- ⚡ **Responsive Support**: Real-time integration health monitoring

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│            Web Interface                 │
│   (User Dashboard + Admin Dashboard)     │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│          Platform Core (Flask)           │
│  • Request Routing                       │
│  • Cost Tracking                         │
│  • Health Monitoring                     │
│  • User Integration Management           │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│        AI Service Integrations           │
├─────────────────────────────────────────┤
│ Chatbots          │ Simulators          │
│ • OpenAI          │ • Stable Diffusion  │
│ • Anthropic       │ • DALL-E            │
│ • Cohere          │ • Midjourney        │
│ • LLaMA           │ • RunwayML          │
└─────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/yourorg/ai-platform.git
cd ai-platform
```

### 2. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Platform
```bash
python app.py
```

### 4. Access the Platform
- User Dashboard: `http://localhost:5000/dashboard`
- Admin Dashboard: `http://localhost:5000/admin-enhanced`
- Integration Setup: `http://localhost:5000/integration-quickstart`

## 🛠️ CLI Tool

The platform includes a powerful CLI for maintenance and monitoring:

```bash
# Install CLI
cd cli
pip install -e .

# Usage
aip health check                    # Check all integrations
aip monitor dashboard               # Live monitoring
aip maintenance run cache_cleanup   # Run maintenance
aip costs analyze --by-service      # Analyze costs
```

## 📁 Project Structure

```
ai-platform/
├── src/                    # Core platform code
│   ├── api_endpoints.py    # REST API endpoints
│   ├── integration_manager.py
│   ├── user_integrations.py
│   └── health_monitoring.py
├── templates/              # Web UI templates
│   ├── user_dashboard.html
│   ├── integration_quickstart.html
│   └── admin_dashboard_enhanced.html
├── cli/                    # CLI tool
│   └── platform_cli.py
├── docs/                   # Documentation
└── tests/                  # Test suite
```

## 🔧 Configuration

### User Integration Setup

Users manage their own API keys through the dashboard:

1. Navigate to `/dashboard/integrations`
2. Click "Add Integration"
3. Select service (OpenAI, Claude, etc.)
4. Enter API key
5. Platform validates and activates

### Platform Configuration

```python
# config.py
PLATFORM_SETTINGS = {
    'service_fee_percentage': 5,  # Optional platform fee
    'health_check_interval': 60,  # Seconds
    'fallback_enabled': True,
    'cost_optimization': True
}
```

## 📊 Features in Detail

### Dynamic Service Selection
```python
# Automatically selects best service based on:
- Cost (cheapest that meets requirements)
- Availability (skip services that are down)
- Performance (fastest response time)
- User preferences
```

### Health Monitoring
- Continuous health checks every 60 seconds
- Immediate validation when adding integrations
- Clear error messages with attribution
- Automatic recovery for external issues

### Cost Management
- Real-time cost tracking per user
- Cost optimization recommendations
- Budget alerts and limits
- Transparent platform fees

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🔄 Migration from Sora-AI-Exploration

This project was previously named `sora-ai-exploration` but has evolved into a generic AI platform. To update your local repository:

```bash
git remote set-url origin https://github.com/yourorg/ai-platform.git
```

## 🆘 Support

- Documentation: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/yourorg/ai-platform/issues)
- Discord: [Join our community](#)

---

Built with ❤️ for the AI community. Not affiliated with OpenAI's Sora or any specific AI service.