import pandas as pd

from bs4 import BeautifulSoup

import requests

import re

def fetch_all_posts_in_a_pt_thread(post_url):
    
    res = requests.get(post_url)

    soup = BeautifulSoup(res.content)

    soup = soup.find('div',attrs={'id':'posts'})

    all_posts = soup.find_all('table',attrs={'class':'tborder'})

    all_dicts = []
    for post in all_posts:
        try:
            tmp_dict = fetch_post(post)
            all_dicts.append(tmp_dict)
        except:
            pass
    dataframe = pd.DataFrame(all_dicts)
    
    dataframe['post_url'] = post_url
    
    return dataframe

def fetch_post(post_tag):
    
    tmp_dict = {}
    
    user_link = 'http://www.proteacher.net/discussions/' + post_tag.find('a',attrs={'class':'bigusername'}).get('href')

    username = post_tag.find('a',attrs={'class':'bigusername'}).text
    
    tmp_dict['user_link'] = user_link
    
    tmp_dict['username'] = username
    
    try:
        user_details_string = post_tag.find('div',attrs={'class':'smallfont'}).text.strip()
                
        user_details = user_details_string.replace('\n','').replace('\t','').replace('                                        ','')
        
        user_details = user_details.split('\r\r')

        joined_date = user_details[0]
        
        tmp_dict['joined_date'] = joined_date

        no_of_posts = user_details[1]
        
        tmp_dict['no_of_posts'] = no_of_posts

        membership_type = user_details[2]
        
        tmp_dict['membership_type'] = membership_type
        
    except:
        user_details_string = post_tag.find('div',attrs={'class':'smallfont'}).text.strip()
            
    post_title = post_tag.find('strong').text
    
    tmp_dict['post_title'] = post_title
    
    posted_date = post_tag.find('td',attrs={'align':'left'}).text.split('\t\t\t')[1]
    
    tmp_dict['posted_date'] = posted_date
    
    tmp_dict['post_text'] = post_tag.find('div',attrs={'id':re.compile('post_message_')}).text
    
    tmp_dict['user_details'] = user_details_string

    return tmp_dict
    