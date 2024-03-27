import pickle
import sqlite3
import s_taper.consts
import s_taper.aio


class Taper:
    """
        Main class. Its instances correspond to a single table in the database.
        Use:
        table1 = Taper("table_name", "file.db")
    """

    class _Answer(list):
        def __init__(self, read, columns):
            self._row = {}
            for num, value in enumerate(read):
                self._row[list(columns.keys())[num]] = num

            super().__init__(read)
            self._columns = columns
            if read:
                self._set_attr(read)

        def _set_attr(self, values):
            # Установка атрибутов для каждого столбца на основе переданных значений.
            for n, column_name in enumerate(self._columns):
                super().__setattr__(column_name, values[n])

        def _set_item(self, key, value):
            # Установка значения элемента с использованием ключа.
            if key in ("_row", "_columns"):
                return
            else:
                try:
                    super().__setitem__(self._row[key], value)
                except KeyError:
                    raise KeyError("Такого столбца не существует в таблице, нельзя добавить этот атрибут.")

        def __setattr__(self, key, value):
            try:
                # Переопределение метода для установки атрибута и вызова _set_item.
                if key in ["_row", "_columns"]:
                    return super().__setattr__(key, value)
                elif key not in self._columns:
                    return
                else:
                    return super().__setattr__(key, value)
            finally:
                self._set_item(key, value)

        def __getitem__(self, item):
            if isinstance(item, slice) or isinstance(item, int):
                return super().__getitem__(item)
            return self.__dict__[item]

        def __setitem__(self, key, value):
            try:
                if isinstance(key, slice) or isinstance(key, int):
                    return super().__setitem__(key, value)
                else:
                    # Обращение как к словарю
                    return super().__setitem__(self._row[key], value)
            finally:
                # Обновление атрибутов после изменения
                self._set_attr(self)

    class _ColumnCountError(Exception):
        def __init__(self, *args):
            if args:
                self.message = args[0]
            else:
                self.message = None

    class _TooMuchColumnError(_ColumnCountError):
        def __init__(self):
            super().__init__()

        def __str__(self):
            if self.message:
                return f"Передано значений больше, чем столбцов в таблице. {self.message}"
            else:
                return f"Передано значений больше, чем столбцов в таблице."

    class _TooFewColumnError(_ColumnCountError):
        def __init__(self):
            super().__init__()

        def __str__(self):
            if self.message:
                return f"Передано значений меньше, чем столбцов в таблице. {self.message}"
            else:
                return f"Передано значений меньше, чем столбцов в таблице."

    def __init__(self, table_name: str, file_name: str):
        self._table_name: str = table_name
        self._file_name: str = file_name
        # self.obj = self._Answer()
        self._columns = {}

    def write(self, values: list | tuple = None, table_name: str = None):
        if table_name is None:
            table_name = self._table_name

            a = type(values)

            if len(values) > len(self._columns):
                raise self._TooMuchColumnError
            if len(values) < len(self._columns):
                raise self._TooFewColumnError

        # pickle check
        values = list(values)
        for n, val in enumerate(values):
            if type(val) in (list, tuple, dict):
                values[n] = pickle.dumps(val)
        # /pickle check

        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        questions = "?"
        for x in range(len(values) - 1):
            questions += ", ?"

        cur.execute(f"INSERT or REPLACE into {table_name} VALUES({questions});", values)
        conn.commit()
        conn.close()
        return values

    # Old version read function
    # def read(self, column_name: str, key: str | int):
    #     conn = sqlite3.connect(self._file_name)
    #     cur = conn.cursor()
    #     cur.execute(f'SELECT * from {self._table_name} WHERE {column_name} = ? ', (key,))
    #     result = cur.fetchall()
    #
    #     if len(result) == 1:
    #         result = result[0]
    #
    #         # pickle check
    #         result = list(result)
    #         for n, val in enumerate(result):
    #             if type(val) in (bytes, bytearray):
    #                 result[n] = pickle.loads(val)
    #         # /pickle check
    #
    #     else:
    #         # pickle check
    #         for n, row in enumerate(result):
    #             row = list(row)
    #             for m, val in enumerate(row):
    #                 if type(val) in (bytes, bytearray):
    #                     row[m] = pickle.loads(val)
    #             result[n] = row
    #     return result

    # New version read function

    def read(self, column_name: str, key: str | int):
        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        cur.execute(f'SELECT * from {self._table_name} WHERE {column_name} = ? ', (key,))
        result = cur.fetchall()

        if len(result) == 1:
            result = result[0]

            # pickle check
            result = list(result)
            for n, val in enumerate(result):
                if type(val) in (bytes, bytearray):
                    result[n] = pickle.loads(val)
            # /pickle check

        else:
            # pickle check
            for n, row in enumerate(result):
                row = list(row)
                for m, val in enumerate(row):
                    if type(val) in (bytes, bytearray):
                        row[m] = pickle.loads(val)
                result[n] = row

        a = self._Answer(result, self._columns)
        # index = 0
        # for key in self._columns:
        #     a.__setattr__(key, result[index])
        #     index += 1
        return a

    # function not used anymore
    # def read_obj(self, column_name: str, key: str | int):
    #     conn = sqlite3.connect(self._file_name)
    #     cur = conn.cursor()
    #     cur.execute(f'SELECT * from {self._table_name} WHERE {column_name} = ? ', (key,))
    #     result = cur.fetchone()
    #
    #     # pickle check
    #     result = list(result)
    #     for n, val in enumerate(result):
    #         if type(val) in (bytes, bytearray):
    #             result[n] = pickle.loads(val)
    #     # /pickle check
    #
    #     index = 0
    #     for key in self._columns:
    #         self.obj.__setattr__(key, result[index])
    #         index += 1
    #     return self.obj

    def read_all(self, table_name: str = None):
        if table_name is None:
            table_name = self._table_name
        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        cur.execute(f"SELECT * from {table_name}")
        result = cur.fetchall()

        # pickle check
        if len(result) <= 1000:
            for n, row in enumerate(result):
                row = list(row)
                for m, val in enumerate(row):
                    if type(val) in (bytes, bytearray):
                        row[m] = pickle.loads(val)
                result[n] = row
        # /pickle check

        final = []
        for row in result:
            a = self._Answer(row, self._columns)
            final.append(a)

        conn.close()
        return final

    def delete_row(self, column_name: str = None, key: str | int = None, all_rows: bool = None):
        """
        Func uses to deleting rows from the table.

        :param column_name: Column name to delete the row in which the key is found in the current column
        :param key: Key which looks in column
        :param all_rows: If True func delete all rows in the table
        """

        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        if all_rows:
            cur.execute(f'DELETE FROM {self._table_name}')
        else:
            cur.execute(f'DELETE FROM {self._table_name} WHERE {column_name} = ?', (key,))
        conn.commit()
        conn.close()

    def create_table(self, table: dict, table_name: str = None):
        """
        table - {
                    "table1": "type",
                    and so on
                }

        """
        if table_name is None:
            table_name = self._table_name
        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        task = f"CREATE TABLE IF NOT EXISTS {table_name}("
        n = 0
        for key in table:
            n += 1
            task += f"{key} {table[key]}"
            if n != len(table):
                task += ", "
            else:
                task += ");"
        cur.execute(task)
        conn.commit()
        conn.close()

        temp = Taper(table_name, self._file_name)
        temp._columns = table
        # temp.__create_obj__()
        return temp

    def drop_table(self, table_name: str = None):
        if not table_name:
            table_name = self._table_name
        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        cur.execute(f"DROP TABLE {table_name}")
        conn.commit()
        conn.close()

    # def __create_obj__(self):
    #     self.obj = self._Answer([], self._columns)
    #     for key in self._columns:
    #         self.obj.__setattr__(key, None)

    def execute(self, sql: str, fetchall=True):
        conn = sqlite3.connect(self._file_name)
        cur = conn.cursor()
        result = cur.execute(sql)
        conn.commit()
        if fetchall:
            result = result.fetchall()
        else:
            result = result.fetchone()
        conn.close()
        return result
