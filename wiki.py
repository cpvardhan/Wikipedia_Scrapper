import random
import bs4 as bs
import re
import requests as rq
from mongoDBOperations import MongoDBManagement
import pandas as pd
import wikipedia
from bs4 import BeautifulSoup
from string import digits


class Wikipedia_functions:

    def get_url(keyword):
        """
        This functions converts and validates the keyword if the keyword is not present .It will take the appropiate keywork and convert into the link.
        (input): keyword name
        (output): Wikipedia URL string
        """
        try:
            keyword_list = wikipedia.search(keyword)
            keyword = str(keyword_list[0])
            url = "_".join(keyword.split())
            url_link = "https://en.wikipedia.org/wiki/" + url
            return url_link

        except Exception as e:
            raise Exception(
                f"(get_url): The entered keyword is not present in the keyword") + str(e)

    def page_request(url):
        """ 
        This function takes the url from the user and converts the url into a html code
        libraries used: requests , beautiful soup
        (input): Wikipedia URL
        (output):  Beautiful Soup output 
        """
        try:
            valid_link = rq.get(url)
            if valid_link.status_code < 199:
                return "http Error"
            elif valid_link.status_code == 200:
                soup = BeautifulSoup(valid_link.content, 'html.parser')
                return soup
            else:
                return "Something went wrong in Converting the url in content(beautiful Soup)"

        except Exception as e:
            raise Exception(
                f"(page_request): Something went wrong in Converting the url in content(beautiful)" + str(e))

    def get_title(soup):
        """ 
        This function take soup url from the user and returns the title of the given url 
        (input): Beautiful Soup
        (output): Wikipedia Title
        """
        try:
            title = soup.find(id='firstHeading')
            return title.text
        except Exception as e:
            raise Exception(
                f"(get_title): Could not get the title of the given page " + str(e))



    def get_text_from_page(soup):
        """
        This Function extracts all the data from the given soup url
        And Returns the all Links present in the given link.
        (input) : BeautifulSoup
        (output) : link 
        """
        try: 
            text = ""
            for paragraph in soup.find_all('p'):
                text = text + paragraph.text
            return text

        except Exception as e:
            raise Exception(f"(get_text_from_page): CouldNot load the page and get the text from the paragraph" + str(e))

    def remove_the_number(text): 
        """ 
        This function return the text which will clear all the numbers and unwanted characters.
        (input): text 
        (output): EDA text 
        """
        try:
            ## Removing numbers in the text
            text = re.sub(r'\[[0-9]*\]', ' ',text)
            ## Removing \n 
            text = re.sub(r'\s+', ' ',text)
            ## Converting the string into Lower Case
            text = text.lower()
            #Removing digits from the text
            text = re.sub(r'\d+' , ' ' , text)
            #Removing spaces from the text
            text = re.sub(r'\s+' , ' ' , text)
            return text 
        except Exception as e:
            raise Exception(f"(remove_the_number) Something Went Wrong)" + str(e))

    def get_reference(soup): 
        """ 
        This function returns the reference HTML for the given soup URL
        (input): BeautifulSoup Links
        (output): Reference HTML As String
        """
        try: 
            reference = soup.find_all('div' , attrs={'class': 'reflist reflist-columns references-column-width'})
            reference = str(reference) # Converts the BeautifulSoup Element in to string
            reference = reference[1:] # Removes first bracket in the reference string.
            reference = reference[:-1] # Removes last bracket in the reference string.
            return reference

        except Exception as e:
            raise Exception(f"(get_reference): Something went wrong while getting the url " + str(e))

    def get_content(soup):
        """ 
        This function extratc==cts the contents from the given soup and returns the content
        (input): Beautiful Soup
        (output): Wikipedia Contents
        """
        try:
            string = ""
            for word in soup.find_all('div' , attrs = {'class': 'toc'}): 
                string += word.text
            content = []
            for i in string.split('\n'): # Splitting the string by \n
                if type(i) == str and len(i) > 2:
                    string = i.lstrip(digits)
                    string = string.replace('.',"")
                    string = string.lstrip(digits)
                    string = string.lstrip()
                    content.append(string)
                    # appending the string into the list
                else: 
                    pass
            return content
        
        except Exception as e:
            raise Exception(f"(get_content): Could not fetch the content from the given soup url" + str(e))

    def get_all_links(soup): 
        """ This Function return all the links in the given soup
        (:param)  : BeautifulSoup
        (:output): Links of all lists"""