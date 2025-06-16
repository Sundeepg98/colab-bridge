#!/usr/bin/env python3
"""
Create and upload a ACTUALLY WORKING Colab notebook
"""

import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.universal_bridge import UniversalColabBridge

def create_fixed_notebook():
    """Create notebook with proper working cells"""
    
    # Fixed cells that actually work
    cells = [
        {
            "cell_type": "code",
            "source": [
                "# Cell 1: Mount Drive\n",
                "from google.colab import drive\n",
                "drive.mount('/content/drive')\n",
                "print('✅ Drive mounted')"
            ],
            "metadata": {},
            "execution_count": None,
            "outputs": []
        },
        {
            "cell_type": "code", 
            "source": [
                "# Cell 2: Authentication\n",
                "from google.colab import auth\n",
                "auth.authenticate_user()\n",
                "print('✅ Authenticated with Google')"
            ],
            "metadata": {},
            "execution_count": None,
            "outputs": []
        },
        {
            "cell_type": "code",
            "source": [
                "# Cell 3: Setup Dependencies\n",
                "import os, json, time, traceback\n",
                "from datetime import datetime\n",
                "from googleapiclient.discovery import build\n",
                "from googleapiclient.http import MediaFileUpload\n",
                "import io\n",
                "import tempfile\n",
                "\n",
                "# Build drive service\n",
                "drive_service = build('drive', 'v3')\n",
                "FOLDER_ID = '1tzHn4J3QntSLJlJNXcNJe3cLdILGEb3Z'\n",
                "\n",
                "print('✅ Dependencies loaded')\n",
                "print(f'📁 Folder: {FOLDER_ID}')\n",
                "\n",
                "# Test folder access\n",
                "try:\n",
                "    query = f\"'{FOLDER_ID}' in parents and trashed=false\"\n",
                "    results = drive_service.files().list(q=query, fields='files(id, name)', maxResults=5).execute()\n",
                "    files = results.get('files', [])\n",
                "    print(f'✅ Folder accessible, {len(files)} files found')\n",
                "except Exception as e:\n",
                "    print(f'❌ Folder access error: {e}')"
            ],
            "metadata": {},
            "execution_count": None,
            "outputs": []
        },
        {
            "cell_type": "code",
            "source": [
                "# Cell 4: Create Active Processor\n",
                "class ActiveProcessor:\n",
                "    def __init__(self):\n",
                "        self.processed = set()\n",
                "        self.running = False\n",
                "        self.stats = {'processed': 0, 'errors': 0}\n",
                "        print('✅ Processor initialized')\n",
                "        \n",
                "    def get_commands(self):\n",
                "        try:\n",
                "            query = f\"'{FOLDER_ID}' in parents and name contains 'command_' and trashed=false\"\n",
                "            results = drive_service.files().list(q=query, fields='files(id, name)').execute()\n",
                "            commands = [f for f in results.get('files', []) if f['id'] not in self.processed]\n",
                "            return commands\n",
                "        except Exception as e:\n",
                "            print(f'❌ Get commands error: {e}')\n",
                "            return []\n",
                "    \n",
                "    def execute_code(self, code):\n",
                "        import sys\n",
                "        from io import StringIO\n",
                "        \n",
                "        old_stdout = sys.stdout\n",
                "        sys.stdout = StringIO()\n",
                "        \n",
                "        try:\n",
                "            namespace = {\n",
                "                '__name__': '__main__',\n",
                "                'print': print,\n",
                "                'datetime': datetime,\n",
                "                'time': time,\n",
                "                'os': os,\n",
                "                'json': json\n",
                "            }\n",
                "            \n",
                "            try:\n",
                "                import numpy as np\n",
                "                import pandas as pd\n",
                "                import matplotlib.pyplot as plt\n",
                "                namespace.update({'np': np, 'pd': pd, 'plt': plt})\n",
                "            except ImportError:\n",
                "                pass\n",
                "            \n",
                "            exec(code, namespace)\n",
                "            output = sys.stdout.getvalue()\n",
                "            \n",
                "            return {\n",
                "                'status': 'success',\n",
                "                'output': output,\n",
                "                'timestamp': time.time()\n",
                "            }\n",
                "        except Exception as e:\n",
                "            return {\n",
                "                'status': 'error',\n",
                "                'error': str(e),\n",
                "                'traceback': traceback.format_exc(),\n",
                "                'timestamp': time.time()\n",
                "            }\n",
                "        finally:\n",
                "            sys.stdout = old_stdout\n",
                "    \n",
                "    def write_response(self, cmd_id, response):\n",
                "        try:\n",
                "            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:\n",
                "                json.dump(response, f, indent=2)\n",
                "                temp_path = f.name\n",
                "            \n",
                "            file_metadata = {\n",
                "                'name': f'result_{cmd_id}.json',\n",
                "                'parents': [FOLDER_ID]\n",
                "            }\n",
                "            \n",
                "            media = MediaFileUpload(temp_path, mimetype='application/json')\n",
                "            \n",
                "            drive_service.files().create(\n",
                "                body=file_metadata,\n",
                "                media_body=media\n",
                "            ).execute()\n",
                "            \n",
                "            os.unlink(temp_path)\n",
                "            print(f'✅ Response written: result_{cmd_id}.json')\n",
                "            \n",
                "        except Exception as e:\n",
                "            print(f'❌ Write error: {e}')\n",
                "    \n",
                "    def process_command(self, cmd_file):\n",
                "        try:\n",
                "            content = drive_service.files().get_media(fileId=cmd_file['id']).execute()\n",
                "            request = json.loads(content.decode('utf-8'))\n",
                "            \n",
                "            cmd_id = cmd_file['name'].replace('command_', '').replace('.json', '')\n",
                "            print(f'\\n📋 Processing: {cmd_id}')\n",
                "            \n",
                "            result = self.execute_code(request.get('code', ''))\n",
                "            self.write_response(cmd_id, result)\n",
                "            \n",
                "            self.processed.add(cmd_file['id'])\n",
                "            self.stats['processed'] += 1\n",
                "            \n",
                "            if result['status'] == 'error':\n",
                "                self.stats['errors'] += 1\n",
                "                print(f\"❌ Error: {result['error']}\")\n",
                "            else:\n",
                "                print(f\"✅ Success: {len(result.get('output', ''))} chars output\")\n",
                "                \n",
                "        except Exception as e:\n",
                "            print(f'❌ Process error: {e}')\n",
                "            self.stats['errors'] += 1\n",
                "\n",
                "# Create processor\n",
                "processor = ActiveProcessor()\n",
                "print('✅ Active processor created')"
            ],
            "metadata": {},
            "execution_count": None,
            "outputs": []
        },
        {
            "cell_type": "code",
            "source": [
                "# Cell 5: RUN PROCESSOR (Continuous Loop)\n",
                "print('🚀 Starting ACTIVE processor...')\n",
                "print('⚠️ This cell runs continuously, NOT 0ms!')\n",
                "\n",
                "processor.running = True\n",
                "start_time = time.time()\n",
                "duration = 1800  # 30 minutes\n",
                "\n",
                "print(f'⏱️ Will run for {duration//60} minutes')\n",
                "print('📊 Status updates every 5 seconds...')\n",
                "\n",
                "try:\n",
                "    while processor.running and (time.time() - start_time < duration):\n",
                "        commands = processor.get_commands()\n",
                "        \n",
                "        if commands:\n",
                "            print(f'\\n📨 Found {len(commands)} commands!')\n",
                "            for cmd in commands:\n",
                "                processor.process_command(cmd)\n",
                "                if not processor.running:\n",
                "                    break\n",
                "        else:\n",
                "            elapsed = int(time.time() - start_time)\n",
                "            print(f'⏳ Active... {elapsed}s | Processed: {processor.stats[\"processed\"]} | Errors: {processor.stats[\"errors\"]}')\n",
                "        \n",
                "        time.sleep(5)\n",
                "        \n",
                "except KeyboardInterrupt:\n",
                "    print('🛑 Stopped by user')\n",
                "    processor.running = False\n",
                "\n",
                "print('🛑 Processor stopped')\n",
                "print(f'📊 Final stats: {processor.stats}')"
            ],
            "metadata": {},
            "execution_count": None,
            "outputs": []
        }
    ]
    
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"name": "python3", "display_name": "Python 3"},
            "colab": {"provenance": []}
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    
    return notebook

def upload_working_notebook():
    """Upload the fixed notebook"""
    print("🔧 CREATING WORKING NOTEBOOK")
    print("=" * 40)
    
    try:
        bridge = UniversalColabBridge("fix_notebook")
        bridge.initialize()
        
        # Create notebook
        notebook = create_fixed_notebook()
        
        # Save temporarily
        temp_path = "/tmp/WORKING_processor.ipynb"
        with open(temp_path, 'w') as f:
            json.dump(notebook, f, indent=2)
        
        print(f"✅ Created working notebook: {temp_path}")
        
        # Upload to Drive
        from googleapiclient.http import MediaFileUpload
        
        file_metadata = {
            'name': 'WORKING-Hybrid-Processor.ipynb',
            'parents': [bridge.folder_id]
        }
        
        media = MediaFileUpload(temp_path, mimetype='application/json')
        
        file = bridge.drive_service.files().create(
            body=file_metadata,
            media_body=media
        ).execute()
        
        file_id = file.get('id')
        
        # Make shareable
        permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': 'sundeepg8@gmail.com'
        }
        
        bridge.drive_service.permissions().create(
            fileId=file_id,
            body=permission
        ).execute()
        
        # Also make publicly readable
        public_permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        
        bridge.drive_service.permissions().create(
            fileId=file_id,
            body=public_permission
        ).execute()
        
        colab_link = f"https://colab.research.google.com/drive/{file_id}"
        
        print(f"✅ WORKING notebook uploaded!")
        print(f"🔗 LINK: {colab_link}")
        
        # Clean up
        import os
        os.unlink(temp_path)
        
        return colab_link
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None

def test_working_notebook():
    """Test the processor by sending a command"""
    print("\n🧪 TESTING THE WORKING PROCESSOR")
    print("=" * 40)
    
    try:
        bridge = UniversalColabBridge("test_working")
        bridge.initialize()
        
        # Send test command
        test_result = bridge.execute_code("""
print("🎉 WORKING PROCESSOR TEST!")
print("✅ This proves the hybrid system works!")
import datetime
print(f"⏰ Executed at: {datetime.datetime.now()}")
print("🚀 Ready for hybrid development!")
""", timeout=30)
        
        print(f"📊 Test Result:")
        print(f"   Status: {test_result.get('status')}")
        
        if test_result.get('status') == 'success':
            print("🎉 SUCCESS! PROCESSOR IS WORKING!")
            print("📤 Output:")
            print(test_result.get('output', ''))
            return True
        elif test_result.get('status') == 'queued':
            print("⏳ Command queued - processor starting up")
            return "queued"
        else:
            print(f"❌ Error: {test_result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("🎯 FIXING AND UPLOADING WORKING NOTEBOOK")
    print("I'll handle this myself!")
    print("=" * 50)
    
    # Upload working notebook
    colab_link = upload_working_notebook()
    
    if colab_link:
        print(f"\n✅ WORKING NOTEBOOK READY!")
        print(f"🔗 {colab_link}")
        print(f"\nℹ️ This notebook:")
        print(f"   ✅ Has proper continuous loop in Cell 5")
        print(f"   ✅ Shows status updates every 5 seconds")
        print(f"   ✅ Actually processes commands")
        print(f"   ✅ Won't finish in 0ms!")
        
        print(f"\n🎯 NEXT: Open link and run all cells")
        print(f"Cell 5 should show status updates, not finish immediately!")
        
    else:
        print(f"\n❌ FAILED TO CREATE WORKING NOTEBOOK")