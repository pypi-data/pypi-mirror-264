from bs4 import BeautifulSoup
import pandas as pd
import warnings


def parse_cakeresume_joblist(soup: BeautifulSoup) -> pd.DataFrame:
    """
        URL = "https://www.cakeresume.com/jobs?location_list%5B0%5D=Taiwan&location_list%5B1%5D=Taipei%20City%2C%20Taiwan&location_list%5B2%5D=%E5%8F%B0%E5%8C%97%E5%B8%82%2C%20%E5%8F%B0%E7%81%A3&location_list%5B3%5D=%E5%8F%B0%E7%81%A3%E5%8F%B0%E5%8C%97%E5%B8%82&location_list%5B4%5D=%E6%96%B0%E5%8C%97%E5%B8%82%2C%20%E5%8F%B0%E7%81%A3&profession%5B0%5D=it_data-scientist&profession%5B1%5D=it_data-engineer&profession%5B2%5D=it_machine-learning-engineer&profession%5B3%5D=it_python-developer&profession%5B4%5D=it_big-data-engineer&order=latest&page=1"
    """
    # Extracting information about each job posting

    # 取出所有職缺的區塊，以此取出每個職缺的資訊
    job_region = soup.find("div", class_="JobSearchPage_searchResults__03mlk")
    job_list = job_region.find_all("div", class_="JobSearchItem_wrapper__bb_vR")

    job_dict_list = []

    for job_item in job_list:
        
        try:
            job_image = job_item.find("img")["src"]
        except Exception as e:
            warnings.warn(f"Image not found. Error: {e}")
            job_image = ""

        try:
            job_title = job_item.find("a", class_="JobSearchItem_jobTitle__bu6yO").text
            job_link = job_item.find("a", class_="JobSearchItem_jobTitle__bu6yO")["href"]
        except Exception as e:
            warnings.warn(f"Job title or link not found. Error: {e}")
            job_title = ""
            job_link = ""
            
        try:
            job_company = job_item.find("a", class_="JobSearchItem_companyName__bY7JI").text
        except Exception as e:
            warnings.warn(f"Company name not found. Error: {e}")
            job_company = ""
            
        try:
            job_description = job_item.find("div", class_="JobSearchItem_description__si5zg").text
        except Exception as e:
            warnings.warn(f"Job description not found. Error: {e}")
            job_description = ""
            
        try:
            job_tags = job_item.find_all("div", class_="Tags_item__B6Bjo Tags_itemClickable__ebGba")
            job_tags = [tag.text for tag in job_tags]
        except Exception as e:
            warnings.warn(f"Tags not found. Error: {e}")
            job_tags = []
        
        try:
            job_feature_div = job_item.find("div", class_="JobSearchItem_features__hR3pk")
        except Exception as e:
            warnings.warn(f"Feature div not found. Error: {e}")
            
        if job_feature_div:
            try: 
                job_features = job_feature_div.find_all("div", class_="InlineMessage_inlineMessage____Ulc InlineMessage_inlineMessageLarge__uaRgi InlineMessage_inlineMessageDark__JjyEO")

                job_number, job_type, job_level = job_features[0].text.split("・")
                job_location = job_features[1].text
                jon_payment = job_features[2].text
                job_experience = job_features[3].text
                job_managers = job_features[4].text
                
            except Exception as e:
                warnings.warn(f"Features not found. Error: {e}")
                job_number, job_type, job_level, job_location, jon_payment, job_experience, job_managers = "", "", "", "", "", "", ""
                
                
        job_dict = {
            "image": job_image,
            "title": job_title,
            "link": job_link,
            "company": job_company,
            "description": job_description,
            "tags": job_tags,
            "number": job_number,
            "type": job_type,
            "level": job_level,
            "location": job_location,
            "payment": jon_payment,
            "experience": job_experience,
            "managers": job_managers
        }
        
        job_dict_list.append(job_dict)
        
    df = pd.DataFrame(job_dict_list)
    
    return df