
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from Transcripts import TranscriptLink, TranscriptText
from argparse import ArgumentParser
from random import randrange
from time import sleep
from pathlib import Path
import yaml

# accept arguments for scraping
argument_parser = ArgumentParser()
argument_parser.add_argument('-t', '--ticker',
                             help='Ticker of the desired company',
                             default=None)
argument_parser.parse_args()


# load your environment variables from the secret.yaml file
my_setup = yaml.safe_load(open('secret.yaml'))
Path("Outputs/Transcripts").mkdir(parents=True, exist_ok=True)


# a new selenium browser
def open_browser() -> webdriver:
    my_options = webdriver.ChromeOptions()
    my_options.add_argument(f'user-data-dir=Scraper')
    my_options.add_argument('--enable-javascript')
    my_options.add_argument('--disable-blink-features=AutomationControlled')
    my_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    my_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=my_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")
    return driver


# login to Seeking Alpha for premium only content
def sign_in(driver: webdriver) -> None:
    driver.find_element(By.XPATH, value='//span[text()="Sign In"]').click()
    driver.find_element(By.NAME, value='email').send_keys(my_setup['username'])
    driver.find_element(By.NAME, value='password').send_keys(my_setup['password'])
    sleep(3)
    driver.find_element(By.XPATH, value='//button[@type="submit"]').click()


# get all the transcripts from webpage
def get_transcripts(driver: webdriver) -> list[WebElement]:

    articles_before_scroll: list = driver.find_elements(By.TAG_NAME, value='article')
    articles_after_scroll: list = []

    while len(articles_after_scroll) != len(articles_before_scroll):
        articles_before_scroll: list = driver.find_elements(By.TAG_NAME, value='article')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)
        articles_after_scroll: list = driver.find_elements(By.TAG_NAME, value='article')

    return articles_after_scroll


# TODO: modify the Press and hold function to assist the user
# based on animation duration in the CSS stylesheet
def press_and_hold(driver):
    captcha_element = driver.find_element(
        By.ID, value='px-captcha-wrapper').find_element(
        By.XPATH, value='//div[@aria-label="Press & Hold"]'
    )

    ActionChains(driver).click_and_hold(on_element=captcha_element).perform()


if __name__ == '__main__':

    ticker = 'FIVE'
    link = f'https://seekingalpha.com/symbol/{ticker}/earnings/transcripts'

    browser = open_browser()
    sleep(3)
    browser.get(link)
    sleep(3)
    sign_in(browser)

    # get the transcript links
    transcript_links = get_transcripts(browser)

    # get article information
    transcript_articles = []
    for article in transcript_links:
        this_article = TranscriptLink(article, symbol=ticker)
        article_info: dict = this_article.get_article_information()
        transcript_articles.append(article_info)

    for article in transcript_articles:
        if article['document_type'] == 'transcripts':
            browser.get(article['url'])
            transcript_text = TranscriptText(browser)
            with open(
                    f'Outputs/Transcripts/{ticker}_{article["document_type"]}_{article["article_title"]}.txt', 'w') as \
                    transcript_file:
                transcript_file.write(transcript_text.html_content)
            sleep(randrange(3, 6))

    browser.close()
