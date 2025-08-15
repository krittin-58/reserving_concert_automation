"""Handler for Ticket Melon website"""

from selenium.webdriver.common.by import By
from .base_handler import BaseTicketHandler
from time import sleep


class TicketMelonHandler(BaseTicketHandler):
    def __init__(self, driver, config, user_details):
        super().__init__(driver, config, user_details)
        self.seat_count = 0
        
    def login(self):
        """Login to Ticket Melon"""
        login_selectors = self.config["login_selectors"]
        
        # Click login button
        self.click_element_safe(By.XPATH, login_selectors["login_button"])
        sleep(1)
        
        # Enter credentials
        username = self.find_element_safe(By.NAME, login_selectors["username_field"])
        if username:
            username.send_keys(self.user_details["email"])
            
        password = self.find_element_safe(By.NAME, login_selectors["password_field"])
        if password:
            password.send_keys(self.user_details["pwd"])
            
        # Submit login
        self.click_element_safe(By.XPATH, login_selectors["submit_button"])
        sleep(2)
        
    def search_concert(self):
        """Search for concert on Ticket Melon"""
        concert_name = self.user_details["concert"]
        
        # Use search functionality or browse events
        search_box = self.find_element_safe(By.NAME, "search")
        if search_box:
            search_box.send_keys(concert_name)
            search_box.submit()
        else:
            # Browse for concert link
            try:
                concert_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, concert_name)
                concert_link.click()
            except:
                print(f"Concert '{concert_name}' not found on Ticket Melon")
                
    def select_show(self):
        """Select show on Ticket Melon"""
        show_num = int(self.user_details["show"])
        booking_selectors = self.config["booking_selectors"]
        
        # Find available show times
        shows = self.driver.find_elements(By.XPATH, booking_selectors["show_selector"])
        
        if show_num <= len(shows) and show_num > 0:
            shows[show_num - 1].click()
            sleep(2)
            
    def select_zone(self, zone=None):
        """Select zone on Ticket Melon"""
        if zone is None:
            zone = self.user_details["zone"]
            
        booking_selectors = self.config["booking_selectors"]
        
        # Find zone options
        zones = self.driver.find_elements(By.XPATH, booking_selectors["zone_selector"])
        
        for zone_element in zones:
            if zone.lower() in zone_element.text.lower():
                zone_element.click()
                sleep(1)
                break
                
    def select_seats(self):
        """Select seats on Ticket Melon"""
        seats_needed = int(self.user_details["seats"])
        self.seat_count = 0
        
        booking_selectors = self.config["booking_selectors"]
        
        # Find available seats
        seats = self.driver.find_elements(By.XPATH, booking_selectors["seat_selector"])
        
        for seat in seats:
            if "available" in seat.get_attribute("class").lower() and self.seat_count < seats_needed:
                seat.click()
                self.seat_count += 1
                sleep(0.5)
                
                if self.seat_count == seats_needed:
                    break
                    
        return self.seat_count > 0
        
    def confirm_booking(self):
        """Confirm booking on Ticket Melon"""
        if self.seat_count > 0:
            booking_selectors = self.config["booking_selectors"]
            
            # Click confirm button
            self.click_element_safe(By.XPATH, booking_selectors["confirm_button"])
            sleep(3)
            
            print("Ticket Melon booking confirmed!")
            return True
        return False