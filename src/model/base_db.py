import os
from sqlite3 import Connection
from typing import Any, Literal


DataType = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]

class DbManager(Connection):
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        path = os.path.dirname(__file__)
        super().__init__(f"{path}/../../.database/{self.db_name}")
        self._cursor = super().cursor()

    def _create_placeholder(self, n: int) -> str:
        return ", ".join(["?" for _ in range(n)])
    
    def data_checker(self, table_name: str, condition: str) -> bool:
        result = self.select(table_name, ["*"], condition)
        if not result:
            return False
        return True

    def create_table(
        self,
        table_name: str,
        **kwargs: str
    ) -> None:
        in_primary = False
        columns = ""
        for key, value in kwargs.items():
            if "PRIMARY" in value:
                in_primary = True
            columns += f"{key} {value}, "
        if not in_primary:
            raise ValueError(f"Missing primary key")

        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns[:-2]})"
        self._cursor.execute(query)
        self.commit()

    def drop_table(self, table_name: str) -> None:
        query = f"DROP TABLE IF EXISTS {table_name}"
        self._cursor.execute(query)
        self.commit()

    def insert(self, table_name: str, **kwargs: Any) -> None:
        columns = ", ".join(kwargs.keys())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({self._create_placeholder(len(kwargs))})"
        self._cursor.execute(
            query,
            tuple(kwargs.values()),
        )
        self.commit()

    def select(
        self,
        table_name: str,
        columns: list[str],
        condition: str | None = None,
    ) -> list[dict[str, Any]]:
        query = f"SELECT {', '.join(columns)} FROM {table_name}"
        if condition is not None:
            query += f" WHERE {condition}"
        cur = self._cursor.execute(query)
        result = cur.fetchall()
        
        res = []
        for r in result:
            if isinstance(r, tuple):
                res.append(dict(zip(columns, r)))
        return res

    def update(self, table_name: str, condition: str, **kwargs: Any) -> None:
        set_values = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        query = f"UPDATE {table_name} SET {set_values} WHERE {condition}"
        vals = [val for val in kwargs.values()]
        self._cursor.execute(query, vals)
        self.commit()

    def delete(self, table_name: str, condition: str) -> None:
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self._cursor.execute(query)
        self.commit()


if __name__ == "__main__":
    db = DbManager("example.db")
    print(db.select("users", ["name", "chip"]))
