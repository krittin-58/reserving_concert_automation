#!/usr/bin/env python3
"""
Test website connectivity and basic navigation
"""

import sys
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import WEBSITES
import time


def test_website_connectivity(website_name):
    """Test basic connectivity to website"""
    print(f"🌐 Testing connectivity to {website_name}...")
    
    if website_name not in WEBSITES:
        print(f"❌ Website '{website_name}' not supported")
        return False
    
    config = WEBSITES[website_name]
    
    # Setup Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        
        # Test basic page load
        print(f"📡 Connecting to {config['base_url']}...")
        start_time = time.time()
        driver.get(config['base_url'])
        load_time = time.time() - start_time
        
        print(f"✅ Page loaded in {load_time:.2f} seconds")
        print(f"📄 Page title: {driver.title}")
        
        # Test if login elements exist
        login_selectors = config['login_selectors']
        login_button_xpath = login_selectors['login_button']
        
        try:
            login_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, login_button_xpath))
            )
            print("✅ Login button found - Website structure intact")
        except:
            print("⚠️ Login button not found - Website may have changed")
        
        # Test page responsiveness
        print("🔄 Testing page responsiveness...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        
        print("✅ Website connectivity test passed")
        return True
        
    except Exception as e:
        print(f"❌ Connectivity test failed: {e}")
        return False
        
    finally:
        if driver:
            driver.quit()


def test_all_websites():
    """Test connectivity to all supported websites"""
    print("🌍 Testing all supported websites...")
    print("=" * 50)
    
    results = {}
    for website_name in WEBSITES.keys():
        print(f"\n🎯 Testing {WEBSITES[website_name]['name']}...")
        results[website_name] = test_website_connectivity(website_name)
        time.sleep(2)  # Be respectful with requests
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 CONNECTIVITY TEST SUMMARY")
    print("=" * 50)
    
    for website, result in results.items():
        status = "✅ ONLINE" if result else "❌ OFFLINE"
        print(f"{status} - {WEBSITES[website]['name']} ({website})")
    
    passed = sum(results.values())
    total = len(results)
    print(f"\n🎯 Results: {passed}/{total} websites accessible")
    
    return passed == total


def main():
    parser = argparse.ArgumentParser(description='Test website connectivity')
    parser.add_argument('--website', help='Specific website to test')
    parser.add_argument('--all', action='store_true', help='Test all websites')
    
    args = parser.parse_args()
    
    if args.website:
        success = test_website_connectivity(args.website)
    elif args.all:
        success = test_all_websites()
    else:
        print("Available websites:")
        for key, value in WEBSITES.items():
            print(f"  - {key}: {value['name']}")
        
        website = input("\nEnter website to test (or 'all' for all): ").strip().lower()
        
        if website == 'all':
            success = test_all_websites()
        else:
            success = test_website_connectivity(website)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()