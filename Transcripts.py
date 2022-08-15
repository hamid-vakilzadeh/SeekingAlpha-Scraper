from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchAttributeException


class TranscriptLink:
    def __init__(self, element, symbol: str = None):
        self._symbol: str = symbol
        self._source = element
        self.url: str = self._get_url_link()
        self.author: str = self._get_author_info()
        self.article_title: str = self._get_article_title()
        self.document_type: str = self._get_document_type()
        self.publication_date: str = self._get_publish_date()
        self.ticker: str = self._get_ticker_info()

    # return article information in a dictionary
    def get_article_information(self):
        return dict(url=self.url,
                    author=self.author,
                    article_title=self.article_title,
                    document_type=self.document_type,
                    publication_date=self.publication_date,
                    ticker=self.ticker)

    # open the transcript page to collect the text
    def open_article(self) -> None:
        try:
            self._source.find_element(
                By.TAG_NAME, value='h3').find_element(
                By.TAG_NAME, value='a').click()

        except Exception:
            raise Exception

    # get the title of the article
    def _get_article_title(self) -> str or None:
        try:
            return self._source.find_element(
                By.TAG_NAME, value='h3').find_element(
                By.TAG_NAME, value='a').text

        except (NoSuchElementException, NoSuchAttributeException):
            return None

    # get the url to the transcript text
    def _get_url_link(self) -> str or None:
        try:
            return self._source.find_element(
                By.TAG_NAME, value='h3').find_element(
                By.TAG_NAME, value='a').get_attribute('href')

        except (NoSuchElementException, NoSuchAttributeException):
            return None

    # get the author information (Usually it is only the SA Transcripts)
    def _get_author_info(self) -> str or None:
        try:
            return self._source.find_element(
                By.TAG_NAME, value='footer').find_element(
                By.XPATH, value='//*[@data-test-id="post-list-author"]').text

        except (NoSuchElementException, NoSuchAttributeException):
            return None

    # get the publication date
    # TODO: date could return 'Today' and 'Yesterday'. fix that.
    def _get_publish_date(self) -> str or None:
        try:
            return self._source.find_element(
                By.TAG_NAME, value='footer').find_element(
                By.XPATH, value='//*[@data-test-id="post-list-date"]').text

        except (NoSuchElementException, NoSuchAttributeException):
            return None

    # get tje ticker of the company
    # TODO: fix the list output
    def _get_ticker_info(self) -> str or None:
        if self._symbol is None:
            try:
                return self._source.find_element(
                    By.TAG_NAME, value='footer').find_element(
                    By.XPATH, value='//*[@data-test-id="post-list-ticker"]')

            except (NoSuchElementException, NoSuchAttributeException):
                return None
        else:
            return self._symbol

    # get document type (transcript or presentation)
    def _get_document_type(self):
        return self._source.find_element(By.TAG_NAME, value='use').get_attribute('xlink:href').replace('#', '')


class TranscriptText:
    def __init__(self, _page: webdriver):
        self._page = _page
        self.title: str = self._get_title()
        self.text: str = self._get_transcript_text()
        self.html_content: str = self._get_html_transcript()

    # get the title of the transcript
    def _get_title(self) -> str or None:
        try:
            return self._page.find_element(
                By.XPATH, value='//*[@data-test-id="post-title"]').text

        except NoSuchElementException:
            return None

    # get the text of the transcript
    def _get_transcript_text(self) -> str:
        return self._page.find_element(
            By.XPATH, value='//*[@data-test-id="article-content"]').text

    # get the HTML Text of the Transcript
    def _get_html_transcript(self) -> str:
        return self._page.find_element(
            By.XPATH, value='//*[@data-test-id="article-section"]').get_attribute('innerHTML')
