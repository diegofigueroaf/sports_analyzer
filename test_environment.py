#!/usr/bin/env python3
"""
Environment Setup Test Script
Tests all components of the development environment
"""

import sys
import subprocess
import importlib.util

def test_python_version():
    """Test Python version"""
    print("🔍 Testing Python version...")
    version = sys.version_info
    print(f"   Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("   ✅ Python version OK")
        return True
    else:
        print("   ❌ Python version too old (need 3.8+)")
        return False

def test_package_imports():
    """Test if required packages can be imported"""
    print("\n🔍 Testing package imports...")
    
    # Core packages (required)
    core_packages = [
        'requests',
        'bs4',  # beautifulsoup4
        'dotenv',  # python-dotenv
    ]
    
    # Optional packages (nice to have)
    optional_packages = [
        'pandas',
        'numpy',
        'sklearn',
        'fastapi',
    ]
    
    core_success = True
    optional_success = 0
    
    print("   Core packages:")
    for package in core_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (REQUIRED)")
            core_success = False
    
    print("   Optional packages:")
    for package in optional_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
            optional_success += 1
        except ImportError:
            print(f"   ⚠️  {package} (optional)")
    
    print(f"   Optional packages installed: {optional_success}/{len(optional_packages)}")
    
    return core_success

def test_directory_structure():
    """Test if directory structure exists"""
    print("\n🔍 Testing directory structure...")
    
    import os
    
    required_dirs = [
        'backend',
        'frontend', 
        'data',
        'config',
        'tests',
        'scripts'
    ]
    
    all_dirs_exist = True
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ❌ {dir_name}/ (missing)")
            all_dirs_exist = False
    
    return all_dirs_exist

def test_git_setup():
    """Test Git configuration"""
    print("\n🔍 Testing Git setup...")
    
    try:
        # Check if git is initialized
        result = subprocess.run(['git', 'status'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Git repository initialized")
        else:
            print("   ❌ Git repository not initialized")
            return False
        
        # Check git config
        name_result = subprocess.run(['git', 'config', 'user.name'], 
                                   capture_output=True, text=True)
        email_result = subprocess.run(['git', 'config', 'user.email'], 
                                    capture_output=True, text=True)
        
        if name_result.stdout.strip() and email_result.stdout.strip():
            print(f"   ✅ Git configured for: {name_result.stdout.strip()}")
        else:
            print("   ⚠️  Git user not configured")
        
        return True
        
    except FileNotFoundError:
        print("   ❌ Git not installed")
        return False

def main():
    """Run all environment tests"""
    print("🏈 Sports Betting Analytics - Environment Test")
    print("=" * 50)
    
    tests = [
        test_python_version(),
        test_package_imports(),
        test_directory_structure(),
        test_git_setup()
    ]
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = sum(tests)
    total = len(tests)
    
    print(f"   Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 Environment setup complete!")
        print("   Ready to start development!")
    else:
        print("\n⚠️  Some tests failed.")
        print("   Please fix issues before continuing.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)