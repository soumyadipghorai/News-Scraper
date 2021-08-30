from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index() : 
    return render_template("index.html") 

def generateNewsdiv(pageLink, category, div, divClass, image, imageClass, header, headerClass, para, paraClass, link, linkClass, categoryType) : 
    url = pageLink + category 
    page = requests.get(url)
    htmlContent = page.content 
    soup = BeautifulSoup(htmlContent, "html.parser")

    newsDiv = soup.find_all(div, {"class" : divClass})

    mainNewsList, counter = [], 0

    for div in newsDiv : 

        if categoryType :
            if counter == 4 : 
                break 
        else :
            if counter == 1 : 
                break

        subNewsList = []

        try :
            imageDiv = div.find(image, {"class" : imageClass} )
            image = div.find("img")
            subNewsList.append(image.get('src'))
        except : 
            image = div.find("img", {"class" : imageClass})
            subNewsList.append(image.get('src'))

        try : 
            headData = div.find(header, {"class" : headerClass})
            subNewsList.append(headData.text)
        except : 
            headData = div.find(header)
            subNewsList.append(headData.text)

        paraData = div.find(para)
        subNewsList.append(paraData.text)

        linkData = div.find(link)["href"]
        subNewsList.append(url+linkData)

        mainNewsList.append(subNewsList)
        
        counter += 1 

    return mainNewsList

def categoryNews(category) : 

    linkList = ["https://www.indiatvnews.com/", "https://indianexpress.com/section/", 
                "https://www.firstpost.com/category/", "https://www.indiatoday.in/"]

    main_news = []

    for i in range(len(linkList)) :
        
        if i == 0 : 
            sub_news = generateNewsdiv(linkList[i], category,
                                        "li", "p_news", "a", "thumb",
                                        "h3", "title", "p", "dic", "a", None, False)

            main_news.append(sub_news)

        if i == 1 and (category == 'india' or category == 'sports'): 
            sub_news = generateNewsdiv(linkList[i],  category,
                                     "div", "articles", "div", "snaps",
                                      "h2", "title", "p", None, "a", None, False)

            main_news.append(sub_news)
        
        if i == 2 : 
            sub_news = generateNewsdiv(linkList[i],  category,
                                     "div", "big-thumb", "a", "thumb-img",
                                      "h3", "main-title", "p", "copy", "a", None, False)

            main_news.append(sub_news)

        if i == 3 and category != 'sports' : 
            sub_news = generateNewsdiv(linkList[i],  category,
                                     "div", "catagory-listing", "div", "pic",
                                      "h2", None, "p", None, "a", None, False)

            main_news.append(sub_news)

    return main_news


@app.route("/indiatoday")
def indiatoday() : 
    newsList = ["india", "world"]
    main_news = []

    for i in range(len(newsList)) :

        sub_news = generateNewsdiv("https://www.indiatoday.in/", newsList[i],
                                     "div", "catagory-listing", "div", "pic",
                                      "h2", None, "p", None, "a", None, True)

        main_news.append(sub_news)
    
    return render_template('indiatoday.html', News = main_news)

@app.route("/firstpost")
def firstpost() : 
    newsList = ["india", "world"]
    main_news = []

    for i in range(len(newsList)) :

        sub_news = generateNewsdiv("https://www.firstpost.com/category/", newsList[i],
                                     "div", "big-thumb", "a", "thumb-img",
                                      "h3", "main-title", "p", "copy", "a", None, True)

        main_news.append(sub_news)
    
    return render_template('firstpost.html', News = main_news)
    
@app.route("/the-indian-express")
def theIndianExpress() : 
    newsList = ["india", "cities"]
    main_news = []

    for i in range(len(newsList)) :

        sub_news = generateNewsdiv("https://indianexpress.com/section/", newsList[i],
                                     "div", "articles", "div", "snaps",
                                      "h2", "title", "p", None, "a", None, True)

        main_news.append(sub_news)
    
    return render_template('theindianexpress.html', News = main_news)

@app.route("/indiatv")
def indiatv() :
    newsList = ["india", "world"]
    main_news = []

    for i in range(len(newsList)) :

        sub_news = generateNewsdiv("https://www.indiatvnews.com/", newsList[i],
                                     "li", "p_news", "a", "thumb",
                                      "h3", "title", "p", "dic", "a", None, True)

        main_news.append(sub_news)
    
    return render_template('indiatv.html', News = main_news) 

@app.route("/india")
def india() :
    return render_template('india.html', News = categoryNews("india"))

@app.route("/world")
def world() :
    return render_template('world.html', News = categoryNews("world"))

@app.route("/Sports")
def Sports() :
    return render_template('Sports.html', News = categoryNews("sports"))


if __name__ == "__main__" : 
    app.run(debug= True)