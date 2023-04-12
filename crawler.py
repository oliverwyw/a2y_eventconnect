from bs4 import BeautifulSoup
import os
import re

# ----------------------- Constant -----------------------

HEADERS = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
               AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
ALLOWED_DOMAINS = ["maizepages.umich.edu/event", "ums.org/performance", \
    "stamps.umich.edu/events", "smtd.umich.edu/events", "mutotix.umich.edu/", \
        "annarbor.org/event", "ypsireal.com/event"]

ROOT = {'aa': 'https://annarbor.org',
        'yp': 'https://ypsireal.com', 
        'maizepage': 'https://maizepages.umich.edu',
        'ums': 'https://ums.org',
        'smtd': 'https://smtd.umich.edu',}


# ----------------------- Functions -----------------------
def normalizeURL(url, root):
  # ends with /
  if url[-1] == "/":
      url = url[:-1]
  # http to https
  if url.startswith('http://'):
      return 'https'+url[4:]
  # no specified protocol
  elif url.startswith('//'):
      return 'https:'+url
  # relative address
  elif url.startswith('.'):
      return root+url[1:]
  elif url.startswith('..'):
      return root+url[2:]
  else:
      return url



def is_valid_url(url):
  """
  Check if url is valid
  params: url - url to check
  return: True if url is valid, False otherwise
  """
  if url[-4:] == ".pdf":
      return False
  
  if "mailto:" in url:
      return False

  for domain in ALLOWED_DOMAINS:
      if domain in url[:35]:
          return True
  
  return False


# ----------------------- Main -----------------------
if __name__ == "__main__":

  clean_url = []

  for file_name in os.listdir("roots"):
    with open("roots/" + file_name, 'r', encoding="ISO-8859-1") as f:
      html_text = f.read()
      soup = BeautifulSoup(html_text, 'html.parser')
      links = soup.find_all('a')
      for link in links:
              
        # "annarbor.org/event", "ypsireal.com/event"
        # oliver
        if 'aa' in file_name or 'yp' in file_name:
          url = link.get('href')
          if url is not None and len(url) != 0 and is_valid_url(url):
            if 'aa' in file_name:
              url = normalizeURL(url, ROOT['aa'])
            elif 'yp' in file_name:
              url = normalizeURL(url, ROOT['yp'])
            # append to clean_url
            if '/event/' in url \
              and '/rss' not in url\
              and url not in clean_url:
              clean_url.append(url)

              
        # "maizepages.umich.edu/event"
        # yuxin
        # elif 'maizepage' in file_name:
        #   url = link.get('href')
        #   if url and "/event/" in url and url not in clean_url:
        #     # clean_url.append("https://maizepages.umich.edu" + link.get('href'))
        #     clean_url.append(url)
        # "stamps.umich.edu/events"
        # freddiew
        elif 'stamp' in file_name:
          if link.get('href') and "/events/" in link.get("href"):
            href = link.get('href')
            href.rstrip('/')
            if "/events/" in href and '/event/' not in href:
              href += "/"
              clean_url.append(href)
        
        
        # "smtd.umich.edu/events" : https://smtd.umich.edu/event/hobsons-choice-chamber-opera/
        # rosen
        elif 'smtd' in file_name:
          if link.get('href') and "/event/" in link.get("href"):
            clean_url.append(normalizeURL(link.get('href'), ROOT['smtd']))
        
        # "ums.org/performance"
        # yuhui
        elif 'ums' in file_name:
          url = link.get('href')
          if url is not None and len(url) != 0 and is_valid_url(url):
            url = normalizeURL(url, ROOT['ums'])
            if "/performance/" in url and url not in clean_url:
              clean_url.append(url)
            
        elif 'maize' not in file_name:
          print('ERROR: unidentified file name:', file_name)
          
  with open("crawled_links.txt", "w") as f:
    for url in set(clean_url):
      f.write(url + "\n")
