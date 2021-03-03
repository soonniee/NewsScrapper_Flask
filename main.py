import requests
from flask import Flask, render_template, request, redirect
from scrapper import news_scrapper,comments_scrapper
base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new_url = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular_url = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

db_news = {}
app = Flask("__name__")
@app.route("/")
def index():
    order_by = request.args.get('order_by')
    if not order_by:
        news_popular = db_news.get('popular')
        if not news_popular:
            news_popular = news_scrapper(popular_url)
            db_news['popular'] = news_popular
            
            return render_template('index.html', news_popular = news_popular, news_new = [])
        else:
            return render_template('index.html', news_popular = news_popular, news_new = [])
    else:
        if order_by == 'popular':
            news_popular = db_news.get('popular')
            if not news_popular:
                news_popular = news_scrapper(popular_url)
                db_news['popular'] = news_popular
                return render_template('index.html', news_popular = news_popular, news_new = [])
            else:
                return render_template('index.html', news_popular = news_popular, news_new = [])
        if order_by == 'new':
            news_new = db_news.get('new')
            if not news_new:
                news_new = news_scrapper(new_url)
                db_news['new'] = news_new
                return render_template('index.html', news_new = news_new, news_popular = [])
            else:
                return render_template('index.html', news_new = news_new, news_popular = [])
db_comments={}
@app.route("/comments/<story_id>")
def comments(story_id):
    
    if not story_id:
        redirect("/")
    else:
        url = make_detail_url(story_id)
        print(url)
        comments_id = db_comments.get(story_id)
        if not comments_id:
            comments, news_info = comments_scrapper(url)
            
            db_comments[story_id] = {
                'news_info' : news_info,
                'comments' : comments
            }
            return render_template('detail.html', comments = comments, news_info = news_info)
        else:
            print(db_comments[story_id]['news_info'])
            return render_template('detail.html', comments = db_comments[story_id]['comments'], news_info = db_comments[story_id]['news_info'])
if(__name__=="__main__"):
    app.run(host="127.0.0.1",debug=True)

