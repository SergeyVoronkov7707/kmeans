import scrapy

from food.items import FoodItem


class RussianFoodSpider(scrapy.Spider):
    dict_products = {
        '2' : 'Первые блюда',
        '3' : 'Вторые блюда',
        '4' : 'Рецепты напитков',
        '5' : 'Рецепты изделий из теста',
        '6' : 'Рецепты закусок',
        '7' : 'Рецепты сладостей',
        '8' : 'Рецепты заготовок',
        '9' : 'Рецепты соусов',
        '69' : 'Рецепты приправ',
        '1535' : 'Рецепты маринада',
    }

    name = 'gastronom'
    allowed_domains = ['www.gastronom.ru']
    start_urls = ['https://www.gastronom.ru/catalog']

    def parse(self, response):
        all_categories = response.xpath("//a[@class='col-catalog__link_cloud']/@href").extract()
        for link in all_categories:
            yield response.follow(link, callback=self.parse_categories)
        print(1)




    def parse_categories(self, response):
        link_recipes = response.xpath("//a[@class='material-anons__title']/@href").extract()
        next_page = response.xpath("//a[@class='pagination__arrow-next  ']/@href").extract()
        print(1)
        for link in link_recipes:
            yield response.follow(link, callback=self.parse_recipes)
        if next_page:
            if len(next_page[0]) > 2:
                yield response.follow(next_page[0], callback=self.parse_categories)


    def parse_recipes(self, response):
        print(1)
        name = response.xpath("//h1[@class='recipe__title']/text()").extract_first()
        time = response.xpath("//div[@class='recipe__summary-list-des recipe__summary-list-des_big']/text()").extract_first()
        ingradient = response.xpath("//li[@class='recipe__ingredient']/text()").extract()
        step_rpeparation = response.xpath("//div[@class='recipe__step-text']/text()").extract()
        img = response.xpath("//div[@class='main-slider__image-wrap']/img/@src").extract_first()
        if img:
            img = self.allowed_domains[0]+img
            # img = img
        else:
            img = 'Фото нету'
        if len(ingradient) >= 1:
            yield FoodItem(name=name, time=time, ingradient=ingradient,step_rpeparation=step_rpeparation,img=img )
