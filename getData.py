import scrapy
import csv
import pandas as pd
from scrapy.crawler import CrawlerProcess
import mergeCsv

class BibliScraper(scrapy.Spider):
    name = "bibli_scraper"
    start_urls = [
        "http://bibliotheque-numerique-sra-bretagne.huma-num.fr/s/sra-bretagne/item?fulltext_search=&property%5B0%5D%5Bjoiner%5D=and&property%5B0%5D%5Bproperty%5D=&property%5B0%5D%5Btype%5D=eq&property%5B0%5D%5Btext%5D=&resource_class_id%5B0%5D=&resource_template_id%5B0%5D=&item_set_id%5B0%5D=&site_id=&owner_id=&submit=Recherche&page=1&sort_by=created&sort_order=desc"
    ]

    def parse(self, response):
        # Extraire les liens dans les balises <div class="identifier">
        for href in response.css("div.identifier a::attr(href)").extract():
            # Suivre chaque lien pour extraire le nom du fichier CSV
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_csv
            )
        """
        # Créer une nouvelle requête pour la page suivante, si elle existe
        next_page_url = response.css(".next.o-icon-next.button::attr(href)").get()
        if next_page_url:
            yield scrapy.Request(
            url=response.urljoin(next_page_url),
            callback=self.parse
          )
          """

    def parse_csv(self, response):
        # Extraire le nom du fichier CSV
        filename = response.css("a[href$='.csv']::attr(href)").get().split("/")[-1]
        
        # Lire les données CSV à partir de la réponse HTTP

        # Écrire les données CSV dans un fichier
        with open(filename, "wb") as f:
            f.write(response.body)

        self.log(f"Enregistré {filename}")

   


def main():
    process = CrawlerProcess()
    process.crawl(BibliScraper)
    process.start()
    mergeCsv.mergeCsvCurrDir()

if __name__ == "__main__":
    main()
    