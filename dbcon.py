from config import host, database, user, password
import psycopg2


class PgConection:

    def __init__(self, host=host, database=database, user=user, password=password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.conectar()

    def conectar(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Conexão ao PostgreSQL bem-sucedida!")

        except (Exception, psycopg2.Error) as error:
            print("Erro ao conectar ao PostgreSQL:", error)

    def desconectar(self):
        if self.connection:
            self.connection.close()
            print("Conexão fechada com sucesso!")

    def executar_query(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            resultado = cursor.fetchall()
            if not resultado:
                return False
            else:
                return resultado
            
