#!/usr/bin/env python3
"""
Generate a clean conda environment file without build strings
for better cross-platform compatibility.
"""

import subprocess
import yaml
import sys
import re

def get_conda_list():
    """Get list of conda packages."""
    try:
        result = subprocess.run(['conda', 'list', '--export'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        print(f"Error getting conda list: {e}")
        return []

def clean_package_spec(package_line):
    """Remove build strings from package specification."""
    if package_line.startswith('#') or not package_line.strip():
        return None
    
    # Split package specification
    parts = package_line.split('=')
    if len(parts) >= 2:
        # Keep only name and version, remove build string
        return f"{parts[0]}={parts[1]}"
    return package_line

def get_environment_name():
    """Get current environment name."""
    try:
        result = subprocess.run(['conda', 'info', '--json'], 
                              capture_output=True, text=True, check=True)
        import json
        info = json.loads(result.stdout)
        active_env = info.get('active_prefix', '')
        if active_env:
            return active_env.split('\\')[-1] if '\\' in active_env else active_env.split('/')[-1]
        return 'smart_recon2'
    except:
        return 'smart_recon2'

def create_clean_environment_yml():
    """Create a clean environment.yml file."""
    packages = get_conda_list()
    conda_packages = []
    pip_packages = []
    
    in_pip_section = False
    
    for line in packages:
        if line.strip().startswith('# pip'):
            in_pip_section = True
            continue
        elif line.startswith('#'):
            continue
        
        if in_pip_section:
            # This is a pip package
            if '==' in line:
                pip_packages.append(line)
        else:
            # This is a conda package
            clean_spec = clean_package_spec(line)
            if clean_spec and not clean_spec.startswith('pip='):
                conda_packages.append(clean_spec)
    
    # Create environment structure
    env_data = {
        'name': get_environment_name(),
        'channels': [
            'conda-forge',
            'defaults'
        ],
        'dependencies': conda_packages
    }
    
    # Add pip section if there are pip packages
    if pip_packages:
        env_data['dependencies'].append({'pip': pip_packages})
    
    return env_data

def main():
    """Main function to generate clean environment file."""
    print("🔧 Generating clean environment file...")
    
    env_data = create_clean_environment_yml()
    
    # Write to file
    output_file = 'environment_clean.yml'
    with open(output_file, 'w') as f:
        yaml.dump(env_data, f, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Clean environment file created: {output_file}")
    print(f"📦 Found {len(env_data['dependencies'])} dependencies")
    
    # Check for pip packages
    pip_deps = [dep for dep in env_data['dependencies'] if isinstance(dep, dict) and 'pip' in dep]
    if pip_deps:
        pip_count = len(pip_deps[0]['pip'])
        print(f"🐍 Including {pip_count} pip packages")
    
    print(f"\n📋 To recreate this environment:")
    print(f"   conda env create -f {output_file}")

if __name__ == "__main__":
    main()
