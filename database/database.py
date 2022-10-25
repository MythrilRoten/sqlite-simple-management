import os
import sqlite3
from pathlib import Path
from types import NoneType
from typing import Sequence


DATABASE_DIR = Path(__file__).parent


class DataBase():
    def __init__(self, path: str) -> None:
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        self.connection.execute("PRAGMA foreign_keys = True")
        self.name_of_tables = [i[0] for i in self.cursor.execute( "SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
        self.info = self.get_info_of_database(self.cursor, self.name_of_tables)

    @staticmethod
    def get_info_of_database(cursor: sqlite3.Cursor, name_of_tables: Sequence[str]) -> dict:
        """Collect and return the info about tables

        Args:
            cursor (sqlite3.Cursor): cursor of connected database
            name_of_tables (Sequence[str]): List of existing tables

        Returns:
            dict: like {'table': {'table_info': [(cid: int, name: str, type: str, notnull: Bool, dflt_value: str, pk: Bool), x1, x2, xn],
                                        'foreign_keys': [(id, seq, table, from, to, on_update, on_delete, match), x1, x2, xn]},
                            'x1': {...},
                            'x2': {...},
                            'xn': {...}}
        """
        data = dict()
        for name_table in name_of_tables:
            temp = dict()
            temp["table_info"] = cursor.execute(f'PRAGMA table_info("{name_table}");').fetchall()
            temp["foreign_keys"] = cursor.execute(f'PRAGMA foreign_key_list("{name_table}");').fetchall()
            data[name_table] = temp
        return data

    def get_content(self, table: str, query: str = None) -> list:
        """Request to connected database for get content of table by using or not

        Args:
            table (str): name of table
            query (str, optional): like "id>5 AND name=='Gregory' OR name==''". Defaults to None.

        Returns:
            list: list of tuples of records of table
        """
        if query is None and query != ' ': # BUG sqlite3.OperationalError: incomplete input after open another bd
            self.content = self.cursor.execute(f'SELECT * FROM {table}').fetchall()
        if query is not None:
            self.content = self.cursor.execute(f'SELECT * FROM {table} WHERE {query}').fetchall()
        return self.content


    def get_last_pk(self, table: str) -> int:
        """Return last pk number of current table 

        Args:
            table (str): name of table

        Returns:
            int: pk
        """
        last_num_pk = self.connection.execute(f"SELECT {self.get_pk(self.info, table)} FROM {table} ORDER BY {self.get_pk(self.info, table)} DESC LIMIT 1").fetchone()
        print(last_num_pk, type(last_num_pk))
        last_num_pk = 0 if last_num_pk is None else last_num_pk[0]
        return last_num_pk
    
    @staticmethod
    def get_pk(full_table_info: dict, table: str) -> str:
        """Return name of PK field in current table

        Args:
            full_table_info (dict): table_info + foreign_key_list or call function get_info_of_database
            table (str): name of table

        Returns:
            str: name of pk field
        """
        for tuple_info in full_table_info[table]['table_info']:
            if tuple_info[-1] == 1: # If pk == True
                name_field = tuple_info[1]
                return name_field


    def delete_record(self, table: str, record: dict) -> bool:
        """Delete record in opened database

        Args:
            table (str): where delete record
            record (dict): record's fields
        Returns:
            bool: status executution
        """

        name_field = self.get_pk(self.info, table)
        query = f"DELETE FROM {table} WHERE {name_field}={record[name_field]}" ## ??????????????????????????????????????????
        try: self.cursor.execute(query)
        except: return False
        self.connection.commit()
        return True
        
    def update_records(self, table: str, records_data: Sequence[dict]) -> None:
        """Update all records in opened database

        Args:
            table (str): where need to update records
            records_data (dict): list which contain all records in table widget
        Returns:
            bool: status executution
        """
        name_field = self.get_pk(self.info, table)
        
        for dict_record in records_data:
            query = f"UPDATE {table} SET "
            keys_record = list(dict_record.keys())
            for key in keys_record:
                if key == name_field:
                    continue
                query += f"""{key} = "{dict_record[key]}", """ if keys_record.index(key) != len(keys_record) - 1 else f"""{key} = "{dict_record[key]}" """
            query += f"WHERE {name_field} = {dict_record[name_field]}"
            
            try: self.cursor.execute(query)
            except: return False
            self.connection.commit()
        return True

    def create_record(self, table: str, record: dict) -> None:
        """Add record in opened database

        Args:
            table (str): where delete record
            record (dict): record's fields
        Returns:
            bool: status executution
        """
        fields_arr = [*record]
        fields_str = ", ".join(fields_arr)
        value_arr = [f"\"{record[field]}\"" for field in fields_arr]
        value_str = ", ".join(value_arr)
        query = f"INSERT INTO {table} ({fields_str}) VALUES ({value_str})"
        try: self.cursor.execute(query)
        except: return False
        self.connection.commit()
        return True

    def __del__(self):
        self.connection.close()

if __name__ == "__main__":
    a = DataBase(os.path.join(DATABASE_DIR, "database.db"))
