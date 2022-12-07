import scrapy


class SteamSpider(scrapy.Spider):
    name = 'steam_parse_games'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['http://store.steampowered.com']
    queries = ['horrors', 'football', 'adventure']
    count_of_pages = 2

    def start_requests(self):
        for query in self.queries:
            for i in range(1, 1 + self.count_of_pages):
                url = f'https://store.steampowered.com/search/?term={query}&page={i}'
                yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        games = []
        for href in response.xpath("//div[@id='search_resultsRows']/a/@href").extract():
            games.append(href)

        for i in games:
            yield scrapy.Request(i, callback=self.parse)

    def parse(self, response):
        items = {}
        name = response.xpath('//div[@id="appHubAppName"]/text()').extract()
        category = response.xpath('//div[@class="blockbg"]/a/text()').extract()
        reviews_count = response.xpath('//div[@class="summary column"]/span[@class="responsive_hidden"]/text()').extract()
        mark = response.xpath('//div [@class="summary column"]/span[@class="nonresponsive_hidden responsive_reviewdesc"]/text()').extract()
        release_date = response.xpath('//div[@class="release_date"]/div[@class="date"]/text()').extract()
        developer = response.xpath('//div[@id="developers_list"]/a/text()').extract()
        tags = response.xpath('//a[@class="app_tag"]/text()').extract()
        price = response.xpath('//div[@class="game_purchase_price price"]/text()').extract()
        platforms = response.xpath('//div[@class="sysreq_tabs"]/div/text()').extract()
        items["name"] = ''.join(name)
        items["category"] = ', '.join(category).replace('All Games', '')
        reviews_c = ''.join(reviews_count).replace("\n", "").replace("\t", "").replace("\r", "").split(')(')
        if len(reviews_c) > 1:
            items["reviews_count"] = reviews_c[1].replace(')', '').replace('(', "")
        else:
            items["reviews_count"] = reviews_c[0].replace(')', '').replace('(', "")
        items["mark"] = str(int(''.join(mark).replace("\n", "").replace("\t", "").replace("\r", "").split('%')[0][2:]) / 10)
        items["release_date"] = ''.join(release_date)
        items["developer"] = ''.join(developer)
        items["tags"] = ', '.join(tags).replace("\n", "").replace("\t", "").replace("\r", "")
        items["price"] = ''.join(price).replace("\n", "").replace("\t", "").replace("\r", "").split('.')
        if items["price"] == [""]:
            price = response.xpath('//div[@class="discount_final_price"]/text()').extract()
            items["price"] = ''.join(price).replace("\n", "").replace("\t", "").replace("\r", "").split('.')
        items["platforms"] = ', '.join(platforms).replace("\n", "").replace("\t", "").replace("\r", "")
        if not items["platforms"]:
            items["platforms"] = "Windows"
        yield items
