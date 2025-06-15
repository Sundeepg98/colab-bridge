#!/usr/bin/env python3

try:
    from app import app
    print('Flask app loaded successfully')
    
    # Test the unified system status endpoint
    with app.test_client() as client:
        response = client.get('/api/unified-system-status')
        print(f'Unified system status: {response.status_code}')
        if response.status_code != 200:
            print(f'Response: {response.get_data(as_text=True)}')
        else:
            print('✓ Unified system status endpoint working')
            
        # Test dynamic framework endpoints with correct URLs
        response = client.get('/api/service-discovery-status')
        print(f'Service discovery status: {response.status_code}')
        
        response = client.get('/api/fallback-system-status')
        print(f'Fallback system status: {response.status_code}')
        
        response = client.get('/api/independent-core-status')
        print(f'Independent core status: {response.status_code}')
        
        response = client.get('/api/system-recommendations')
        print(f'System recommendations: {response.status_code}')
        
        if all([
            client.get('/api/unified-system-status').status_code == 200,
            client.get('/api/service-discovery-status').status_code == 200,
            client.get('/api/fallback-system-status').status_code == 200,
            client.get('/api/independent-core-status').status_code == 200,
            client.get('/api/system-recommendations').status_code == 200,
        ]):
            print('\n✅ All dynamic framework API endpoints are working!')
        else:
            print('\n❌ Some endpoints are not working properly')
            
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()