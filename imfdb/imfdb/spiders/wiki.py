# -*- coding: utf-8 -*-
import scrapy
from imfdb.items import ImfdbItem
from scrapy.selector import HtmlXPathSelector 

class WikiSpider(scrapy.Spider):
	name = "wiki"
	allowed_domains = ["imfdb.org"]
	start_urls = ["http://www.imfdb.org/wiki/Beretta_92_pistol_series"]

	def parse(self, response):
		self.log("\t\tVisited: " + response.url)
		wiki_table = response.xpath('//table[@class="wikitable"]')[0:1]
		films = wiki_table.css('i > a::attr(href)').extract()

		for film in films:
			next_page = "http://www.imfdb.org" + film
			yield scrapy.Request(next_page, callback=self.parse_page)

	def parse_page(self, response):
		image_urls = response.xpath('//img/@src').extract()
		images= response.xpath('//a[@class="image"]')
		items = []

		for image in images:
			item = ImfdbItem()
			link=image.xpath('@href').extract()[0]
			if(link.find("Question_mark") == -1):
				link = 'http://imfdb.org/'+link
				yield  scrapy.Request(link, callback=self.downloadParse)
				
	def downloadParse(self, response):
		
		for elem in response.xpath("//img"):
			img_url_list = elem.xpath("@src").extract()
			for img_url in img_url_list:
				if(not ("http://ox-d.gunbroker.com" in img_url) and not("/skins/" in  img_url) and not('thumb' in img_url)):
					link = 'http://www.imfdb.org'+ img_url
					yield {'image_urls': [link]}