import sqlite3
from datetime import date

TODAY = date.today()


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
        date text
        )""")

    def delete_row(self, store, name):
        self.cur.execute(f"""DELETE FROM {store} WHERE date = ? AND name = ?""", (TODAY, name))

    def process_item(self, item, spider):
        name = item['name']
        store = item['store']
        self.crate_table(store)
        self.delete_row(store, name)

        self.cur.execute(f"""INSERT OR IGNORE INTO {store} VALUES(?,?,?,?,?)""",
                         (item['name'],
                          item['category'],
                          item['price'],
                          item['image'],
                          item['date']))
        self.con.commit()
        return item
