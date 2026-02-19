from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Session

class Base(DeclarativeBase):
    pass

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key = True, autoincrement = True)
    text = Column(String)
    done = Column(Boolean, default = False)

    def add_todo(text):
        with Session(engine) as session:
            todo = Todo(text = text, done = False)
            session.add(todo)
            session.commit()

    def mark_done(text):
        with Session(engine) as session:
            todo = session.query(Todo).filter(Todo.text == text).first()
            todo.done = True
            session.commit()

    def delete_todo(text):
        with Session(engine) as session:
            todo = session.query(Todo).filter(Todo.text == text).first()
            session.delete(todo)
            session.commit()

    def __repr__(self):
        return f"Todo(id = {self.id}, text = {self.text}, done = {self.done})"
  
engine = create_engine("sqlite:///todo.db")
Base.metadata.create_all(engine)
with Session(engine) as session:
    todo1 = str(input("Введите первую заметку: "))
    todo2 = str(input("Введите вторую заметку: "))
    todo3 = str(input("Введите третью заметку: "))

    Todo.add_todo(todo1)
    Todo.add_todo(todo2)
    Todo.add_todo(todo3)

    todos = session.query(Todo).all()
    for todo in todos:
        print(todo)

    Todo.mark_done(todo1)

    session.expire_all()
    todos = session.query(Todo).all()
    for todo in todos:
        print(todo)

    Todo.delete_todo(todo3)

    session.expire_all()
    todos = session.query(Todo).all()
    for todo in todos:
        print(todo)