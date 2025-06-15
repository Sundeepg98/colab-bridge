#!/usr/bin/env python3
"""
Interactive Project Renaming Script
Renames sora-ai-exploration project to a generic AI platform name
"""

import os
import re
import shutil
import glob
from pathlib import Path
from typing import List, Dict, Tuple

# Suggested generic AI platform names
SUGGESTED_NAMES = [
    "ai-platform",
    "unified-ai-platform", 
    "multi-ai-platform",
    "ai-optimization-platform",
    "universal-ai-engine",
    "ai-integration-hub",
    "smart-ai-platform",
    "ai-orchestrator",
    "intelligent-ai-suite",
    "ai-workflow-engine"
]

class ProjectRenamer:
    def __init__(self, project_root: str = "/var/projects/sora-ai-exploration"):
        self.project_root = Path(project_root)
        self.current_name = "sora-ai-exploration"
        self.current_title = "Sora AI Platform"
        self.current_underscore = "ai_integration_platform"
        
        # Key files to update (relative to project root)
        self.key_files = [
            "README.md",
            "app.py", 
            "DEPLOYMENT_STATUS.md",
            "NEON_SUCCESS.md",
            "Dockerfile",
            "docker-compose.yml",
            "docker/Dockerfile",
            "docker/docker-compose.yml",
            "PROJECT_CONFIG.py",
            "requirements.txt",
            "requirements_production.txt",
            "setup.py",
            "cli/setup.py",
            "src/config.py",
            "src/database/db_config.py",
            "config/api_config.py"
        ]

    def display_suggestions(self) -> None:
        """Display suggested project names"""
        print("\n🚀 Project Renaming Tool")
        print("=" * 50)
        print(f"Current project: {self.current_name}")
        print(f"Current location: {self.project_root}")
        print("\n💡 Suggested generic AI platform names:")
        
        for i, name in enumerate(SUGGESTED_NAMES, 1):
            print(f"  {i:2d}. {name}")
        
        print(f"  {len(SUGGESTED_NAMES) + 1:2d}. Enter custom name")

    def get_user_choice(self) -> Tuple[str, str, str]:
        """Get user's choice for new project name"""
        while True:
            try:
                choice = input(f"\nEnter your choice (1-{len(SUGGESTED_NAMES) + 1}): ").strip()
                
                if choice.isdigit():
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(SUGGESTED_NAMES):
                        new_name = SUGGESTED_NAMES[choice_num - 1]
                        break
                    elif choice_num == len(SUGGESTED_NAMES) + 1:
                        new_name = input("Enter custom project name (use kebab-case): ").strip()
                        if self.validate_name(new_name):
                            break
                        else:
                            print("❌ Invalid name. Use lowercase letters, numbers, and hyphens only.")
                            continue
                    else:
                        print(f"❌ Please enter a number between 1 and {len(SUGGESTED_NAMES) + 1}")
                        continue
                else:
                    print(f"❌ Please enter a valid number")
                    continue
                    
            except KeyboardInterrupt:
                print("\n\n👋 Operation cancelled by user")
                exit(0)
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
        
        # Generate title and underscore versions
        new_title = self.name_to_title(new_name)
        new_underscore = new_name.replace("-", "_")
        
        return new_name, new_title, new_underscore

    def validate_name(self, name: str) -> bool:
        """Validate project name format"""
        pattern = r'^[a-z0-9-]+$'
        return bool(re.match(pattern, name)) and not name.startswith('-') and not name.endswith('-')

    def name_to_title(self, name: str) -> str:
        """Convert kebab-case name to title format"""
        words = name.split('-')
        # Capitalize AI specifically
        title_words = []
        for word in words:
            if word.lower() == 'ai':
                title_words.append('AI')
            else:
                title_words.append(word.capitalize())
        return ' '.join(title_words)

    def preview_changes(self, new_name: str, new_title: str, new_underscore: str) -> None:
        """Preview what changes will be made"""
        print(f"\n📋 Preview of changes:")
        print("=" * 50)
        print(f"Project name:     {self.current_name} → {new_name}")
        print(f"Project title:    {self.current_title} → {new_title}")
        print(f"Underscore name:  {self.current_underscore} → {new_underscore}")
        print(f"New directory:    /var/projects/{new_name}")
        
        print(f"\n📁 Key files to be updated:")
        existing_files = []
        for file_path in self.key_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                existing_files.append(str(file_path))
        
        for file_path in existing_files:
            print(f"  • {file_path}")
        
        # Check for database files
        db_files = glob.glob(str(self.project_root / "sora_ai*.db"))
        if db_files:
            print(f"\n🗄️ Database files to be renamed:")
            for db_file in db_files:
                old_name = Path(db_file).name
                new_db_name = old_name.replace("sora_ai", new_underscore)
                print(f"  • {old_name} → {new_db_name}")

    def update_file_content(self, file_path: Path, new_name: str, new_title: str, new_underscore: str) -> bool:
        """Update content in a single file"""
        try:
            if not file_path.exists():
                return True  # Skip non-existent files
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Replace project name references
            content = content.replace(self.current_name, new_name)
            content = content.replace(self.current_title, new_title)
            content = content.replace(self.current_underscore, new_underscore)
            
            # Handle specific cases
            if file_path.name == "docker-compose.yml":
                # Update container names and database names
                content = re.sub(r'container_name:\s*.*sora.*', f'container_name: {new_underscore}', content, flags=re.IGNORECASE)
                content = re.sub(r'POSTGRES_DB:\s*.*sora.*', f'POSTGRES_DB: {new_underscore}', content, flags=re.IGNORECASE)
            
            # Replace "Sora AI" with "AI Platform" specifically
            content = content.replace("Sora AI", "AI Platform")
            
            # Only write if content changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            return True
            
        except Exception as e:
            print(f"❌ Error updating {file_path}: {e}")
            return False

    def rename_database_files(self, new_underscore: str) -> List[str]:
        """Rename database files"""
        renamed_files = []
        
        for db_file_path in glob.glob(str(self.project_root / "sora_ai*.db")):
            db_file = Path(db_file_path)
            old_name = db_file.name
            new_name = old_name.replace("sora_ai", new_underscore)
            new_path = db_file.parent / new_name
            
            try:
                shutil.move(str(db_file), str(new_path))
                renamed_files.append(f"{old_name} → {new_name}")
            except Exception as e:
                print(f"❌ Error renaming {old_name}: {e}")
        
        return renamed_files

    def create_directory_rename_script(self, new_name: str) -> str:
        """Create bash script to rename the project directory"""
        script_content = f"""#!/bin/bash

# Project Directory Rename Script
# Generated by rename_project.py

echo "🚀 Renaming project directory..."
echo "Current: /var/projects/{self.current_name}"
echo "New:     /var/projects/{new_name}"
echo ""

# Check if current directory exists
if [ ! -d "/var/projects/{self.current_name}" ]; then
    echo "❌ Source directory /var/projects/{self.current_name} does not exist"
    exit 1
fi

# Check if target directory already exists
if [ -d "/var/projects/{new_name}" ]; then
    echo "❌ Target directory /var/projects/{new_name} already exists"
    echo "Please remove it first or choose a different name"
    exit 1
fi

# Perform the rename
echo "📁 Moving directory..."
mv "/var/projects/{self.current_name}" "/var/projects/{new_name}"

if [ $? -eq 0 ]; then
    echo "✅ Directory successfully renamed!"
    echo "New location: /var/projects/{new_name}"
    echo ""
    echo "Next steps:"
    echo "1. cd /var/projects/{new_name}"
    echo "2. Update any IDE/editor workspace settings"
    echo "3. Update any deployment scripts or CI/CD pipelines"
    echo "4. Update any symlinks or shortcuts"
    echo "5. Update any git remote URLs if this is a git repository"
else
    echo "❌ Failed to rename directory"
    exit 1
fi
"""
        
        script_path = self.project_root / "rename_directory.sh"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make script executable
        os.chmod(script_path, 0o755)
        
        return str(script_path)

    def perform_rename(self, new_name: str, new_title: str, new_underscore: str) -> None:
        """Perform the actual renaming"""
        print(f"\n🔄 Starting project rename...")
        
        # Update key files
        updated_files = []
        failed_files = []
        
        for file_path in self.key_files:
            full_path = self.project_root / file_path
            if self.update_file_content(full_path, new_name, new_title, new_underscore):
                if full_path.exists():
                    updated_files.append(str(file_path))
            else:
                failed_files.append(str(file_path))
        
        # Also update additional files that might contain references
        additional_files = []
        extensions = ['.py', '.html', '.js', '.json', '.md', '.txt', '.yml', '.yaml']
        skip_dirs = {'__pycache__', '.git', 'node_modules', 'venv', 'env', '.env', 'user_profiles', 'learning_data', 'rejection_data'}
        
        for root, dirs, files in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for file in files:
                file_path = Path(root) / file
                if any(file.endswith(ext) for ext in extensions):
                    rel_path = file_path.relative_to(self.project_root)
                    if str(rel_path) not in self.key_files:
                        if self.update_file_content(file_path, new_name, new_title, new_underscore):
                            # Check if file actually contained references and was updated
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if new_name in content or new_title in content or new_underscore in content:
                                    additional_files.append(str(rel_path))
        
        # Rename database files
        renamed_db_files = self.rename_database_files(new_underscore)
        
        # Create directory rename script
        script_path = self.create_directory_rename_script(new_name)
        
        # Report results
        print(f"\n✅ Rename operation completed!")
        print("=" * 50)
        
        if updated_files:
            print(f"📝 Updated {len(updated_files)} key files:")
            for file_path in updated_files:
                print(f"  ✓ {file_path}")
        
        if additional_files:
            print(f"\n📝 Updated {len(additional_files)} additional files:")
            for file_path in additional_files[:10]:  # Show first 10
                print(f"  ✓ {file_path}")
            if len(additional_files) > 10:
                print(f"  ... and {len(additional_files) - 10} more files")
        
        if renamed_db_files:
            print(f"\n🗄️ Renamed {len(renamed_db_files)} database files:")
            for rename_info in renamed_db_files:
                print(f"  ✓ {rename_info}")
        
        if failed_files:
            print(f"\n❌ Failed to update {len(failed_files)} files:")
            for file_path in failed_files:
                print(f"  ✗ {file_path}")
        
        print(f"\n📜 Directory rename script created: {script_path}")
        print(f"\nTo complete the rename, run:")
        print(f"  bash {script_path}")
        
        print(f"\n🎉 Project successfully renamed from '{self.current_name}' to '{new_name}'!")

    def confirm_operation(self, new_name: str, new_title: str, new_underscore: str) -> bool:
        """Ask user to confirm the operation"""
        print(f"\n⚠️  This will make permanent changes to your project!")
        print("   Make sure you have backups if needed.")
        
        while True:
            response = input("\nProceed with renaming? (y/N): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no', '']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no")

    def run(self) -> None:
        """Main execution flow"""
        try:
            # Display options
            self.display_suggestions()
            
            # Get user choice
            new_name, new_title, new_underscore = self.get_user_choice()
            
            # Preview changes
            self.preview_changes(new_name, new_title, new_underscore)
            
            # Confirm operation
            if not self.confirm_operation(new_name, new_title, new_underscore):
                print("\n👋 Operation cancelled by user")
                return
            
            # Perform rename
            self.perform_rename(new_name, new_title, new_underscore)
            
        except KeyboardInterrupt:
            print("\n\n👋 Operation cancelled by user")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("Please check the error and try again")

def main():
    """Entry point"""
    # Check if we're in the right directory
    current_dir = Path.cwd()
    project_root = Path("/var/projects/sora-ai-exploration")
    
    if not project_root.exists():
        print(f"❌ Project directory not found: {project_root}")
        print("Please make sure you're running this from the correct location")
        return
    
    renamer = ProjectRenamer(str(project_root))
    renamer.run()

if __name__ == "__main__":
    main()