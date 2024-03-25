import sqlite3
from typing import List
import datetime
from model import Todo

connect_db = sqlite3.connect("todo.db")
cn_db = connect_db.cursor()

def create_table():
   cn_db.execute("""CREATE TABLE IF NOT EXISTS to_do (
           task text,
           category text,
           date_added text,
           date_completed text,
           status integer,
           position integer
           )""")

create_table()

def insert_task(todo: Todo):
  cn_db.execute('select count(*) FROM to_do')
  count = cn_db.fetchone()[0]
  todo.position = count if count else 0
  with connect_db:
    cn_db.execute('INSERT INTO to_do (task, category, date_added, date_completed, status, position) VALUES (:task, :category, :date_added, :date_completed, :status, :position)',
                  {'task': todo.task, 'category': todo.category, 'date_added': todo.date_added,
                   'date_completed': todo.date_completed, 'status': todo.status, 'position': todo.position })


def get_all_task() -> List[Todo]:
   cn_db.execute('select * from to_do')
   results = cn_db.fetchall()
   to_do =[]
   for result in results:
       to_do.append(Todo(*result))
   return to_do

def remove_task(position):
   cn_db.execute('select count(*) from to_do')
   count = cn_db.fetchone()[0]

   with connect_db:
       cn_db.execute("DELETE from to_do WHERE position=:position", {"position": position})
       for posit in range (position+1, count):
           change_position(posit, posit-1, False)

def change_position(old_position: int, new_position: int, commit=True):
   cn_db.execute('UPDATE to_do SET position = :position_new WHERE position = :position_old',
                   {'position_old': old_position, 'position_new': new_position })
   if commit:
       connect_db.commit()

def update_task(position: int, task: str, category:str):
   with connect_db:
       if task is not None and category is not None:
           cn_db.execute('UPDATE to_do SET task = :task, category = :category WHERE position = :position',
                     {'position': position, 'task': task, 'category': category})
       elif task is not None:
           cn_db.execute('UPDATE to_do SET task = :task WHERE position = :position',
                     {'position': position, 'task': task})
       elif category is not None:
           cn_db.execute('UPDATE to_do SET category = :category WHERE position = :position',
                     {'position': position, 'category': category})

def done_task(position: int):
   with connect_db:
       cn_db.execute('UPDATE to_do SET status = 2, date_completed = :date_completed WHERE position = :position',
                      {'position': position, 'date_completed': datetime.datetime.now().isoformat()})
