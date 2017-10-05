import wikipedia
import tweepy
from flickrapi import FlickrAPI
import os


# 0: Twitter
# 1: Wikipedia
# 2: Flickr

def get_result(api_raw, search_text):

    result_text = []
    result_images = []

    api_raw = str(api_raw)
    api = get_api(api_raw.lower())
    if api == 0:
        # Twitter
        ACCESS_KEY = os.environ['ACCESS_KEY']
        ACCESS_SECRET = os.environ['ACCESS_SECRET']
        CONSUMER_KEY = os.environ['CONSUMER_KEY']
        CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)
        twitter_search = api.search(search_text)
        for result in twitter_search:
            result_text.append(result.text)
    elif api == 1:
        # Wikipedia
        try:
            wikiPage = wikipedia.page(search_text)
            result_text.append(wikiPage.summary)
            result_images = wikiPage.images
        except wikipedia.WikipediaException:
            result_text.append("Sorry, no page matched your search '" + search_text + "'.")
            result_images.append(None)
    elif api == 2:
        # Flickr
        FLICKR_PUBLIC = os.environ['FLICKR_PUBLIC']
        FLICKR_SECRET = os.environ['FLICKR_SECRET']
        flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
        extras = 'url_c,url_l,url_o'
        results = flickr.photos.search(tags=search_text, per_page=25, extras=extras)
        for rslt in results['photos']['photo']:
            if 'url_l' in rslt:
                result_images.append(rslt['url_l'])
            elif 'url_c' in rslt:
                result_images.append(rslt['url_c'])
            elif 'url_o' in rslt:
                result_images.append(rslt['url_o'])
            if 'title' in rslt:
                title = str(rslt['title'])
                if len(title) > 0:
                    lines = title.splitlines()
                    result_text.append(lines[0])
                    print(lines[0])
                else:
                    result_text.append("")

    return result_text,result_images


def get_api(api_raw):
    if api_raw.startswith('t'):
        return 0
    if api_raw.startswith('w'):
        return 1
    if api_raw.startswith('f'):
        return 2
    if api_raw.startswith('0'):
        return 0
    if api_raw.startswith('1'):
        return 1
    if api_raw.startswith('2'):
        return 2