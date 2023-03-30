import oracledb
# from .address import Address
import os

class Database:
    def __init__(self, autocommit=True):
        self.__connection = oracledb.connect(user=os.environ['DBUSER'], password=os.environ['DBPWD'],
                                             host="198.168.52.211", port=1521, service_name="pdbora19c.dawsoncollege.qc.ca")
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

    
    # def add_address(self, address):
    #     if isinstance(address,Address):
    #         try:
    #             with self.__get_cursor() as cursor:
    #                 cursor.execute("INSERT INTO FLASK_ADDRESSES VALUES(:name,:street,:city,:province)",name=address.name,street=address.street,city=address.city,province=address.province)
    #         except oracledb.IntegrityError as e:
    #             raise Exception (e)
    #     else:
    #         raise TypeError

    # def get_address(self, name):
    #     with self.__get_cursor() as cursor:
    #         results=cursor.execute("SELECT name,street,city,province FROM FLASK_ADDRESSES WHERE name=:name",name=name)
    #         for row in results:
    #             return Address(row[0],row[1],row[2],row[3])

    # def get_addresses(self):
    #     addresses_list=[]
    #     with self.__get_cursor() as cursor:
    #         results=cursor.execute("SELECT name,street,city,province FROM FLASK_ADDRESSES")
    #         for row in results:
    #             addresses_list.append(Address(row[0],row[1],row[2],row[3]))
    #     return addresses_list

    def close(self):
        '''Closes the connection'''
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None

    def __get_cursor(self):
            for i in range(3):
                try:
                    return self.__connection.cursor()
                except Exception as e:
                    # Might need to reconnect
                    self.__reconnect()

    def __reconnect(self):
        try:
            self.close()
        except oracledb.Error as f:
            pass
        self.__connection = self.__connect()
        
if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')