from bs4 import BeautifulSoup
import re

class HTMLExtractor:
    """ Structure that deals with processing 
    and extraction of useful info """

    def __init__(self, source):
        self.soupPage = BeautifulSoup(source, 'lxml')

    def extract(self):
        extraction_area = self.soupPage.find(id="HeroHeaderModule")
        summary_area = extraction_area.find_all('div')[2].div
        job_company = self._remove_digits(summary_area.contents[0])
        job_title = summary_area.contents[1].string
        job_location = summary_area.contents[2].get_text()

        job_main = self.soupPage.find(id="Details")
        for line_break in job_main.find_all('br', 'b'):
            line_break.decompose()

        print(job_main.prettify())
        
        # print(job_company, job_title, job_location)
                
    def _remove_digits(self, element):
        text = element.get_text()
        match = re.search('[0-9]+', text)
        if match:
            cleaned_text = text[0: match.start()]     
            return cleaned_text
        return text
        
      
