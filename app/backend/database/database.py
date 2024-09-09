
import sqlite3

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path


    def get_connection(self):
        return sqlite3.connect(self.db_path)


    def create_table(self):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            description TEXT NOT NULL,
                            category TEXT NOT NULL,
                            priority INTEGER DEFAULT 1,
                            author TEXT NOT NULL,
                            completed BOOLEAN DEFAULT FALSE,
                            date_completed TIMESTAMP DEFAULT NULL,
                            deadline TIMESTAMP NOT NULL,
                            FOREIGN KEY (priority) REFERENCES priorities (id)
                        )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS priorities (
                                id INTEGER PRIMARY KEY,
                                description TEXT NOT NULL
                            )''')

            cursor.executemany('''INSERT OR IGNORE INTO priorities (id, description) VALUES (?, ?)''', [
                (1, 'Низкий'),
                (2, 'Средний'),
                (3, 'Высокий'),
                (4, 'Очень высокий')
            ])

            conn.commit()
        finally:
            conn.close()