import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

import sys
sys.path.append('../../../utils/')

from library import fetch_all_posts_in_a_pt_thread
from db_functions import add_data_to_db



class MySpider(CrawlSpider):
    name = 'crawler'
    start_urls = ['http://www.proteacher.net']
    
    """
    We are restricting the spider to look for specific allow regex and deny regex. The post url contains #(post number in that thread). 
    There is no need for fetching the same post multiple times. So, we will ignore all the individual post urls, which is what added to deny regex.
    """
    rules = (
        Rule(LinkExtractor(allow=r'proteacher',deny=r'#post'), callback='parse_url',follow=True),
        )
    
    custom_settings = dict()
    custom_settings['DEPTH_LIMIT'] = 0
    custom_settings['USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'


    def parse_url(self, response):
        """
        The actual post url will have showthread.php in it. The function to get all the posts will throw errors if we pass non-post urls to it. 
        To avoid unnecessary processing, we are instructing the spider to look if the particular substring exists in the url, if yes, then go and fetch all the posts.
        Ignore otherwise. 

        We are creating a new unique identifier called uid, which is the primary key for the database and ignore all the duplicate urls. 
        It would be better if we include other columns as well in hashing, because the same user can post multiple times in a thread which we may exclude those from 
        adding into the database. 
        """
        if response.status == 200:    
            item = dict()
            url = response.url
            item['url'] = url
            if 'showthread.php' in url:
                dataframe = fetch_all_posts_in_a_pt_thread(url)
                dataframe['uid'] = dataframe['username'] + dataframe['post_url']
                dataframe['uid'] = dataframe['uid'].map(hash)
                add_data_to_db(dataframe)
                yield None
