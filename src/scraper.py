import requests
import bs4 as BeautifulSoup
import json
import re
import os

def search():
    subname_code = {} 
    igcse_url = r"https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-upper-secondary/cambridge-igcse/subjects/"
    o_level_url = r"https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-upper-secondary/cambridge-o-level/subjects/"
    as_alevel_url = r"https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-advanced/cambridge-international-as-and-a-levels/subjects/"

    o_level_website = requests.get(o_level_url)
    o_level_text = BeautifulSoup.BeautifulSoup(o_level_website.text,"html.parser")
    extracted_o_level_text = o_level_text.find_all("a")

    a_level_website = requests.get(as_alevel_url)
    a_level_text = BeautifulSoup.BeautifulSoup(a_level_website.text,"html.parser")
    extracted_a_level_text = a_level_text.find_all("a")

    igcse_website = requests.get(igcse_url)
    igcse_text = BeautifulSoup.BeautifulSoup(igcse_website.text,"html.parser")
    extracted_igcse_text = igcse_text.find_all("a")
    code_pattern = r"\d{4}"

    a_level_dict = {}
    o_level_dict = {}
    igcse_dict = {}
    as_dict = {}

    for a in extracted_igcse_text:
        href = a.get("href","")
        if href.startswith("/programmes-and-qualifications/cambridge-igcse-"):
            code_match = re.search(code_pattern,a.get_text(strip=True))
            if code_match:
                code = code_match.group()
                text = a.get_text(strip=True)
                text = text[:code_match.start()]
                text = re.sub(r"[^A-Za-z)]+$","",text)
                igcse_dict[code] = text

    for a in extracted_o_level_text:
        href = a.get("href","")
        if href.startswith("/programmes-and-qualifications/cambridge-o-level-"):
            code_match = re.search(code_pattern,a.get_text(strip=True))
            if code_match:
                code = code_match.group()
                text = a.get_text(strip=True)
                text = text[:code_match.start()]
                text = re.sub(r"[^A-Za-z)]+$","",text)
                o_level_dict[code] = text

    for a in extracted_a_level_text:
        href = a.get("href","")
        if href.startswith("/programmes-and-qualifications/cambridge-international-as-and-a-level-"):
            code_match = re.search(code_pattern,a.get_text(strip=True))
            if code_match:
                code = code_match.group()
                text = a.get_text(strip=True)
                text = text[:code_match.start()]
                if code.startswith("8"):
                    text = re.sub(r"[^A-Za-z)]+$","",text)
                    as_dict[code] = text
                
                else:
                    text = re.sub(r"[^A-Za-z)]+$","",text)
                    a_level_dict[code] = text
        
    subname_code = {
        "IGCSE":igcse_dict,
        "O Level":o_level_dict,
        "AS & A Level":a_level_dict
    }

    return subname_code
    
    


def generate_file(subjects):
    os.makedirs("data",exist_ok=True)
    with open("data/subjects.json","w",encoding="utf-8") as file:
        json.dump(subjects,file,indent=4,ensure_ascii=False)



if __name__ == "__main__":
    print("This is a test\n")
    dictionary = search()
    generate_file(dictionary)
    