#!/usr/bin/env python3
"""
Debug tool to inspect website elements and selectors
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


def debug_page_elements(website_name, page_type="main"):
    """Debug and inspect page elements"""
    print(f"🔍 Debugging elements for {website_name} - {page_type} page...")
    
    if website_name not in WEBSITES:
        print(f"❌ Website '{website_name}' not supported")
        return False
    
    config = WEBSITES[website_name]
    
    # Setup Chrome driver (visible for debugging)
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    
    try:
        # Navigate to website
        print(f"📡 Navigating to {config['base_url']}...")
        driver.get(config['base_url'])
        
        print("\n🎯 ELEMENT INSPECTION MODE")
        print("=" * 50)
        print("Browser is now open for manual inspection.")
        print("Use browser dev tools to inspect elements.")
        print("\nTesting configured selectors...")
        
        # Test login selectors
        if page_type in ["main", "login"]:
            print("\n🔐 Testing Login Selectors:")
            login_selectors = config['login_selectors']
            
            for selector_name, selector_value in login_selectors.items():
                print(f"\n🔍 Testing {selector_name}: {selector_value}")
                
                try:
                    if selector_name == 'username_field' or selector_name == 'password_field':
                        element = driver.find_element(By.ID, selector_value)
                    else:
                        element = driver.find_element(By.XPATH, selector_value)
                    
                    print(f"✅ Found: {element.tag_name}")
                    if element.text:
                        print(f"   Text: '{element.text[:50]}...'")
                    if element.get_attribute('class'):
                        print(f"   Class: '{element.get_attribute('class')}'")
                        
                except Exception as e:
                    print(f"❌ Not found: {e}")
        
        # Test booking selectors
        if page_type in ["main", "booking"]:
            print("\n🎫 Testing Booking Selectors:")
            booking_selectors = config['booking_selectors']
            
            for selector_name, selector_value in booking_selectors.items():
                print(f"\n🔍 Testing {selector_name}: {selector_value}")
                
                try:
                    elements = driver.find_elements(By.XPATH, selector_value)
                    print(f"✅ Found {len(elements)} elements")
                    
                    for i, element in enumerate(elements[:3]):  # Show first 3
                        print(f"   [{i+1}] {element.tag_name}")
                        if element.text:
                            print(f"       Text: '{element.text[:30]}...'")
                            
                except Exception as e:
                    print(f"❌ Not found: {e}")
        
        # Interactive mode
        print("\n" + "=" * 50)
        print("🎮 INTERACTIVE MODE")
        print("Commands:")
        print("  'find <xpath>' - Test XPath selector")
        print("  'click <xpath>' - Click element")
        print("  'text <xpath>' - Get element text")
        print("  'screenshot' - Take screenshot")
        print("  'quit' - Exit")
        
        while True:
            command = input("\n🔧 Enter command: ").strip()
            
            if command == 'quit':
                break
            elif command == 'screenshot':
                filename = f"debug_{website_name}_{int(time.time())}.png"
                driver.save_screenshot(filename)
                print(f"📸 Screenshot saved: {filename}")
            elif command.startswith('find '):
                xpath = command[5:]
                try:
                    elements = driver.find_elements(By.XPATH, xpath)
                    print(f"✅ Found {len(elements)} elements")
                    for i, elem in enumerate(elements[:5]):
                        print(f"   [{i+1}] {elem.tag_name} - '{elem.text[:50]}...'")
                except Exception as e:
                    print(f"❌ Error: {e}")
            elif command.startswith('click '):
                xpath = command[6:]
                try:
                    element = driver.find_element(By.XPATH, xpath)
                    element.click()
                    print("✅ Clicked successfully")
                except Exception as e:
                    print(f"❌ Click failed: {e}")
            elif command.startswith('text '):
                xpath = command[5:]
                try:
                    element = driver.find_element(By.XPATH, xpath)
                    print(f"📝 Text: '{element.text}'")
                except Exception as e:
                    print(f"❌ Error: {e}")
            else:
                print("❓ Unknown command")
        
        return True
        
    except Exception as e:
        print(f"❌ Debug session failed: {e}")
        return False
        
    finally:
        print("🔚 Debug session ended")
        # Don't auto-close in debug mode
        input("Press Enter to close browser...")
        driver.quit()


def main():
    parser = argparse.ArgumentParser(description='Debug website elements')
    parser.add_argument('--website', required=True, help='Website to debug')
    parser.add_argument('--page', default='main', 
                       choices=['main', 'login', 'booking'],
                       help='Page type to debug')
    
    args = parser.parse_args()
    
    print("🐛 ELEMENT DEBUGGING TOOL")
    print("=" * 50)
    
    success = debug_page_elements(args.website, args.page)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()