#!/usr/bin/env python3
"""
Test script to verify environment setup
"""

import sys
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import os


def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires 3.8+")
        return False


def test_selenium_import():
    """Test Selenium import"""
    print("\n🔧 Testing Selenium import...")
    try:
        import selenium
        print(f"✅ Selenium {selenium.__version__} - Imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Selenium import failed: {e}")
        return False


def test_chrome_driver():
    """Test Chrome WebDriver setup"""
    print("\n🌐 Testing Chrome WebDriver...")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ Chrome WebDriver - Working (loaded: {title})")
        return True
    except Exception as e:
        print(f"❌ Chrome WebDriver failed: {e}")
        print("💡 Try: pip install webdriver-manager")
        return False


def test_config_files():
    """Test configuration files"""
    print("\n📁 Testing configuration files...")
    
    required_files = [
        "config.py",
        "userdetail.json",
        "ticket_automation.py"
    ]
    
    all_good = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - Missing")
            all_good = False
    
    return all_good


def test_json_config():
    """Test JSON configuration validity"""
    print("\n📋 Testing JSON configuration...")
    try:
        with open("userdetail.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_keys = ["email", "pwd", "concert", "zone", "show", "seats"]
        missing_keys = [key for key in required_keys if key not in config]
        
        if missing_keys:
            print(f"❌ Missing keys in userdetail.json: {missing_keys}")
            return False
        else:
            print("✅ userdetail.json - Valid structure")
            return True
            
    except FileNotFoundError:
        print("❌ userdetail.json - File not found")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ userdetail.json - Invalid JSON: {e}")
        return False


def test_website_handlers():
    """Test website handler imports"""
    print("\n🏗️ Testing website handlers...")
    try:
        from website_handlers import ThaiTicketMajorHandler, TicketMelonHandler, EventpopHandler
        print("✅ Website handlers - All imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Website handlers import failed: {e}")
        return False


def main():
    """Run all setup tests"""
    print("🧪 TICKET AUTOMATION - SETUP TESTING")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Selenium Import", test_selenium_import),
        ("Chrome WebDriver", test_chrome_driver),
        ("Configuration Files", test_config_files),
        ("JSON Configuration", test_json_config),
        ("Website Handlers", test_website_handlers)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} - Exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System ready for automation.")
        return True
    else:
        print("⚠️ Some tests failed. Please fix issues before proceeding.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)