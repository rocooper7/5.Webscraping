import scrapy
from scrapy.crawler import CrawlerProcess

class Spider12(scrapy.Spider):
    name = 'Spider12'
    allowed_domains = ['pagina12.com.ar']
    custom_settings = {'DEPTH_LIMIT': 5,
                       'FEED_FORMAT': 'json',  #csv
                       'FEED_URI': 'resultados.json',   #.csv
                       'ROBOTSTXT_OBEY': True, 
                       'FEED_EXPORT_ENCODING': 'utf-8',}
                       
    start_urls = ['https://www.pagina12.com.ar/secciones/el-pais',
                  'https://www.pagina12.com.ar/secciones/economia',
                  'https://www.pagina12.com.ar/secciones/sociedad',
                  'https://www.pagina12.com.ar/suplementos/cultura-y-espectaculos',
                  'https://www.pagina12.com.ar/secciones/ciencia',
                  'https://www.pagina12.com.ar/secciones/el-mundo',
                  'https://www.pagina12.com.ar/secciones/deportes',
                  'https://www.pagina12.com.ar/secciones/contratapa']
   
    def parse(self, response):
        # Artículo principal
        nota_principal = response.xpath('//article[@class="article-item article-item--main "]//div[@class="article-item__content"]//h2/a/@href').get()
        if nota_principal is not None:
            yield response.follow(nota_principal, callback= self.parse_nota)

        # Sub-Artículos principales
        subnotas_principales = response.xpath('//article[@class="article-item article-item--featured "]//div[@class="article-item__content"]//h3/a/@href').getall()
        for subnota in subnotas_principales:
            yield response.follow(subnota, callback= self.parse_nota)    

        # Listado de notas
        notas = response.xpath('//div[@class="articles-list"]//div[@class="article-item__header"]//a/@href').getall()
        for nota in notas:
            yield response.follow(nota, callback= self.parse_nota)

        # Link a próxima página
        next = response.xpath('//a[@class="next"]/@href').get()
        if next is not None:
            yield response.follow(next, callback= self.parse)

    def parse_nota(self, response):
        # Parseo la nota
        seccion = response.xpath('//div[@class="suplement"]//text()').get()
        titulo = response.xpath('//h1[@class="article-title"]/text()').get()
        cuerpo = ''.join(response.xpath('//div[@class="article-text"]//text()').getall())
         
        yield {'url': response.url,
               'seccion': seccion,
               'titulo': titulo,
               'cuerpo': cuerpo}


if __name__ == '__main__':

    process = CrawlerProcess()
    process.crawl(Spider12)
    process.start()