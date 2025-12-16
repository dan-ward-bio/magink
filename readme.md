# magi(n)k
## A few scripts to turn a Raspberry Pi and an e-ink display in to a dashboard e-photo frame / dashboard.

**Currently, the scripts perform four functions:**
1. **User photo slideshow**: configurable delay, image resolution parsing script.
2. **TFL bus countdown scrape**: button actuated, scrapes bus arrivals from TFL website without need for API key.
3. **Schedule view**: button actuated, downloads ICS formatted calendar from URL and renders list of engagements using [icalendar2fullcalendar](https://github.com/leonaard/icalendar2fullcalendar).
4. **Month calendar view**: button actuated, downloads ICS formatted calendar from URL and renders a month calendar.

**To be added:**
1. Weather dash

### Description


sudo apt-get install libopenblas-dev


### Equipment
* Pi Zero 2 W or greater.
* Inky Impression 7.3" (7 colour ePaper/E Ink HAT).
* Momentary buttons [like this from PiHut](https://thepihut.com/products/wired-self-adhesive-momentary-pushbutton)
* Photo frame.


### Software 
**Download and flash appropriate Raspian version [link to Pi imager](https://www.raspberrypi.com/software/):**
* Configure the Imager with you Wi-Fi settings etc.
* Install Raspian 32 bit (Full) - Be sure to get the *Full* version with additional software.

**Enable SPI and I2C:**
```raspi-config``` > interface options > enable SPI/I2C

**Download the correct software for your e-ink display from the Pimoroni website. For the Inky series:**
```curl https://get.pimoroni.com/inky | bash```

**Install firefox:**
```sudo apt-get install firefox-esr```

**Clone the e-ink tools repo:**
```git clone https://github.com/dan-ward-bio/eink_tools.git```

**Transfer your photos to the Pi and use ```python image_resize.py``` to resize your images for the e-ink display. Swap out the resolution appropriate for your display:**
```python ~/eink-tools/image_resize.py ~/photo_directory/ 800x480```


Make the launcher executable:
```chmod +x ~/eink-tools/launcher.py```

**Run launcher.py with the two positional arguments:**
```python ~/eink-tools/launcher.py <path_to_processed_photo_dir> <photo refresh (seconds) INT>```

eg.
```python ~/eink-tools/launcher.py ~/photos/processed 10000```

### Create a service for running the launcher on boot
1. sudo nano /etc/systemd/system/eink.service
2. Paste the contents of eink.service (included in repo) in to nano.
3. sudo systemctl daemon-reload
4. sudo systemctl start eink.service
5. sudo systemctl enable eink.service

### Configuration
**Open _bus_countdown.py_ in a text editor:**
1. Change the fields in the dictionary. The first can be found on the [Tfl travel information site](https://tfl.gov.uk/travel-information/stations-stops-and-piers/). You can extract the code from the URL there. The second field is an alias for you to assign (it can be anything)  '495012362W': 'Highstreet stop'.
2. Adjust vertical_spacing, titlesize and fontsize so that the bus information fits on the page.

**Calendar config:**

You can change advanced configuration in _calendar/js/custom_display_day.js_. To change the ICS URL for the calendar download open _launcher.py_ in a text editor and paste your ICR URL in to the calendar_url variable. 
