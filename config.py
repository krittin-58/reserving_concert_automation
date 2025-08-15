"""Configuration settings for ticket booking automation"""

# Supported websites configuration
WEBSITES = {
    "thaiticketmajor": {
        "base_url": "https://www.thaiticketmajor.com/concert/",
        "name": "Thai Ticket Major",
        "login_selectors": {
            "login_button": "//*[@class='btn-signin item d-none d-lg-inline-block']",
            "username_field": "username",
            "password_field": "password",
            "submit_button": "//button[@class='btn-red btn-signin']"
        },
        "booking_selectors": {
            "concert_link": "partial_link_text",
            "show_selector": "//div[@class='box-event-list']/div[2]/div[{show}]/div[2]/span[1]/a[1]",
            "zone_map": "//*[@name='uMap2Map']/area",
            "seat_table": "//*[@id='tableseats']/tbody[1]/tr",
            "confirm_button": "ยืนยันที่นั่ง / Book Now"
        }
    },
    "ticketmelon": {
        "base_url": "https://www.ticketmelon.com/",
        "name": "Ticket Melon",
        "login_selectors": {
            "login_button": "//a[contains(@class, 'login')]",
            "username_field": "email",
            "password_field": "password",
            "submit_button": "//button[@type='submit']"
        },
        "booking_selectors": {
            "concert_link": "partial_link_text",
            "show_selector": "//div[contains(@class, 'show-time')]",
            "zone_selector": "//div[contains(@class, 'zone')]",
            "seat_selector": "//div[contains(@class, 'seat')]",
            "confirm_button": "//button[contains(text(), 'Confirm')]"
        }
    },
    "eventpop": {
        "base_url": "https://www.eventpop.me/",
        "name": "Eventpop",
        "login_selectors": {
            "login_button": "//button[contains(text(), 'เข้าสู่ระบบ')]",
            "username_field": "email",
            "password_field": "password",
            "submit_button": "//button[contains(@class, 'login-btn')]"
        },
        "booking_selectors": {
            "concert_link": "partial_link_text",
            "show_selector": "//div[contains(@class, 'event-session')]",
            "zone_selector": "//div[contains(@class, 'ticket-type')]",
            "seat_selector": "//button[contains(@class, 'seat')]",
            "confirm_button": "//button[contains(text(), 'จองตั๋ว')]"
        }
    }
}

# Default settings
DEFAULT_WAIT_TIME = 30
MAX_RETRY_ATTEMPTS = 3
IMPLICIT_WAIT = 30