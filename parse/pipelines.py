import psycopg2
import scrapy
import requests

from food.config import DB_NAME,DB_HOST,DB_PASS,DB_USER
import datetime


class FoodPipeline:
    def __init__(self):
        self.conn = psycopg2.connect(database=DB_NAME, user=DB_USER,
                                password=DB_PASS, host=DB_HOST)  # , port=5432

        self.cur = self.conn.cursor()
        self.cur.execute("Create Table if not EXISTS recipes_dish(name TEXT,"
                    "step_rpeparation text,"
                    "ingradient TEXT,"
                    "img TEXT,"
                         "time TEXT"
                         ");")
        self.conn.commit()

    def __del__(self):
        self.cur.close()

    def updete_data(self, name, img, ingradient, step_preparation, time):
        self.cur.execute("INSERT INTO recipes_dish (name, img, ingradient, step_preparation, time ) VALUES (%s, %s, %s, %s, %s)",
                         (name, img, ingradient, step_preparation, time))

        self.conn.commit()
    def process_item(self, item, spider):
        img = item['img']
        ingradient = item['ingradient']
        ingradient = ' \n '.join(ingradient).replace(':', '')
        name = item['name']
        step_preparation = [i.rstrip().strip() for i in item['step_rpeparation']]
        step_preparation = ''.join(step_preparation)
        time = item['time']
        if img != 'Фото нету':
            print('photo true')
            img = 'http://' + img
            try:
                p = requests.get(img)
                out = open(f"photo\{name}.jpg", "wb")
                out.write(p.content)
                out.close()
                # scrapy.Request(img)
                print('photo download')
            except:
                print('except')
                pass
            print(1)
        self.updete_data(name=name, step_preparation=step_preparation, ingradient=ingradient,
                         img=img, time=time)
        print(1)
        return item
