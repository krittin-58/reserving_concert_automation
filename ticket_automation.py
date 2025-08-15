"""
Multi-Website Ticket Booking Automation
Supports: Thai Ticket Major, Ticket Melon, Eventpop
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import sys
from config import WEBSITES
from website_handlers import ThaiTicketMajorHandler, TicketMelonHandler, EventpopHandler


class TicketBookingAutomation:
    def __init__(self, website_name, user_details_file="userdetail.json"):
        self.website_name = website_name.lower()
        self.user_details_file = user_details_file
        self.driver = None
        self.handler = None
        
        # Load user details
        try:
            with open(user_details_file, 'r', encoding='utf-8') as f:
                self.user_details = json.load(f)
        except FileNotFoundError:
            print(f"User details file '{user_details_file}' not found!")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Invalid JSON in '{user_details_file}'!")
            sys.exit(1)
            
        # Validate website support
        if self.website_name not in WEBSITES:
            print(f"Website '{website_name}' is not supported!")
            print(f"Supported websites: {', '.join(WEBSITES.keys())}")
            sys.exit(1)
            
        self.config = WEBSITES[self.website_name]
        
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        # Uncomment the next line for headless mode
        # chrome_options.add_argument("--headless")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def get_handler(self):
        """Get the appropriate website handler"""
        handlers = {
            "thaiticketmajor": ThaiTicketMajorHandler,
            "ticketmelon": TicketMelonHandler,
            "eventpop": EventpopHandler
        }
        
        handler_class = handlers.get(self.website_name)
        if handler_class:
            return handler_class(self.driver, self.config, self.user_details)
        else:
            raise ValueError(f"No handler found for {self.website_name}")
            
    def run_booking_process(self):
        """Run the complete booking process"""
        try:
            print(f"Starting ticket booking automation for {self.config['name']}...")
            
            # Setup
            self.setup_driver()
            self.handler = self.get_handler()
            self.handler.setup()
            
            # Login
            print("Logging in...")
            self.handler.login()
            
            # Search for concert
            print(f"Searching for concert: {self.user_details['concert']}")
            self.handler.search_concert()
            
            # Select show
            print(f"Selecting show #{self.user_details['show']}")
            self.handler.select_show()
            
            # Select zone
            print(f"Selecting zone: {self.user_details['zone']}")
            self.handler.select_zone()
            
            # Select seats
            print(f"Selecting {self.user_details['seats']} seats...")
            seats_selected = self.handler.select_seats()
            
            if not seats_selected:
                print("No seats available in preferred zone.")
                
                # Try alternative zones if handler supports it
                if hasattr(self.handler, 'find_alternative_zones'):
                    print("Trying alternative zones...")
                    if self.handler.find_alternative_zones():
                        seats_selected = True
                    
            if seats_selected:
                # Confirm booking
                print("Confirming booking...")
                success = self.handler.confirm_booking()
                
                if success:
                    print("✅ Booking completed successfully!")
                else:
                    print("❌ Booking confirmation failed!")
            else:
                print("❌ No seats could be selected!")
                
        except Exception as e:
            print(f"❌ An error occurred: {str(e)}")
            
        finally:
            # Keep browser open for manual verification
            input("Press Enter to close the browser...")
            if self.driver:
                self.driver.quit()


def main():
    """Main function"""
    print("🎫 Multi-Website Ticket Booking Automation")
    print("=" * 50)
    
    # Add testing mode argument
    import argparse
    parser = argparse.ArgumentParser(description='Ticket booking automation')
    parser.add_argument('--dry-run', action='store_true', help='Test mode without actual booking')
    parser.add_argument('--verbose', action='store_true', help='Verbose logging')
    parser.add_argument('--timeout', type=int, default=30, help='Timeout in seconds')
    parser.add_argument('--website', help='Website to use')
    
    args = parser.parse_args()
    
    # Show supported websites
    print("Supported websites:")
    for key, value in WEBSITES.items():
        print(f"  - {key}: {value['name']}")
    print()
    
    # Get website choice
    if args.website:
        website = args.website.lower()
    else:
        website = input("Enter website name: ").strip().lower()
    
    if not website:
        print("No website specified. Using default: thaiticketmajor")
        website = "thaiticketmajor"
    
    if args.dry_run:
        print("⚠️ DRY RUN MODE: No actual booking will be performed")
    
    # Run automation
    automation = TicketBookingAutomation(website)
    
    # Apply test settings
    if hasattr(automation, 'set_test_mode'):
        automation.set_test_mode(args.dry_run, args.verbose, args.timeout)
    
    automation.run_booking_process()


if __name__ == "__main__":
    main()