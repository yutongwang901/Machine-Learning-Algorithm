import scrapy
from scrapy.crawler import CrawlerProcess
import json
import csv

class FolksySpider(scrapy.Spider):
    name = 'folksy_post'
    start_urls = []
    for i in range(200):
        start_urls.append('https://talk.folksy.com/latest.json?no_definitions=true&order=default&page={}'.format(i+1))
        post_url = 'https://talk.folksy.com/t/%s.json?track_visit=true&forceLoad=true'
    download_delay = 2.5
    custom_settings={ 'FEED_URI': "folksy_post.csv",'FEED_FORMAT': 'csv'}

    
    def parse(self, response):
        data = json.loads(response.body)
        for topic in data['topic_list']['topics']:
            yield scrapy.Request(self.post_url % topic.get('id'), callback=self.parse_post)

    def parse_post(self, response):
        data_new = json.loads(response.body)
        for posts in data_new['post_stream']['posts']:
            yield {'id': posts['id'],
                   'username': posts['username'],
                   'created_at': posts['created_at'],
                   'cooked': posts['cooked'],
                   'post_number': posts['post_number'],
                   'updated_at': posts['updated_at'],
                   'reply_count': posts['reply_count'],
                   'reply_to_post_num': posts['reply_to_post_number'],
                   'reads': posts['reads'],
                   'topic_id': posts['topic_id'],
                   'user_id': posts['user_id']
            }

process = CrawlerProcess()
process.crawl(FolksySpider)
process.start()



