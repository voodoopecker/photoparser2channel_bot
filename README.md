Telegram bot. Scraping pictures, filtering duplicates and posting them using a scheduler to your Telegram channel.

![](start.jpg)

---
# Installation
* Download the project

````
git clone https://github.com/voodoopecker/photoparser2channel_bot.git
````
* Upload bot's files to your server
* Install dependencies
````
pip install -r requirements.txt
````
---
# Usage

* Set bot settings in bottoken.py:
  * ```TOKEN``` - your bot token
  * ```admin_ID``` - bot admin ID
  * ```channel_ID``` - channel ID for posting.
  * ```post_interval``` - posting time interval (seconds)
  * ```post_disp``` - additional random value for the posting interval (seconds)
* Add a list of URLs to be scraped to the urls.txt file. Each URL should be on a new line.
* Run bot:
  * If you use a virtual environment, you need to activate it.
  * Run ```python3 main_bot.py```