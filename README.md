# SeekingAlpha-Scraper
A bot for collecting Earnings Announcement Transcripts from SeekingAlpha.com

# Disclaimer
**_DO NOT ABUSE THIS SCRAPER._**

This scraper was developed for educational purposes only and has limited applications.
SeekingAlpha TOS prohibit scraping and I make no representation that your account won't be banned if you use this program. 
Furthermore, should I be contacted by SeekingAlpha with a request to remove this repo, I will do so immediately.

# About
This scraper collects the earnings announcements of a specific company (identified with `ticker` or `t`).


# Installation
First, make sure that you're using Python 3.7+.

1. Clone or download this repository.
2. Run `pip install -r requirements.txt` inside this repo. Consider doing this inside of a Python virtual environment.
3. You need the [Chromedriver](http://chromedriver.chromium.org/) in the working directory.
4. Create a `secret.yaml` file containing the keys `username` and `password` with your SeekingAlpha login information. You should consider creating a dummy SeekingAlpha account.

# Usage
```
usage: Scraper.py [-h] [-t ticker]

optional arguments:
  -h, --help                                  show this help message and exit
  -t SYMBOL, --ticker SYMBOL                  Ticker Symbol of the desired company.
```

Run the script as follows, taking **Costco (Ticker Symbol: COST)** as an example.

### Example 1

`python Scraper.py -t COST`

The outputs will be saved in `Outputs/Transcripts` as HTML files.

### Note
This scraper does not pass any CAPTCH tests.

