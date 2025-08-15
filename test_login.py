#!/usr/bin/env python3
"""
Test login functionality for ticket booking websites
"""

import sys
import argparse
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import WEBSITES
import time


def test_login(website_name, dry_run=True, debug=False):
    """Test login functionality"""
    print(f"🔐 Testing login for {website_name}...")
    
    if website_name not in WEBSITES:
        print(f"❌ Website '{website_name}' not supported")
        return False
    
    # Load user details
    try:
        with open('userdetail.json', 'r', encoding='utf-8') as f:
            user_details = json.load(f)
    except FileNotFoundError:
        print("❌ userdetail.json not found")
        return False
    
    config = WEBSITES[website_name]
    
    # Setup Chrome driver
    chrome_options = Options()
    if not debug:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(30)
        
        # Navigate to website
        print(f"📡 Navigating to {config['base_url']}...")
        driver.get(config['base_url'])
        
        if debug:
            print("🔍 Debug mode: Browser will stay open for inspection")
            input("Press Enter to continue with login test...")
        
        # Find and click login button
        login_selectors = config['login_selectors']
        print("🔍 Looking for login button...")
        
        login_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, login_selectors['login_button']))
        )
        print("✅ Login button found")
        
        if dry_run:
            print("🏃 Dry run mode: Stopping before actual login")
            print("✅ Login elements accessible - Test passed")
            return True
        
        # Click login button
        login_button.click()
        time.sleep(2)
        
        # Find username field
        print("🔍 Looking for username field...")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, login_selectors['username_field']))
        )
        print("✅ Username field found")
        
        # Find password field
        print("🔍 Looking for password field...")
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, login_selectors['password_field']))
        )
        print("✅ Password field found")
        
        # Enter credentials (if not dry run)
        print("📝 Entering credentials...")
        username_field.send_keys(user_details['email'])
        password_field.send_keys(user_details['pwd'])
        
        # Find submit button
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, login_selectors['submit_button']))
        )
        print("✅ Submit button found")
        
        # Submit login
        current_url = driver.current_url
        submit_button.click()
        time.sleep(5)
        
        # Check if login was successful
        new_url = driver.current_url
        if new_url != current_url:
            print("✅ Login successful - URL changed")
            
            # Check for common success indicators
            success_indicators = [
                "logout", "profile", "account", "dashboard",
                "ออกจากระบบ", "โปรไฟล์"
            ]
            
            page_source = driver.page_source.lower()
            found_indicators = [ind for ind in success_indicators if ind in page_source]
            
            if found_indicators:
                print(f"✅ Login confirmed - Found indicators: {found_indicators}")
                return True
            else:
                print("⚠️ Login may have succeeded but no clear indicators found")
                return True
        else:
            print("❌ Login may have failed - URL unchanged")
            
            # Check for error messages
            error_indicators = [
                "error", "invalid", "incorrect", "failed",
                "ผิดพลาด", "ไม่ถูกต้อง"
            ]
            
            page_source = driver.page_source.lower()
            found_errors = [err for err in error_indicators if err in page_source]
            
            if found_errors:
                print(f"❌ Login failed - Found errors: {found_errors}")
            
            return False
        
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return False
        
    finally:
        if driver and not debug:
            driver.quit()
        elif debug:
            input("Press Enter to close browser...")
            driver.quit()


def main():
    parser = argparse.ArgumentParser(description='Test login functionality')
    parser.add_argument('--website', required=True, help='Website to test')
    parser.add_argument('--dry-run', action='store_true', help='Test without actual login')
    parser.add_argument('--debug', action='store_true', help='Run with browser visible')
    
    args = parser.parse_args()
    
    print("🧪 LOGIN FUNCTIONALITY TEST")
    print("=" * 50)
    
    if args.dry_run:
        print("⚠️ DRY RUN MODE: Will not perform actual login")
    
    success = test_login(args.website, args.dry_run, args.debug)
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Login test PASSED")
    else:
        print("💥 Login test FAILED")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()