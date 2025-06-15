# User Integration System Design

## Overview

The integration system should be **user-managed**, not admin-managed. Users add their own API keys and pay the actual costs from each platform.

## Current Problems

1. **Admin Burden**: Admin shouldn't manage user API keys
2. **Pricing Control**: We can't control OpenAI, Anthropic, or Stability AI pricing
3. **Scalability**: Admin can't manually add keys for every user

## Proposed Solution

### 1. User Dashboard
Each user gets their own integration management page where they can:
- Add their own API keys
- See real-time costs from each platform
- Monitor usage and spending
- Enable/disable integrations

### 2. Platform Role
The platform:
- **Routes requests** to the appropriate service
- **Tracks usage** and costs
- **Optimizes** which service to use
- **Provides fallbacks** when services fail
- **Adds platform fee** (optional) on top of actual costs

### 3. Pricing Structure

```
Total Cost = Platform Cost + Platform Fee (optional)

Where:
- Platform Cost = Actual cost from OpenAI/Claude/etc
- Platform Fee = Fixed % or flat fee per request
```

## Implementation Changes

### 1. Move Integration UI from Admin to User

**From**: `/admin-enhanced/integrations`  
**To**: `/dashboard/integrations`

### 2. User API Key Storage

```python
class UserIntegration:
    user_id: str
    service: str  # 'openai', 'anthropic', etc.
    api_key: str  # Encrypted
    enabled: bool
    added_date: datetime
    total_spent: float
    last_used: datetime
```

### 3. Cost Tracking

```python
class UsageRecord:
    user_id: str
    service: str
    request_type: str  # 'text', 'image', 'video'
    platform_cost: float  # What OpenAI/etc charged
    platform_fee: float   # Our markup (if any)
    total_cost: float
    timestamp: datetime
```

## Benefits

1. **No Admin Overhead**: Users manage their own integrations
2. **Transparent Pricing**: Users see exactly what each platform charges
3. **Scalable**: Works for unlimited users
4. **Flexible**: Users can use their own accounts with volume discounts
5. **Revenue Model**: Optional platform fee on top of actual costs

## User Flow

1. User signs up for platform
2. Goes to "My Integrations" page
3. Adds their API keys for desired services
4. Platform automatically:
   - Routes requests to their integrated services
   - Tracks costs
   - Optimizes for best price/performance
   - Falls back to other services if one fails

## Admin Dashboard Changes

The admin dashboard should show:
- **Platform Statistics**: Total requests, revenue from platform fees
- **Service Health**: Which services are up/down
- **User Analytics**: Most popular integrations, usage patterns
- **NOT individual user API keys**

## Example User Integration Page

```
My Integrations
---------------

[+] Add New Integration

Active Integrations:
┌─────────────────────────────────────────┐
│ OpenAI (GPT-4)                          │
│ Status: ✓ Active                        │
│ This Month: $12.43                      │
│ [Configure] [Disable] [Remove]          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Stable Diffusion                        │
│ Status: ✓ Active                        │
│ This Month: $8.21                       │
│ [Configure] [Disable] [Remove]          │
└─────────────────────────────────────────┘

Total Platform Costs This Month: $20.64
Platform Service Fee (5%): $1.03
-----------------------------------
Total: $21.67
```

## Revenue Models

### Option 1: Percentage Fee
- Add 5-10% on top of actual platform costs
- Simple and scales with usage

### Option 2: Flat Monthly Fee
- $X/month for unlimited integrations
- Users still pay their own platform costs

### Option 3: Freemium
- Free: Use our API keys (limited)
- Paid: Add your own keys (unlimited)

### Option 4: No Platform Fee
- Monetize through other features
- Integration management is free value-add

## Security Considerations

1. **Encrypt all API keys** in database
2. **Never expose keys** to frontend
3. **Audit trail** of all API usage
4. **Rate limiting** per user
5. **Anomaly detection** for unusual usage

## Migration Plan

1. Create new user integration tables
2. Build user-facing integration UI
3. Move existing admin integrations to system-level
4. Update routing to check user integrations first
5. Add billing/cost tracking
6. Deprecate admin integration management

This approach makes integrations a user feature, not an admin burden, while maintaining platform control over routing, optimization, and optional monetization.