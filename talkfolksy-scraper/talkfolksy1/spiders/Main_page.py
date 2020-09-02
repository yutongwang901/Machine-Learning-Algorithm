import scrapy
from scrapy.crawler import CrawlerProcess
import json
import csv

class FolksySpider(scrapy.Spider):
    name = 'folksy_main'
    start_urls = []
    for i in range(200):
        start_urls.append('https://talk.folksy.com/latest.json?no_definitions=true&order=default&page={}'.format(i+1))
    download_delay = 2.5
    custom_settings={ 'FEED_URI': "folksy.csv",'FEED_FORMAT': 'csv'}


    
    def parse(self, response):
        data = json.loads(response.body)
        for topic in data['topic_list']['topics']:
            yield{
                'id': topic['id'],
                'title': topic['title'],
                'created_at': topic['created_at'],
                'last_posted_at': topic['last_posted_at'],
                'views': topic['views'],
                'like_count': topic['like_count'],
                'category_id': topic['category_id']
            }

process = CrawlerProcess()
process.crawl(FolksySpider)
process.start()