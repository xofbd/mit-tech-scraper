from urllib.parse import urlencode

from scrapy import Request, Spider

LIMIT = 3

class MITSpider(Spider):
    name = "tech"

    def start_requests(self):
        url_base = "https://tlo.mit.edu/industry-entrepreneurs/available-technologies?"
        if not hasattr(self, "search_term"):
            self.search_term = ""

        for page in range(0, LIMIT + 1):
            query_string = urlencode({
                "search_api_fulltext": self.search_term,
                "page": page,
            })

            url = url_base + query_string
            yield Request(url, self.parse_page_links)

    def parse_page_links(self, response):
        for link in response.css("div.tech-brief-teaser h3 a"):
            yield response.follow(link, self.parse_tech)

    def parse_tech(self, response):
        researchers = (
            response
            .css("div.tech-brief-details__researchers-list ::text")
            .get()
            .split("/")
        )
        researchers = list(map(str.strip, researchers))
        title = response.css("h1.tech-brief-header__title ::text").get()

        try:
            description, problem_addressed = (
                response.css("div.tech-brief-body__inner p ::text")
                .getall()[:2]
            )
        except ValueError:
            description = None
            problem_addressed = None

        yield {
            "title": title,
            "researchers": researchers,
            "description": description,
            "problem_addressed": problem_addressed,
        }

