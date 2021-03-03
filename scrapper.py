import requests
def news_scrapper(url):
    news_new = []
    request = requests.get(url).json()['hits']
    for news in request:
        news_info = {
            'title' : news['title'],
            'link' : news['url'],
            'points' : news['points'],
            'author' : news['author'],
            'comments' : news['num_comments'],
            'id' : news['objectID']
        }
        news_new.append(news_info)
    return news_new
def comments_scrapper(url):
    comments=[]
    request = requests.get(url).json()
    news_info = {
        'title' : request['title'],
        'link' : request['url'],
        'points' : request['points'],
        'author' : request['author']
    }
    request_comments = request['children']
    for comment in request_comments:
        author = comment['author']
        text = comment['text']
        if author is not None and text is not None:
            comment_info={
                'author' : author,
                'text' :text            
            }
            comments.append(comment_info)
    return comments, news_info
    
