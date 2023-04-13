import os
import requests
from bs4 import BeautifulSoup
from crawler import HEADERS
import re
import json

# ----------------------- Helper Functions -----------------------
def get_html(URL):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
                             ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
        r = requests.get(url = URL, headers = headers,timeout=1)
        if r.status_code != requests.codes.ok:
            
            text = None
        else:                    
            text = r.text
        return text
    except requests.exceptions.RequestException as e:
        print("exception with url: " + URL)
        return


def removeSGML(targetStr):
    # these tags are within <...>
    rmTarget = re.compile(r'<[^>]+>')
    return rmTarget.sub('', targetStr)



def get_stamps_text(text, link, counter):
    with open('crawled_pages/stamps' + str(counter) +'.txt', 'w') as file:
      soup = BeautifulSoup(text, 'html.parser')
      js = soup.find("script", {"type": "application/ld+json"}).string.strip()
      json_obj = json.loads(js)['@graph'][0]
      
      file.write(link)
      file.write(soup.find('title').string.strip() + '\n')
      body_text = ' '.join([str(tag) for tag in soup.find_all('p')])
      body_text = removeSGML(body_text)
      

      try:
        file.write(json_obj["location"]["address"].replace('\n', ' ') + '\n')
        file.write(json_obj["startDate"].replace('\n', ' ')+'\n')
        file.write(json_obj["description"].replace('\n', ' ') + '\n')
        body_text += ' ' + soup.find('title').string.strip() + ' ' + \
            json_obj["description"]
        body_text = body_text.replace('\n', ' ').replace(
            '\r', ' ').replace('\t', ' ')
        file.write(body_text)
      except:
        os.remove('crawled_pages/stamps' + str(counter) + '.txt')
        counter -= 1
        # print("ERROR", "No info found for ", link)
      return counter



# ----------------------- Functions -----------------------

def download_aa():
    """by Oliver"""

    # read aa links
    with open("crawled_links.txt", "r", encoding = "ISO-8859-1") as f:
        links = f.readlines()
        aa_links = [link for link in links if "annarbor.org" in link]

        count = 1
        for link in aa_links:
            link = link.strip()
            # if 'annarbor.org' in link:
            r = requests.get(link, headers = HEADERS, timeout = 2)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # title
            title = soup.find('title').text
            # location
            location_li = soup.find('ul', {'class': 'info'}).find('li')
            location_icon = location_li.find('i', {'class': 'fas fa-map-marker-alt'})
            location = location_li.text.replace(location_icon.text, '').strip()
            # date
            dates_li = soup.find('li', {'data-name': 'dates'})
            if dates_li is None:
                dates = ''
            else:
                dates = dates_li.find('span', {'class': 'info-list-value'}).text.strip()
            # time
            time_li = soup.find('li', {'data-name': 'time'})
            if time_li is None:
                time = ''
            else:
                time = time_li.find('span', {'class': 'info-list-value'}).text.strip()
            # overview
            tab_content = soup.find('div', {'class': 'detail-tab active'}).find('div', {'class': 'tab-content'})
            overview = tab_content.text.strip()
            overview = overview.replace('\n', ' ')

            # write to file
            ff = open(os.path.join("crawled_pages", "aa_" + str(count) + ".txt"), "w", encoding = "utf-8")
            ff.write(link + '\n')
            ff.write(title + '\n')
            ff.write(location + '\n')
            ff.write(time + ' ' + dates + '\n')
            ff.write(overview + '\n')
            ff.write(title + ' ' + overview)
            ff.close()
            count += 1
            


def download_yp():
    """by Oliver"""

    # read yp links
    with open("crawled_links.txt", "r", encoding = "ISO-8859-1") as f:
        links = f.readlines()
        yp_links = [link for link in links if "ypsireal.com" in link]

        count = 1
        for link in yp_links:
            link = link.strip()
            r = requests.get(link, headers = HEADERS, timeout = 2)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # title
            title = soup.find('title').text
            # location
            location_li = soup.find('ul', {'class': 'info'}).find('li')
            location_icon = location_li.find('i', {'class': 'fas fa-map-marker-alt'})
            location = location_li.text.replace(location_icon.text, '').strip()
            # date
            dates_li = soup.find('li', {'data-name': 'dates'})
            if dates_li is None:
                dates = ''
            else:
                dates = dates_li.find('span', {'class': 'info-list-value'}).text.strip()
            # time
            time_li = soup.find('li', {'data-name': 'time'})
            if time_li is None:
                time = ''
            else:
                time = time_li.find('span', {'class': 'info-list-value'}).text.strip()
            # overview
            tab_content = soup.find('div', {'class': 'detail-tab active'}).find('div', {'class': 'tab-content'})
            overview = tab_content.text.strip()
            overview = overview.replace('\n', ' ')

            # write to file
            ff = open(os.path.join("crawled_pages", "yp_" + str(count) + ".txt"), "w", encoding = "utf-8")
            ff.write(link + '\n')
            ff.write(title + '\n')
            ff.write(location + '\n')
            ff.write(time + ' ' + dates + '\n')
            ff.write(overview + '\n')
            ff.write(title + ' ' + overview)
            ff.close()
            count += 1



def download_stamps():
    """by Freddie"""
    counter = 0
    with open('crawled_links.txt', 'r') as f:
      links = f.readlines()
      for link in links:
        if 'https://stamps.umich.edu/events/' in link:
          r = requests.get(link.rstrip(), headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
              AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
          
          counter = get_stamps_text(r.text, link, counter)
          counter += 1



def dowload_ums():
    '''by Yuhui'''
    with open("crawled_links.txt", "r", encoding = "ISO-8859-1") as f:
        f = f.readlines()
        idx = 0
        for url in f:
            if "ums.org/performance/" in url:
                url = url.strip()
                text = get_html(url)
                if text == None:
                    continue
                else:
                    soup = BeautifulSoup(text, "html.parser")
                    output = soup.find("script", {"type": "application/ld+json"}).string.strip()
                    with open(os.path.join('crawled_pages/','ums_' + str(idx) + '.txt'), 'w')as file:
                        if output != None:
                            output = output.replace('\n', '').replace('\r', '').replace('\t', '')
                            output = ''.join(filter(lambda x: x.isprintable(), output))
                            # Parse the JSON string
                            my_json_object = json.loads(output)

                            file.write(url + '\n')
                            file.write(my_json_object["name"] + '\n')
                            file.write(my_json_object["location"]["address"]["name"] + '\n')
                            file.write(my_json_object["startDate"]+'\n')
                            file.write(my_json_object["description"] + '\n') 
                            file.write(my_json_object["name"] + my_json_object["description"] + '\n')     
                        if output == None:
                            file.write(url + '\n')
                    idx += 1
    return



def download_smtd():
    # Rosen
    with open('crawled_links.txt', 'r') as f:
        links = f.readlines()
        counter = 0
        for link in links:
            if 'smtd' in link:
                r = requests.get(link.rstrip(), headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
                soup = BeautifulSoup(r.text, 'html.parser')
    
                output = soup.find("script", {"type": "application/ld+json"}).string.strip()
                output = output.replace('\n', '').replace('\r', '').replace('\t', '')
                output = ''.join(filter(lambda x: x.isprintable(), output))
                # Parse the JSON string
                my_json_object = json.loads(output)

                location_tag = soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['et_pb_text_inner'] and tag.find('strong'))
                if location_tag and location_tag.strong:
                    location = location_tag.strong.get_text(strip=True) 
                else:
                    location = "Location not found"

                # Find the "Event" object
                event_object0 = None
                event_object4 = None
                for obj in my_json_object["@graph"]:
                    if obj["@type"] == "WebPage":
                        event_object0 = obj
                    if obj["@type"] == "Event":
                        event_object4 = obj

                with open('crawled_pages/smtd' + str(counter) + '.txt', 'w') as f:
                    f.write(link)
                    if event_object0:
                        f.write(event_object0["name"] + '\n')
                    else:
                        f.write("Name not found\n")
                    if location == "":
                        f.write("Location not found\n")
                    else:
                        f.write(location + '\n')
                    if event_object4:
                        f.write(event_object4["startDate"] + '\n')
                        f.write(event_object4["description"] + '\n')
                    else:
                        f.write("Start date not found\n")
                        f.write("Description not found\n")
                    if event_object0:
                        f.write(event_object0["name"])
                    if event_object4: 
                        f.write (' ' + event_object4["description"] + '\n')    
                counter += 1



# ----------------------- Main -----------------------
if __name__ == "__main__":
    download_aa()
    download_yp()
    download_stamps()
    dowload_ums()
    download_smtd()
