import scrapy


class StatesSpider(scrapy.Spider):
    name = 'states'
    allowed_domains = ['www.earthquaketrack.com']  # http/s is prohibited in this list var
    start_urls = ['https://www.earthquaketrack.com/p/myanmar/recent']

    def parse(self, response):
        #rows = response.xpath("(//div[@class='quakes-info-list col col-lg-4 col-sm-6 col-12'])[1]/div/div")
        rows = response.xpath("//div[@class='quake-info-container']")
        for row in rows:

            # xpath selection on the selected object used
            # timeago = row.xpath(".//abbr[@class='timeago']/text()").get()

            timeago = row.xpath(".//abbr/text()").get()  # xpath selection on the selected object
            scale = row.xpath(".//span/text()").get()
            city = row.xpath(".//a[2]/text()").get()
            region = row.xpath(".//a[3]/text()").get()
            yield {
                #'row': row,
                'timeago': timeago,
                'scale': scale,
                'city': city,
                'region': region
            }

        next_page = response.xpath("//a[@class='next_page']/@href").get()
        #next_page_absolute_path = response.urljoin(next_page)
        next_page_absolute_path = f"https://www.earthquaketrack.com{next_page}"

        #print(next_page)

        if next_page_absolute_path:
            yield scrapy.Request(url=next_page_absolute_path, callback=self.parse)