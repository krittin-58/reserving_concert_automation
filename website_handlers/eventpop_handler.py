"""Handler for Eventpop website"""

from selenium.webdriver.common.by import By
from .base_handler import BaseTicketHandler
from time import sleep


class EventpopHandler(BaseTicketHandler):
    def __init__(self, driver, config, user_details):
        super().__init__(driver, config, user_details)
        self.seat_count = 0
        
    def login(self):
        """Login to Eventpop"""
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
        """Search for concert on Eventpop"""
        concert_name = self.user_details["concert"]
        
        # Search for event
        try:
            search_box = self.find_element_safe(By.NAME, "q")
            if search_box:
                search_box.send_keys(concert_name)
                search_box.submit()
                sleep(2)
                
                # Click on the event
                event_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, concert_name)
                event_link.click()
            else:
                # Direct link search
                concert_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, concert_name)
                concert_link.click()
        except:
            print(f"Concert '{concert_name}' not found on Eventpop")
            
    def select_show(self):
        """Select show on Eventpop"""
        show_num = int(self.user_details["show"])
        booking_selectors = self.config["booking_selectors"]
        
        # Find event sessions
        sessions = self.driver.find_elements(By.XPATH, booking_selectors["show_selector"])
        
        if show_num <= len(sessions) and show_num > 0:
            sessions[show_num - 1].click()
            sleep(2)
            
    def select_zone(self, zone=None):
        """Select ticket type/zone on Eventpop"""
        if zone is None:
            zone = self.user_details["zone"]
            
        booking_selectors = self.config["booking_selectors"]
        
        # Find ticket types
        ticket_types = self.driver.find_elements(By.XPATH, booking_selectors["zone_selector"])
        
        for ticket_type in ticket_types:
            if zone.lower() in ticket_type.text.lower():
                ticket_type.click()
                sleep(1)
                break
                
    def select_seats(self):
        """Select seats on Eventpop"""
        seats_needed = int(self.user_details["seats"])
        self.seat_count = 0
        
        # For Eventpop, usually quantity selection rather than individual seats
        quantity_input = self.find_element_safe(By.NAME, "quantity")
        if quantity_input:
            quantity_input.clear()
            quantity_input.send_keys(str(seats_needed))
            self.seat_count = seats_needed
        else:
            # If seat selection is available
            booking_selectors = self.config["booking_selectors"]
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
        """Confirm booking on Eventpop"""
        if self.seat_count > 0:
            booking_selectors = self.config["booking_selectors"]
            
            # Click booking button
            self.click_element_safe(By.XPATH, booking_selectors["confirm_button"])
            sleep(3)
            
            print("Eventpop booking confirmed!")
            return True
        return False