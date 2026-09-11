"""Database Module - SQLite operations for Task Tracker"""

import sqlite3
from typing import List, Dict, Optional


class TaskDatabase:
    """Manages database operations for tasks."""
    
    def __init__(self, db_name: str = "tasks.db"):
        """Initialize database connection and create table."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)
        self.conn.commit()
    
    def add_task(self, name: str, status: str) -> bool:
        """Add a new task."""
        try:
            self.cursor.execute("INSERT INTO tasks (name, status) VALUES (?, ?)", (name, status))
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False
    
    def get_all_tasks(self) -> List[Dict]:
        """Get all tasks."""
        try:
            self.cursor.execute("SELECT id, name, status FROM tasks ORDER BY id")
            return [{"id": r[0], "name": r[1], "status": r[2]} for r in self.cursor.fetchall()]
        except sqlite3.Error:
            return []
    
    def get_task_by_id(self, task_id: int) -> Optional[Dict]:
        """Get task by ID."""
        try:
            self.cursor.execute("SELECT id, name, status FROM tasks WHERE id = ?", (task_id,))
            r = self.cursor.fetchone()
            return {"id": r[0], "name": r[1], "status": r[2]} if r else None
        except sqlite3.Error:
            return None
    
    def update_task(self, task_id: int, name: str, status: str) -> bool:
        """Update existing task."""
        try:
            self.cursor.execute("UPDATE tasks SET name = ?, status = ? WHERE id = ?", (name, status, task_id))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error:
            return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete task."""
        try:
            self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error:
            return False
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
