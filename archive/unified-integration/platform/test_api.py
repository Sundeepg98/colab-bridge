import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load .env file
load_dotenv()

key = os.getenv('ANTHROPIC_API_KEY')
print(f'Key loaded: {"Yes" if key else "No"}')
print(f'Key length: {len(key) if key else 0}')

if key:
    try:
        client = Anthropic(api_key=key)
        response = client.messages.create(
            model='claude-3-5-sonnet-20241022',
            max_tokens=50,
            messages=[{'role': 'user', 'content': 'Say hello'}]
        )
        print(f'API Test: Success')
        print(f'Response: {response.content[0].text}')
    except Exception as e:
        print(f'API Test Failed: {e}')
else:
    print('No API key found in .env')
