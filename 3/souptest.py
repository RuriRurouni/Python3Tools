from bs4 import BeautifulSoup as soupy
import urllib.request
import re

html = urllib.request.urlopen('https://twitter.com/RuriRurouni').read()
soup = soupy(html, features = "html.parser")

x = soup.find("meta", {"name":"description"})
print(x)

x = soup.find("meta", {"name":"description"})['content']
print(x)

filter = re.findall(r'"(.*?)"',x)
data = filter[0]
print(data)
