from urllib.parse import urlencode

from scrapy import Request, Spider

LIMIT = 3

class MITSpider(Spider):
    name = "tech"

    def start_requests(self):
        url_base = "https://tlo.mit.edu/technologies?"
        if not hasattr(self, "search_term"):
            self.search_term = ""

        for page in range(1, LIMIT + 1):
            query_string = urlencode({
                "search_api_views_fulltext": self.search_term,
                "page": page,
            })

            url = url_base + query_string
            yield Request(url, self.parse_page_links)

    def parse_page_links(self, response):
        for link in response.css("span.field-content > a"):
            yield response.follow(link, self.parse_tech)
    
    def parse_tech(self, response):
        inventors = response.css("div.field-name-field-inventors h2 ::text").getall()
        title = response.css("h1.title#page-title ::text").get()
        application, problem_addressed = (
            response.css("section#block-system-main div.field-name-field-body ::text")
            .getall()[:2]
        )

        yield {
            "inventors": inventors,
            "title": title,
            "application": application,
            "problem_addressed": problem_addressed,
        }

        
