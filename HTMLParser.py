from bs4 import BeautifulSoup


class HTMLParser:
    """ Structure that deals with processing 
    and extraction of useful info """

    def __init__(self, soupTag):
        self.soupTag = soupTag

    def extract(self):
        relevant_element = self.soupTag.div.next_sibling
        company_name = relevant_element.contents[0]
        job_title = relevant_element.contents[1]
        job_location = relevant_element.contents[2]

        print('==============================')
