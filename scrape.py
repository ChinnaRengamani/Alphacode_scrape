import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

firefox_options = Options()
firefox_options.add_argument('-headless')

print('Building session')
driver = webdriver.Firefox(options=firefox_options)

search = input("Search images for: ").lower().split(' ')
search = '+'.join(search)
html=''
driver.get(f'https://wall.alphacoders.com/search.php?search={search}')
html+=driver.page_source
url=driver.current_url
print(url)
title= int(driver.title.split(' ')[0].split('+')[0])

value = int(int(title)/30)+1
if title>200:
    print(f'{title} is larger than 200')
    quit()
else:
    kk=input(f'Do you want to Download {title}+ Wallpapers:(Y/n)')
    if kk.lower() =='y':
        print('Downloading...')
    else:
        print('Exiting...')
        quit()
driver.close()

def sel(value):
    driver1 = webdriver.Firefox(options=firefox_options)
    driver1.get(f'{url}&page={value}')
    html=driver1.page_source
    driver1.close()
    return html

for i in range(2,value):
    html+=sel(i)

soup = BeautifulSoup(html,'html.parser')

links=[]
l=[0,1,2]
for c in soup.find_all("div",{'class':"thumb-container-big"}):
    f=str(c.meta['content'])
    l[0] = 'images'+re.findall(r"/images(\d)\b", f)[0] if re.findall(r"/images(\d)\b", f) else None
    l[1] = re.findall(r"\d+", f)[-1]
    l[2] = re.search(r"\.(\w+)$", f).group(1)
    links.append(f'https://initiate.alphacoders.com/download/{l[0]}/{l[1]}/{l[2]}')

for i in links:
    response = requests.get(i)
    if response.status_code == 200:
        i=i.split('/')
        with open(f'{search}/{i[-2]}.{i[-1]}', 'wb') as f:
            f.write(response.content)


