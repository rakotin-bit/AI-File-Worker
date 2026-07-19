import sqlite3
from pathlib import Path


class ModelStorage:
    def __init__(self, db_path="models.db"):
        self.db_path = Path(db_path)
        self._init_db()
        self._migrate()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS model_stats (
                    model TEXT PRIMARY KEY
                )
                """
            )

            conn.commit()

    def _migrate(self):
        required_columns = {
            "success_count": "INTEGER DEFAULT 0",
            "failure_count": "INTEGER DEFAULT 0",
            "total_response_time": "REAL DEFAULT 0",
            "avg_response_time": "REAL DEFAULT 0",
        }

        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "PRAGMA table_info(model_stats)"
            )

            existing = {
                row[1]
                for row in cursor.fetchall()
            }

            for column, definition in required_columns.items():
                if column not in existing:
                    cursor.execute(
                        f"""
                        ALTER TABLE model_stats
                        ADD COLUMN {column} {definition}
                        """
                    )

            conn.commit()

    def get(self, model):
        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    model,
                    success_count,
                    failure_count,
                    total_response_time,
                    avg_response_time
                FROM model_stats
                WHERE model = ?
                """,
                (model,),
            )

            row = cursor.fetchone()

            if not row:
                return {
                    "model": model,
                    "success_count": 0,
                    "failure_count": 0,
                    "total_response_time": 0,
                    "avg_response_time": 0,
                }

            return {
                "model": row[0],
                "success_count": row[1],
                "failure_count": row[2],
                "total_response_time": row[3],
                "avg_response_time": row[4],
            }

    def create_if_missing(self, model):
        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT OR IGNORE INTO model_stats
                (
                    model,
                    success_count,
                    failure_count,
                    total_response_time,
                    avg_response_time
                )
                VALUES (?,0,0,0,0)
                """,
                (model,),
            )

            conn.commit()

    def update(self, model, data):
        self.create_if_missing(model)

        fields = []
        values = []

        for key, value in data.items():
            fields.append(f"{key}=?")
            values.append(value)

        values.append(model)

        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                f"""
                UPDATE model_stats
                SET {", ".join(fields)}
                WHERE model=?
                """,
                values,
            )

            conn.commit()