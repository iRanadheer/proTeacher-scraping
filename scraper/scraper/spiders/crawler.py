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
    

    rules = (
        Rule(LinkExtractor(allow=r'proteacher',deny=r'#post'), callback='parse_url',follow=True),
        )
    
    custom_settings = dict()
    custom_settings['DEPTH_LIMIT'] = 0
    custom_settings['USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'


    def extract_external_urls(self, response):
        extractor = LinkExtractor()
        links = extractor.extract_links(response)
        all_links = []
        for link in links:
            url = link.url
            all_links.append(url)
        return url

    def parse_url(self, response):
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


# class CrawlerSpider(scrapy.Spider):
#     name = 'crawler'
#     start_urls = ['http://www.proteacher.net']

#     rules = (
#         Rule( callback='parse_url',follow=True),
#         )
#     def parse_url(self, response):
#         items = dict()
#         if response.status == 200:
#             # url = response.url
#             # if 'showthread.php' in url:
#             #     dataframe = fetch_all_posts_in_a_pt_thread(url)
#             #     yield dataframe
#             url = response.url
#             items['url'] = url
#             yield items