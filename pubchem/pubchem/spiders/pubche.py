import scrapy
from scrapy_playwright.page import PageMethod

class PubcheSpider(scrapy.Spider):
    name = "pubchem"
    allowed_domains = ["pubchem.ncbi.nlm.nih.gov"]
# 
# 10225 11349 12232 24721137 3083613 181119 474540 124017 5280666 5321288 51029223 5318517 5316836
# 5281674 5971 5458800 65126 73419 66841 82143 68071 7462
    def start_requests(self):
        urls = "10225 11349 12232 24721137 3083613 181119 474540 124017 5280666 5321288 51029223 5318517 5316836 5281674 5971 5458800 65126 73419 66841 82143 68071 7462"

        IGNORED_DOMAINS = ['www.google-analytics.com']
        ram = urls.split(" ")
        for i in ram[0:]:
            if not i:
                continue

            url = f"https://pubchem.ncbi.nlm.nih.gov/compound/{i}"
            self.logger.debug(f"Processing URL: {url}")

            request = scrapy.Request(
                url,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("wait_for_selector", "section#Information-Sources")
                    ],
                ),
                callback=self.parse,
                errback=self.errback,  # Handle errors with the specified errback
            )
            yield request

    def parse(self, response):
        self.logger.debug("Parsing page")
        kegg_id = response.xpath("//section[@id='KEGG-ID']//div[@class='break-words space-y-1']/a/text()").get()

        yield {
            'Pubchem_id': response.xpath("//section[@id='Title-and-Summary']//div[text()='PubChem CID']/following-sibling::div/text()").get(),
            "iupac_name": "".join(response.xpath("//section[@id='IUPAC-Name']//div[@class='break-words space-y-1']//text()").getall()),
            "molecular_formula": "".join(response.xpath("//section[@id='Molecular-Formula']//div[@class='break-words space-y-1']//span//text()").getall()),
            "molecular_weight": response.xpath("//div[@class='sm:table-row-group']/div[1]//div[@class='break-words space-y-1']/text()").get()[:6],
            "kegg_id": kegg_id if kegg_id else "Not available",
        }

    def should_ignore_request(self, request):
        # Ignore requests to Qualtrics and Google Analytics
        ignored_domains = ['siteintercept.qualtrics.com', 'www.google-analytics.com']

        return any(domain in request.url for domain in ignored_domains)

    def errback(self, failure):
        self.logger.error(f"Error processing request: {failure.getErrorMessage()}")
        page = failure.request.meta.get("playwright_page")
        if page:
            page.close()
