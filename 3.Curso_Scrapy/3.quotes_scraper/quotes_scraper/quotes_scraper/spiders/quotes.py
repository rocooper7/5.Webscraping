import scrapy

# Título = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# Top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()
# Next page button = //ul[@class="pager"]//li[@class="next"]/a/@href


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]
    custom_settings = {
        'FEED_URI': 'quotes.json',  #Puede ser csv tambien 
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 24,   #No. de peticiones
        'MEMUSAGE_LIMIT_MB': 2048,   #Memoria RAM para trabajar Scrapy
        'MEMUSAGE_NOTIFY_MAIL': ['facundo@platzi.com'],   #Cuando se pasa del RAM notifica al admon 
        'ROBOTSTXT_OBEY': True,      #No problemas legales
        'USER_AGENT': 'PepitoMartinez',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse_only_quotes(self, response, **kwargs):      #Se crea el metodo para extraer las quotes y con kwargs se desempaqueta mis quotes 
        if kwargs:
            quotes = kwargs['quotes']   #Accedemos a los valores de quotes, quotes es una lista 
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()) #A la lista quotes se le aplica la funcion de lista extend para seguir agregando info
        #En este caso se agrega las quotes de la segunda pagina 
        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})  #Se repite el proceso de ir a otra pagina 
        else:    #Cuando ya no hay mas botones de next page 
            yield {
                'quotes': quotes
            }

    def parse(self, response):
        title = response.xpath('//h1/a/text()').get()   #Nos trae listas 
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        top_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall(
        )

        top = getattr(self, 'top', None)   #Este pedazo de codigo nos ayuda a extraer el top 10 que se quiera extraer
        if top:
            top = int(top)
            top_tags = top_tags[:top]

        yield {           # yield es un return parcial de datos, retoma el estado que tenia y puede seguir haciendo returns
            'title': title,     #Se quita quotes:quotes y se manda como kwargs en follow
            'top_tags': top_tags
        }

        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()    
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})  #quotes trae las quotes de la 1ra pagina
            #Follow nos lleva a la pagina 2, callback repite el proceso, y en vez de poner en callback el metodo parse, 
            # le pasamos el metodo parse only quotes para que solo traiga las quotes y ya no el title y las top_tags 
