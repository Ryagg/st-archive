# obtain the html source
#content = requests.get(link_discovery)

# create BeautifulSoup object and extract content
#soup = BeautifulSoup(content.content, "html.parser")

#beta:element: <a href="/wiki/Desperate_Hours" class="category-page__member-link" title="Desperate Hours">Desperate Hours</a>

#<a href="/wiki/Desperate_Hours" title="Desperate Hours">Desperate Hours</a>
# Desperate Hours

#xpath: //*[@id="mw-content-text"]/div/ul[1]/li[1]/i/a
#fullxpath: /html/body/div[4]/div[3]/div[5]/main/div[4]/div[2]/div/ul[1]/li[1]/i/a

# #mw-content-text > div > ul:nth-child(12) > li:nth-child(2) > i > a
# <a href="/wiki/Drastic_Measures" title="Drastic Measures">Drastic Measures</a>

#titles = soup.select("ul li i a")

#print(titles)
# print(type(titles))

#links = []

#for link in titles.findAll("a"):
    #url=link.find("href").text

    #links.append(url)

#print(links)
