import sqlite3
import pandas as pd
from datetime import datetime

class TradeDatabase:
    def __init__(self, db_path="data/trading_history.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME,
                    code TEXT,
                    type TEXT,
                    qty INTEGER,
                    price INTEGER,
                    profit REAL
                )
            """)
            conn.commit()

    def log_trade(self, code, type, qty, price, profit=0):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO trades (timestamp, code, type, qty, price, profit)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (datetime.now(), code, type, qty, price, profit))
            conn.commit()

    def get_all_trades(self):
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql("SELECT * FROM trades", conn)
