
from datetime import datetime
import aiosqlite
from config.config import db_path


class Todo:
    def __init__(self, title: str, description: str, category: str, priority: int, author: str, deadline: datetime, completed: bool = False, date_completed: datetime = None, id: int = None):
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.author = author
        self.deadline = deadline
        self.completed = completed
        self.date_completed = date_completed
        self.id = id


    @staticmethod
    def get_db_path():
        return db_path


    async def create(self):
        async with aiosqlite.connect(self.get_db_path()) as conn:
            formated_deadline = self.deadline.strftime("%d.%m.%y %H:%M")
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO tasks (title, description, category, priority, author, deadline) VALUES (?, ?, ?, ?, ?, ?)",
                    (self.title, self.description, self.category, self.priority, self.author, formated_deadline)
                )
                await conn.commit()
                self.id = cursor.lastrowid


    @staticmethod
    async def get_all():
        async with aiosqlite.connect(Todo.get_db_path()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""
                    SELECT t.id, t.title, t.description, t.category, p.description AS priority_description, t.author, t.completed, t.date_completed, t.deadline
                    FROM tasks t
                    JOIN priorities p ON t.priority = p.id
                """)
                rows = await cursor.fetchall()
        return [Todo.from_db_row(row) for row in rows]


    @staticmethod
    async def get_by_id(todo_id: int):
        async with aiosqlite.connect(Todo.get_db_path()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT * FROM tasks WHERE id = ?", (todo_id,))
                row = await cursor.fetchone()
        if row:
            return Todo.from_db_row(row)
        return None


    async def update(self):
        async with aiosqlite.connect(self.get_db_path()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "UPDATE tasks SET title = ?, description = ?, category = ?, priority = ?, author = ?, completed = ?, date_completed = ?, deadline = ? WHERE id = ?",
                    (self.title, self.description, self.category, self.priority, self.author, self.completed, self.date_completed, self.deadline, self.id)
                )
                await conn.commit()


    async def delete(self):
        async with aiosqlite.connect(self.get_db_path()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("DELETE FROM tasks WHERE id = ?", (self.id,))
                await conn.commit()


    @staticmethod
    def from_db_row(row):
        return Todo(
            id=row[0],
            title=row[1],
            description=row[2],
            category=row[3],
            priority=row[4],
            author=row[5],
            completed=row[6],
            date_completed=row[7],
            deadline=row[8],
        )