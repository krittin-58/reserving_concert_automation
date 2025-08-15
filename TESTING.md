# Testing Guide - Ticket Booking Automation

## 🧪 Step-by-Step Testing Instructions

### Prerequisites
1. **Python 3.8+** installed
2. **Google Chrome** browser (latest version)
3. **Valid accounts** on target websites
4. **Test concert events** available for booking

---

## 📋 Phase 1: Environment Setup

### Step 1: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python -c "import selenium; print('Selenium version:', selenium.__version__)"
```

### Step 2: Verify Chrome Driver
```bash
# Test Chrome driver setup
python test_setup.py
```

### Step 3: Configure Test Data
```bash
# Copy example config
cp userdetail.json userdetail_test.json

# Edit with your test credentials
# Use REAL credentials but select EXPIRED or TEST events
```

---

## 🔍 Phase 2: Component Testing

### Step 1: Test Website Connectivity
```bash
# Test each website individually
python test_connectivity.py --website thaiticketmajor
python test_connectivity.py --website ticketmelon  
python test_connectivity.py --website eventpop
```

### Step 2: Test Login Functionality
```bash
# Test login without booking
python test_login.py --website thaiticketmajor --dry-run
```

### Step 3: Test Concert Search
```bash
# Test finding concerts
python test_search.py --website thaiticketmajor --concert "test concert"
```

---

## 🎯 Phase 3: Integration Testing

### Step 1: Dry Run Mode
```bash
# Run full process without actual booking
python ticket_automation.py --dry-run --website thaiticketmajor
```

### Step 2: Test with Expired Events
```bash
# Use expired/sold-out events for safe testing
python ticket_automation.py --website thaiticketmajor
```

### Step 3: Test Error Handling
```bash
# Test with invalid credentials
python test_error_handling.py
```

---

## 🛡️ Phase 4: Safety Testing

### Step 1: Test Timeout Handling
- Disconnect internet during process
- Verify graceful timeout handling
- Check browser cleanup

### Step 2: Test Interruption Recovery
- Stop process mid-execution (Ctrl+C)
- Verify no hanging processes
- Check browser cleanup

### Step 3: Test Rate Limiting
- Run multiple instances
- Verify proper delays
- Check for IP blocking

---

## 📊 Phase 5: Performance Testing

### Step 1: Speed Testing
```bash
# Measure execution time
python test_performance.py --website thaiticketmajor --iterations 5
```

### Step 2: Memory Usage
```bash
# Monitor memory consumption
python test_memory.py --website thaiticketmajor
```

### Step 3: Browser Resource Usage
- Monitor CPU usage during execution
- Check memory leaks
- Verify proper cleanup

---

## 🎪 Phase 6: Live Testing (CAREFUL!)

### ⚠️ **IMPORTANT WARNINGS:**
- **Use test accounts only**
- **Select cheap/free events**
- **Have payment method ready to cancel**
- **Test during off-peak hours**
- **Never test on high-demand events**

### Step 1: Select Safe Test Event
```json
{
    "email": "test@example.com",
    "pwd": "testpassword",
    "concert": "FREE_TEST_EVENT_2024",
    "zone": "FREE",
    "show": "1", 
    "seats": "1",
    "website": "thaiticketmajor"
}
```

### Step 2: Monitor Live Execution
```bash
# Run with verbose logging
python ticket_automation.py --verbose --website thaiticketmajor
```

### Step 3: Manual Verification
1. **Watch browser actions** in real-time
2. **Verify each step** completes correctly
3. **Cancel booking** before payment if needed
4. **Check account** for any charges

---

## 🔧 Troubleshooting Common Issues

### Issue 1: Chrome Driver Problems
```bash
# Update Chrome driver
pip install --upgrade webdriver-manager

# Check Chrome version
google-chrome --version
```

### Issue 2: Element Not Found
```bash
# Run element inspector
python debug_elements.py --website thaiticketmajor --page login
```

### Issue 3: Timeout Errors
```bash
# Test with increased timeouts
python ticket_automation.py --timeout 60 --website thaiticketmajor
```

### Issue 4: Login Failures
```bash
# Test login separately
python test_login.py --website thaiticketmajor --debug
```

---

## 📝 Test Checklist

### Before Each Test:
- [ ] Chrome browser updated
- [ ] Test credentials verified
- [ ] Internet connection stable
- [ ] No other automation running
- [ ] Test event selected (not real booking)

### During Testing:
- [ ] Monitor console output
- [ ] Watch browser actions
- [ ] Check for error messages
- [ ] Verify each step completion
- [ ] Note any unusual behavior

### After Testing:
- [ ] Browser closed properly
- [ ] No hanging processes
- [ ] Check account for charges
- [ ] Review log files
- [ ] Document any issues

---

## 🚨 Emergency Procedures

### If Booking Goes Wrong:
1. **Immediately close browser**
2. **Check account transactions**
3. **Contact website support**
4. **Cancel any pending bookings**
5. **Review automation logs**

### If System Hangs:
```bash
# Kill all Chrome processes
pkill -f chrome

# Kill Python processes
pkill -f python

# Clean up temp files
rm -rf /tmp/chrome*
```

---

## 📈 Success Criteria

### Component Tests:
- ✅ All dependencies install correctly
- ✅ Chrome driver works
- ✅ Website connectivity established
- ✅ Login successful
- ✅ Concert search works

### Integration Tests:
- ✅ Full dry-run completes
- ✅ Error handling works
- ✅ Timeout handling works
- ✅ Browser cleanup works

### Performance Tests:
- ✅ Execution time < 5 minutes
- ✅ Memory usage < 500MB
- ✅ No memory leaks
- ✅ Proper resource cleanup

---

## 📞 Support

If you encounter issues:
1. **Check logs** in console output
2. **Review this testing guide**
3. **Test individual components**
4. **Use debug mode** for detailed info
5. **Document the issue** with screenshots

**Remember: Always test responsibly and never on high-demand events!**