import sqlite3
from datetime import date
from transformers import pipeline

TODAY = date.today()

#API
finetuned_checkpoint = "peter2000/xlm-roberta-base-finetuned-ecoicop"
classifier = pipeline("text-classification", model=finetuned_checkpoint)
print('API LOAD')


class StorePipeline(object):

    def __init__(self):
        self.con = sqlite3.connect('Products.db')
        self.cur = self.con.cursor()

    def crate_table(self, store):
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {store}(
        name text,
        category text,
        price text,
        image text,
        date text,
        label,
        score
        )""")

    def delete_row(self, store, name):
        self.cur.execute(f"""DELETE FROM {store} WHERE date = ? AND name = ?""", (TODAY, name))

    def process_item(self, item, spider):
        name = item['name']
        store = item['store']
        self.crate_table(store)
        self.delete_row(store, name)

        cla = classifier(f'{item["category"]} <sep> {item["name"]} <sep> {item["url"]}')

        self.cur.execute(f"""INSERT OR IGNORE INTO {store} VALUES(?,?,?,?,?,?,?)""",
                         (item['name'],
                          item['category'],
                          item['price'],
                          item['image'],
                          item['date'],
                          cla[0].get('label'),
                          cla[0].get('score')))


        self.con.commit()
        return item
