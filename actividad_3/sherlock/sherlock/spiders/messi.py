import scrapy
import html2text
converter = html2text.HTML2Text()
converter.ignore_links = True
converter.ignore_images = True
converter.ignore_tables = True
import re

def extraer_links(texto):
    links = []
    for doi in re.findall('(10[.][0-9]{4,}[^\s"/<>]*/[^\s"<>]+)', texto):
        links.append('https://dx.doi.org/'+doi[:-1])
    return links

class MessiSpider(scrapy.Spider):
    name = 'messi'
    #allowed_domains = ['prueba.com']
    start_urls = ['https://pubmed.ncbi.nlm.nih.gov/?term=cultural+evolution&filter=simsearch2.ffrft']

    def parse(self, response):
        texto = converter.handle( response.css("*").get() )
        texto = texto.encode("ascii", "ignore")
        mis_links =  extraer_links( str(texto) )
        i = 1
        for link in mis_links:
            yield scrapy.Request( link, callback=self.parse_paper, cb_kwargs=dict( num=str(i) ) )
            i = i + 1
        #with open('baldness_links.txt', 'w') as f:
            #for item in mis_links:
                #link = 'https://dx.doi.org/'+item[:-1]
                #f.write("%s\n" %link)

    def parse_paper(self, response, num):
        if hasattr(response, "text"):
            texto = converter.handle( response.css("*").get() )
            texto = texto.encode("ascii", "ignore")
            f = open("cultevo_"+num+".txt", "w")
            f.write( str(texto) )
            f.close()
