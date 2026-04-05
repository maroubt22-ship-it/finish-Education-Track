"""
Setup script to create the EduTrack IA project structure
"""
import os

# Create .github directory for copilot instructions
os.makedirs('.github', exist_ok=True)
print("✅ Created: .github")

# Define the directory structure
dirs = [
    'frontend',
    'frontend/streamlit',
    'frontend/streamlit/pages',
    'frontend/streamlit/components',
    'frontend/streamlit/utils',
    'frontend/gradio',
    'frontend/parent_view',
    'frontend/shared',
    'frontend/shared/data',
    'frontend/shared/styles'
]

# Create directories
for directory in dirs:
    os.makedirs(directory, exist_ok=True)
    print(f"✅ Created: {directory}")

# Create __init__.py files
init_files = [
    'frontend/__init__.py',
    'frontend/streamlit/__init__.py',
    'frontend/streamlit/components/__init__.py',
    'frontend/streamlit/utils/__init__.py',
    'frontend/shared/__init__.py',
    'frontend/shared/data/__init__.py',
    'frontend/shared/styles/__init__.py'
]

for init_file in init_files:
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(f"# {os.path.dirname(init_file)}\n")
    print(f"✅ Created: {init_file}")

print("\n🎉 Project structure created successfully!")
