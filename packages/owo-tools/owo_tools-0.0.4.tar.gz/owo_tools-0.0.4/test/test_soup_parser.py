import pandas as pd
import requests
from bs4 import BeautifulSoup
from owo_tools.soup_parser import parse_cakeresume_joblist


def test_parse_cakeresume_joblist_not_empty():
    URL = "https://www.cakeresume.com/jobs?location_list%5B0%5D=Taiwan&location_list%5B1%5D=Taipei%20City%2C%20Taiwan&location_list%5B2%5D=%E5%8F%B0%E5%8C%97%E5%B8%82%2C%20%E5%8F%B0%E7%81%A3&location_list%5B3%5D=%E5%8F%B0%E7%81%A3%E5%8F%B0%E5%8C%97%E5%B8%82&location_list%5B4%5D=%E6%96%B0%E5%8C%97%E5%B8%82%2C%20%E5%8F%B0%E7%81%A3&profession%5B0%5D=it_data-scientist&profession%5B1%5D=it_data-engineer&profession%5B2%5D=it_machine-learning-engineer&profession%5B3%5D=it_python-developer&profession%5B4%5D=it_big-data-engineer&order=latest&page=1"
    
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extracting information about each job posting
    df = parse_cakeresume_joblist(soup)
    
    assert not df.empty
    

    