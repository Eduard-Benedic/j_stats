from bs4 import BeautifulSoup
import re

class HTMLExtractor:
    """ Structure that deals with processing 
    and extraction of useful info """

    def __init__(self, source):
        self.soupPage = BeautifulSoup(source, 'lxml')

    def extract(self):
        extraction_area = self.soupPage.find(id="HeroHeaderModule")
        summary_area = extraction_area.contents[2].div
        job_company = self._remove_digits(summary_area.contents[0])
        job_title = summary_area.contents[1].get_text()
        job_location = summary_area.contents[2].get_text()
        job_main_tag = self.soupPage.find(class_="jobDescriptionContent")
        self._clean_tag(job_main_tag)
        
        requirements = self._get_requirements(job_main_tag)

        return {
            'job_company': job_company,
            'job_title': job_title,
            'job_location': job_location,
            'requirements': requirements
        }

                
    def _remove_digits(self, element):
        text = element.get_text()
        match = re.search('[0-9]+', text)
        if match:
            cleaned_text = text[0: match.start()]     
            return cleaned_text
        return text

    def _clean_tag(self, element):
        try:
            for line_break in element.find_all('br', 'b'):
                if line_break:
                        line_break.decompose()
                else:
                    continue
        except:
            print('No br element')
             
    def _get_requirements(self, element):
        artificial_block = []
        is_passed_first_tag = True
        for list_tag in element.find_all('ul'):
            try:
                if self._has_prev_sibling(list_tag, 'ul') and self._has_next_sibling(list_tag, 'ul'):
                    if is_passed_first_tag:
                        artificial_block.append(list_tag.previous_sibling.get_text())
                        is_passed_first_tag = False

                    artificial_block.append(list_tag.get_text())
                elif self._has_prev_sibling(list_tag, 'ul') and not self._has_next_sibling(list_tag, 'ul'):
                    artificial_block.append('--end-block--')
                    is_passed_first_tag = True
                else:
                    for list_item in list_tag:
                        artificial_block.append(list_item.get_text())
            except Exception:
                print('Cannot find element name')
        return artificial_block

    def _has_next_sibling(self, element, el_type):
        return True if element.next_sibling.name == el_type else False
      
    def _has_prev_sibling(self, element, el_type):
        return True if element.previous_sibling.name == el_type else False
