import psycopg2


# POSTGRESQL
class PostgreSQL():
    def __init__(self,dbname, user, password, host='localhost', port=5432):
        self._host = host
        self._dbname = dbname
        self._user = user
        self._password = password
        self._port = port
        self._parameters = f"dbname={self._dbname} user={self._user} password={self._password} host={self._host} port={self._port}"

    def connect(self):
        self._conn = psycopg2.connect(self._parameters)
        self._cursor = self._conn.cursor()
        return self._conn
 
    def disconnect(self):
        self._conn.close()
    
    def cursor(self):
        return self._cursor

    def version(self):
        self.execute("SELECT version();")
        return self._cursor.fetchone()
    
    def execute(self, schema: str, vars: tuple = ()):
        self._cursor.execute(schema, vars)

    def commit(self):
        return self._conn.commit()
        
    def deleteTable(self,table:str):
        self.execute(f"""DROP TABLE IF EXISTS {table}""")

    def get_all(self,table:str):
        self.execute(f"""SELECT * FROM {table}""")

        return self._cursor.fetchall()
    
    def get_single(self,unique:str,table:str,column:str):
        self.execute(f"SELECT * FROM {table} WHERE {column} LIKE"+"%s", ('%' + unique + '%',))

        result = self._cursor.fetchone()

        if result is not None:
            return unique

        else:
            return None

    def get_first(self, unique: str, table: str, column: str):
        self.execute(f"SELECT * FROM {table} WHERE {column} LIKE %s", ('%' + unique + '%',))
        
        result = self._cursor.fetchone()

        if result is not None:
            return result
        
        else:
            return None


