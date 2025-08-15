# Multi-Website Ticket Booking Automation
Automated ticket booking for multiple Thai ticketing websites

## Supported Websites
- **Thai Ticket Major** (thaiticketmajor.com)
- **Ticket Melon** (ticketmelon.com) 
- **Eventpop** (eventpop.me)

## Installation
1. **Python 3.8+** - [Download here](https://www.python.org/downloads/)

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Chrome WebDriver** (automatically managed by webdriver-manager)

## Configuration
Edit `userdetail.json` with your booking details:

```json
{
    "email": "your-email@example.com",
    "pwd": "your-password",
    "concert": "Concert Name",
    "zone": "Zone Code (e.g., BR, VIP)",
    "show": "1",
    "seats": "2",
    "website": "thaiticketmajor"
}
```

### Website-Specific Notes

**Thai Ticket Major:**
- Use exact concert name as shown on website
- Zone codes: BR, VIP, A, B, C, etc.
- Show number starts from 1

**Ticket Melon:**
- Concert name can be partial match
- Zone names are usually descriptive (e.g., "Standing", "Seated")

**Eventpop:**
- Uses ticket types instead of zones
- Quantity-based selection for most events

## Usage

### Interactive Mode
```bash
python ticket_automation.py
```

### Direct Mode (Legacy)
```bash
python reserve.py  # Thai Ticket Major only
```

## Features
- ✅ Multi-website support
- ✅ Automatic login and navigation
- ✅ Smart seat selection
- ✅ Alternative zone fallback (Thai Ticket Major)
- ✅ Error handling and retry logic
- ✅ Modern Selenium 4 compatibility
- ✅ Configurable wait times

## Adding New Websites

1. **Add website configuration** in `config.py`
2. **Create handler class** in `website_handlers/`
3. **Implement required methods** from `BaseTicketHandler`
4. **Register handler** in `ticket_automation.py`

Example handler structure:
```python
class NewSiteHandler(BaseTicketHandler):
    def login(self): pass
    def search_concert(self): pass
    def select_show(self): pass
    def select_zone(self): pass
    def select_seats(self): pass
    def confirm_booking(self): pass
```

## Troubleshooting

**Common Issues:**
- **Element not found**: Website layout changed, update selectors in `config.py`
- **Login failed**: Check credentials and website-specific login flow
- **Timeout errors**: Increase wait times in `config.py`
- **Chrome driver issues**: Update Chrome browser

**Debug Mode:**
- Browser stays open after completion for manual verification
- Check console output for detailed error messages

## Legal Notice
This tool is for educational purposes. Users are responsible for:
- Complying with website terms of service
- Respecting rate limits and fair usage
- Not engaging in ticket scalping or reselling

## Contributing
1. Fork the repository
2. Create feature branch
3. Add new website handler
4. Test thoroughly
5. Submit pull request

## Architecture

```
ticket_automation.py          # Main orchestrator
├── config.py                 # Website configurations
├── website_handlers/         # Handler implementations
│   ├── base_handler.py      # Abstract base class
│   ├── thaiticketmajor_handler.py
│   ├── ticketmelon_handler.py
│   └── eventpop_handler.py
└── userdetail.json          # User configuration
```

## Version History
- **v2.0**: Multi-website support, modern Selenium 4
- **v1.0**: Thai Ticket Major only (legacy)

---
**Happy ticket hunting! 🎫**
