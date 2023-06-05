import scrapy
import csv
import requests
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin

class BibliScraper(scrapy.Spider):
    name = "bibli_scraper"
    start_urls = [
        "http://bibliotheque-numerique-sra-bretagne.huma-num.fr/s/sra-bretagne/item?fulltext_search=&property%5B0%5D%5Bjoiner%5D=and&property%5B0%5D%5Bproperty%5D=&property%5B0%5D%5Btype%5D=eq&property%5B0%5D%5Btext%5D=&resource_class_id%5B0%5D=&resource_template_id%5B0%5D=&item_set_id%5B0%5D=&site_id=&owner_id=&submit=Recherche&page=1&sort_by=created&sort_order=desc"
    ]
    pages_visited = 0  # Variable de classe pour suivre le nombre de pages parcourues
    data = []  # Liste pour stocker les données des pages

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Extraire les liens dans les balises <div class="identifier">
        for href in response.css("div.identifier a::attr(href)").extract():
            # Suivre chaque lien pour extraire le nom du fichier CSV
            yield scrapy.Request(
                url=response.urljoin(href),
                callback=self.parse_csv
            )

        # Extraire le lien vers la page suivante et suivre ce lien si disponible
        next_page_link = response.css("a[title='Suivant']::attr(href)").get()
        if next_page_link and self.pages_visited < 87:  # Arrêter après 87 pages
            self.pages_visited += 1
            yield response.follow(next_page_link, callback=self.parse)

    def parse_csv(self, response):
        # Extraire le lien du fichier CSV avec le texte "csv"
        csv_link = response.xpath("//a[text()='csv']/@href").get()
        full_csv_link = urljoin(response.url, csv_link)  # Construire l'URL complète
        
        # Effectuer une requête HTTP pour obtenir le contenu du fichier CSV
        csv_response = requests.get(full_csv_link)
        
        if csv_response.status_code == 200:
            # Extraire le contenu CSV
            csv_content = csv_response.content.decode('utf-8')
            
            # Traiter le contenu CSV comme souhaité
            # Par exemple, tu peux l'écrire dans un fichier CSV ou le traiter avec la bibliothèque pandas
            # avec open("output.csv", "w") as f:
            #     f.write(csv_content)
            #
            # dataframe = pd.read_csv(csv_response.content)
            #
            # ...
            
            # Extraire les lignes de données du contenu CSV
            csv_rows = csv_content.splitlines()
            
            # Ajouter les lignes de données à la liste
            self.data.extend(csv.reader(csv_rows[1:]))

            self.log(f"Données du CSV extraites")

    def closed(self, reason):
        # Écrire les données dans le fichier CSV
        with open("output.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(self.data)

        self.log("Données écrites dans le fichier CSV")

def main():
    process = CrawlerProcess()
    process.crawl(BibliScraper)
    process.start()

if __name__ == "__main__":
    main()
