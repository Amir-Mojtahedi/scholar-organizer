import os
import oracledb


from CoursePlannerApp.user import User

class Database:
    def __init__(self, autocommit=True):
        self.__connection = self.__connect()
        self.__connection.autocommit = autocommit

    def run_file(self, file_path):
        statement_parts = []
        with self.__connection.cursor() as cursor:
            with open(file_path, 'r') as f:
                for line in f:
                    statement_parts.append(line)
                    if line.strip('\n').strip('\n\r').strip().endswith(';'):
                        statement = "".join(
                            statement_parts).strip().rstrip(';')
                        if statement:
                            try:
                                cursor.execute(statement)
                            except Exception as e:
                                print(e)
                        statement_parts = []

    def close(self):
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None

    def __get_cursor(self):
        for _ in range(3):
            try:
                return self.__connection.cursor()
            except Exception as _:
                # Might need to reconnect
                self.__reconnect()

    def __reconnect(self):
        try:
            self.close()
        except oracledb.Error as _:
            pass
        self.__connection = self.__connect()

    def __connect(self):
        return oracledb.connect(user=os.environ['DBUSER'], password=os.environ['DBPWD'],
                                host="198.168.52.211", port=1521, service_name="pdbora19c.dawsoncollege.qc.ca")
    def add_user(self, user):
        if not isinstance(user, User):
            raise TypeError("You must provide a user object to this function.")
        with self.__conn.cursor() as cursor:
            cursor.execute('insert into courseapp_users (email, password, name) values (:email, :password, :name)',
                           email = user.email,
                           password = user.password,
                           name = user.name)

if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')


