#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from requests import get
from bs4 import BeautifulSoup
import os
import pandas as pd
import numpy as np

headers = {'User-Agent': 'Codeup Data Science - Kalpana'}
topics = ["business","sports","technology","entertainment"]
urls = ['https://codeup.com/data-science/jobs-after-a-coding-bootcamp-part-1-data-science/',
        'https://codeup.com/data-science/math-in-data-science/',
        'https://codeup.com/data-science/transition-into-data-science/',
        'https://codeup.com/data-science/data-science-career/',
        'https://codeup.com/data-science/data-science-without-a-degree/']


def get_blogs(urls,headers):
    '''
    Given a list of URLs of Codeup blog articles, returns a list of dictionaries containing the url, blog title and blog content.
    '''
    filename = 'codeup_blogs_raw.csv'

    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        blog_list = []
        for url in urls:
            #get page info
            response = get(url,headers=headers)
            #turn into soup object
            soup = BeautifulSoup(response.content,'html.parser')
            
            blog_dict = {
                'url': url,
                'title': soup.title.text,
                'content': soup.select('.entry-content')[0].text
            }
            blog_list.append(blog_dict)
            df = pd.DataFrame(blog_list)
        df.to_csv(filename, index=False)
        return df

def get_news(topics,headers):
    '''
    Given a list of news topics, retrieve the title and content for all articles in that inshorts topic.
    '''
    filename = 'inshorts_raw.csv'

    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        base_url = 'https://inshorts.com/en/read/'
        article_list = []
        for t in topics:
            #create section url
            topic_url = base_url + t
            #get the content
            response = get(topic_url,headers=headers)
            #convert to soup
            soup = BeautifulSoup(response.content,'html.parser')
            #get the headline for each article in this topic - list of headlines
            headlines = soup.find_all(itemprop="headline")
            #get the content for each article - list of article bodies
            bodies = soup.find_all(itemprop="articleBody")
            
            #loop over the 'cards' 
            #but really just looping over the list of headlines and article bodies
            for title, content in zip(headlines, bodies):
                #add all to dictionary
                art_dict = {
                    'title': title.text,
                    'content': content.text,
                    'category': t
                }
                #append this article to the list
                article_list.append(art_dict)
            df = pd.DataFrame(article_list)
        df.to_csv(filename, index=False)
        return df
    
################################################################   

def get_post_details(post):
    """ Returns dictionary of url, title, date published, and content for each post on the Codeup.com/blog site"""
    output = {}
    # Extract URL
    output['url'] = post.select('a')[0].attrs['href']
    # Extract title
    output['title'] = post.text.strip()
    # Extract date published
    output['date_published'] = post.select('span.published')[0].text
    # Extracts blog post contents
    output['original'] = get_blog_content(output['url'])
    
    return output

def get_blog_content(url):
    """ Returns the content of the blog post from Codeup.com/blog """
    headers = {'User-Agent': 'Codeup Data Science'} # Some websites don't accept the python-requests default user-agent
    response = get(url, headers=headers)


    # Make a soup variable holding the response content
    soup = BeautifulSoup(response.content, 'html.parser')
    entry_text = ""
    # Adds the blog post contents to the string
    for t in soup.select('div.entry-content'):
        entry_text += t.text.strip()
    return entry_text

def get_blog_articles(use_cache = True):
    """ Returns dictionary of information about blog posts on codeup.com/blog site """
    
    filename = 'blog.csv'
    
    if use_cache and os.path.exists(filename):
        return pd.read_csv(filename).dropna().to_dict()
        
    url = 'https://codeup.com/blog/'
    headers = {'User-Agent': 'Codeup Data Science'} # Some websites don't accept the python-requests default user-agent
    response = get(url, headers=headers)


    # Make a soup variable holding the response content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    pd.DataFrame([get_post_details(post) for post in soup.select('article.et_pb_post')]).dropna().to_csv(filename, index=None)
    

    return [get_post_details(post) for post in soup.select('article.et_pb_post')]

#### NEWS SITE SCRAPING (inshorts) ####
def get_category_news_cards(category):
    """ Returns list with each item the soup for a different news card from the category page"""
    
    # Note that having the category name capitalized sends you to a different website than lowercase!!
    # Generates url for the category from which we want to scrape the news
    base_url = r'https://inshorts.com/en/read'
    url = base_url +r'/'+category.lower()
    
    headers = {'User-Agent': 'Codeup Data Science'} # Some websites don't accept the python-requests default user-agent
    response = get(url, headers=headers)

    # Make a soup variable holding the response content for each category 
    cat_soup = BeautifulSoup(response.content, 'html.parser')
    
    # Selects each news card within the category's 
    return cat_soup.select('div.news-card.z-depth-1')

def get_news_details(news_card, category):
    """ Returns dictionary with information about the article 
    news_card: the soup for an individual news card within a category card stack
    category: this is passed to this function so it can be added to the dictionary"""
    
    output={}
    output['title'] = news_card.select('div.news-card-title')[0].find("span").text
    output['author'] =  news_card.select('div.news-card-author-time')[0].find('span', class_='author').text
    output['datetime'] = news_card.select('div.news-card-author-time')[0].find('span', class_='time').attrs['content']
    output['category'] = category.lower()
    output['original'] = news_card.select('div.news-card-content')[0].find('div').text
    
    return output
    
def get_each_news_in_category(category):
    """ Returns list of dictionaries for each article in the category with article information
    category: string of category name from inshorts """
    
    # India news appears to be outdated - national category gets updated
    if category == 'india':
        category = 'national'
        
    # Get a list of soup objects for each news card    
    list_of_news_cards = get_category_news_cards(category)
    
    print("Total News Articles in Category: ",len(list_of_news_cards))
    
    # Return list of dictionaries with the contents (headline, author, etc.) of each news card
    return [get_news_details(news_card, category) for news_card in list_of_news_cards]
    
def get_news_categories(soup):
    """ Returns list of news categories from the inshorts homepage 
    soup: the soup object returned by the response from inshorts.com/en/read """
    
    # Selects the category list, and from that only the active-category. The first element is "All News" so this is skipped.
    categories = soup.select('ul.category-list')[0].select('li.active-category')[1:]
    
    # Convert categories to lower case
    return [c.text.lower() for c in categories]

def get_news_articles(desired_categories = 'all', get_fresh_news = False):
    """ Returns dictionary of news article information from https://inshorts.com/ or from cached csv.
    desired_categories: 'all' by default or a list of categories desired
    get_fresh_news: if True returns fresh news and writes fresh news to news.csv """
    
    # Filepath for cache
    news_cache_file = 'news.csv'
    
    # Check whether we want fresh news. If not, simply reads from cached csv. If cached csv does not exist then automatically collects fresh news
    if not get_fresh_news:
        # Checks if cache exists
        if os.path.exists(news_cache_file):
            print("Importing from csv")
            return pd.read_csv('news.csv').dropna().to_dict()
        else:
            print("News cache does not exist, acquiring fresh news...")
            # Condition when don't want fresh news but no cache exists, ensure new data is cached to csv
            need_cache = True
    
    
    url = 'https://inshorts.com/en/read'
    headers = {'User-Agent': 'Codeup Data Science'} # Some websites don't accept the python-requests default user-agent
    response = get(url, headers=headers)


    # Make a soup variable holding the response content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Generate the list of category names
    categories = get_news_categories(soup)
    
    # Initialize news list
    news = []
    
    # Check if we want articles from all categories or just specific ones
    if desired_categories == 'all':
        
        # Iterate through each category, scraping each article, save details to news list
        for cat in categories:
            
            print("Scraping category: ", cat)
            news+=get_each_news_in_category(cat)
    else:
        # For the case when we only want to scrape articles in particular categories
        for cat in desired_categories:
            # Checks if the desired category exists. If it doesn't moves on to the next category desired
            if cat.lower() not in categories:
                print(cat,"does not exist at site, skipping scraping of this category")
                continue
            print("Scraping category: ", cat)
            news+=get_each_news_in_category(cat)
    
    # Write results to cache
    if get_fresh_news or need_cache:
        pd.DataFrame(news).dropna().to_csv(news_cache_file, index = None)
       
    return news

