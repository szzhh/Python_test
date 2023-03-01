import sqlite3

conn = sqlite3.connect('test.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS books
            (id int primary key,
            sort int,
            name text,
            price real)''')

c.execute('''INSERT INTO books VALUES
    (1,1,'computer science',39.1)''')

books = [
    (2,2,'computer science',68),
    (3,2,'python science',89),
    (4,3,'stm32 science',78),
]

c.executemany('INSERT INTO books VALUES(?,?,?,?)',books)

conn.commit()

conn.close()
print('done')
