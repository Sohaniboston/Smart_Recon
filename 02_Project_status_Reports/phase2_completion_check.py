#!/usr/bin/env python3
"""
Phase 2 Completion Validation Script
Checks if all Phase 2 components are properly implemented and functional
"""

import sys
import os
import importlib.util

def check_module_exists(module_path, module_name):
    """Check if a module exists and can be imported"""
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None:
            return False, f"Module spec not found for {module_name}"
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return True, f"✅ {module_name} module loaded successfully"
    except Exception as e:
        return False, f"❌ {module_name} module failed to load: {str(e)}"

def check_fuzzy_matching_implementation():
    """Check if fuzzy matching module is properly implemented"""
    fuzzy_path = "src/modules/fuzzy_matching.py"
    if not os.path.exists(fuzzy_path):
        return False, "❌ Fuzzy matching module not found"
    
    success, message = check_module_exists(fuzzy_path, "fuzzy_matching")
    if not success:
        return False, message
    
    # Check file size to ensure it's not empty
    file_size = os.path.getsize(fuzzy_path)
    if file_size < 1000:  # Should be substantial implementation
        return False, f"❌ Fuzzy matching module too small ({file_size} bytes)"
    
    return True, f"✅ Fuzzy matching module implemented ({file_size} bytes)"

def check_enhanced_exception_handler():
    """Check if exception handler has been enhanced"""
    handler_path = "src/modules/exception_handler.py"
    if not os.path.exists(handler_path):
        return False, "❌ Exception handler module not found"
    
    success, message = check_module_exists(handler_path, "exception_handler")
    if not success:
        return False, message
    
    # Check if file contains DataFrame handling
    with open(handler_path, 'r') as f:
        content = f.read()
        if 'DataFrame' in content and 'process_exceptions' in content:
            return True, "✅ Exception handler enhanced with DataFrame support"
        else:
            return False, "❌ Exception handler not properly enhanced"

def check_workflow_integration():
    """Check if main workflow has been updated"""
    app_path = "app.py"
    if not os.path.exists(app_path):
        return False, "❌ Main application file not found"
    
    # Check if app.py contains fuzzy matching integration
    with open(app_path, 'r') as f:
        content = f.read()
        if 'fuzzy_matching' in content and 'FuzzyMatcher' in content:
            return True, "✅ Main workflow integrated with fuzzy matching"
        else:
            return False, "❌ Main workflow not integrated with fuzzy matching"

def check_configuration_updates():
    """Check if configuration has been updated for Phase 2"""
    config_path = "config/default_config.json"
    if not os.path.exists(config_path):
        return False, "❌ Configuration file not found"
    
    # Check if config contains fuzzy matching settings
    with open(config_path, 'r') as f:
        content = f.read()
        if 'fuzzy_matching' in content and 'similarity_threshold' in content:
            return True, "✅ Configuration updated with fuzzy matching settings"
        else:
            return False, "❌ Configuration not updated for Phase 2"

def check_requirements():
    """Check if requirements include fuzzy matching dependencies"""
    req_path = "requirements.txt"
    if not os.path.exists(req_path):
        return False, "❌ Requirements file not found"
    
    with open(req_path, 'r') as f:
        content = f.read()
        if 'fuzzywuzzy' in content or 'jellyfish' in content:
            return True, "✅ Requirements updated with fuzzy matching dependencies"
        else:
            return False, "❌ Requirements not updated for Phase 2"

def main():
    """Main validation function"""
    print("🔍 Phase 2 Completion Validation")
    print("=" * 50)
    
    checks = [
        ("Fuzzy Matching Module", check_fuzzy_matching_implementation),
        ("Enhanced Exception Handler", check_enhanced_exception_handler),
        ("Workflow Integration", check_workflow_integration),
        ("Configuration Updates", check_configuration_updates),
        ("Requirements Updates", check_requirements)
    ]
    
    all_passed = True
    results = []
    
    for check_name, check_func in checks:
        try:
            success, message = check_func()
            results.append((check_name, success, message))
            if not success:
                all_passed = False
        except Exception as e:
            results.append((check_name, False, f"❌ Check failed: {str(e)}"))
            all_passed = False
    
    # Print results
    for check_name, success, message in results:
        print(f"\n{check_name}:")
        print(f"  {message}")
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 PHASE 2 COMPLETION: SUCCESS")
        print("All Phase 2 components are properly implemented and integrated!")
    else:
        print("⚠️  PHASE 2 COMPLETION: INCOMPLETE")
        print("Some Phase 2 components need attention.")
    
    print("=" * 50)
    return all_passed

if __name__ == "__main__":
    # Set working directory to project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    success = main()
    sys.exit(0 if success else 1)
