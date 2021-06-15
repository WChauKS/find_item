# find_item

## Introduction
This is a web scraping project. I created it because I bought an item about three years ago which was recently discontinued and the attachments for it were no longer being made. Occasionally, the website would post a refurbished item to their refurbished section. I have been manually checking this section frequently in the past few months. Instead of manually going to the website, I have set up a Raspberry Pi Zero W to run this script every hour.\
I needed a way for it to alert me when a new item was posted, so I incorporated tweepy to send me a direct message on Twitter. I originally planned on using Twilio to text me, but I did not want to purchase a phone number just for this project. \

## Usage
**Key Dependencies**\
[requests](https://docs.python-requests.org/en/master/): makes an HTTP request to the website \
[beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/): scrapes the website and uses Python's built-in 'html.parser' to parse the elements of the website \
[tweepy](https://docs.tweepy.org/en/stable/): tweets user as a way of notification \\

**Optional**\
[PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation): for accessing __config.yaml__ where the user can make modifications to their own search parameters and Twitter account/auth. This is marked optional because it could be changed to *config.py* \
```
site: ''
url: ''

# key word to search for
item_of_interest: ''

# strings to remove for cleaning up dict key
rm_strings: []

# name of text file for comparing to see if new items were posted
filename: 'prev.txt'

# twitter user id
user_id: ''

# twitter auth
twitter:
  consumer_key: ''
  consumer_secret: ''
  access_token: ''
  access_token_secret: ''
```
Copy the above block of code and paste it into a file named __config.yaml__ and insert the appropriate data inside of the ''. If you decide to use __config.py__, simply assign all the strings as variables (ex. site = 'www.google.com') and update __main.py__ by removing lines 7-8, and replacing all data[] and data[][] with the appropriate variable name. \

In order to run the script successfully, you may need to edit `scrape` and `get_relevent_items` functions __main.py__ to match with the formatting of the website you are scraping.

## Running Cron Job ##
I am using [crontab](https://man7.org/linux/man-pages/man5/crontab.5.html) which is built into Rasbian OS. I entered `crontab -e` then I appended `0 * * * * python3 /home/pi/find_next/main.py` to the file. This indicates that the script will run at every minute 0 (when the clock changes from 59 minutes to 00 minutes). You can test other schedule expressions at https://crontab.guru/.

## ToS ##
__Check with the website's robots.txt and ToS before running.__ \
In my case, the website I am scraping does not disallow scraping its product pages nor the refurbished page.
