import scrapy
import csv
from scrapy.crawler import CrawlerProcess


class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = [
        "http://bibliotheque-numerique-sra-bretagne.huma-num.fr/s/sra-bretagne/item/33018"
    ]

    def parse(self, response):
        # Utilisez un sélecteur CSS pour trouver tous les liens CSV
        for link in response.css('a[href$=".csv"]::attr(href)').getall():
            yield scrapy.Request(response.urljoin(link), callback=self.parse_csv)

    def parse_csv(self, response):
        # Extraire le nom du fichier CSV
        filename = response.url.split("/")[-1]

        # Écrire les données CSV dans un fichier
        with open(filename, "wb") as f:
            f.write(response.body)

        self.log(f"Enregistré {filename}")


def main():
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()

if __name__ == "__main__":
    main()