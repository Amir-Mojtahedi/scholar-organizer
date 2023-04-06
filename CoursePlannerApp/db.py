import os

from .domain import Domain
from .course import Course
import oracledb

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

    def add_course(self, course): 
        '''Add a course to the DB for the given Course object'''
        with self.__connection.cursor() as cursor:
            if (not isinstance(course, Course)):
                raise ValueError
            cursor.execute("CALL add_course(:courseToAdd)",  courseToAdd = course)            
            if not cursor.rowcount:
                raise oracledb.Error
    
    def update_course(self, course): 
        '''Update a coursefor the given Course object'''
        with self.__connection.cursor() as cursor:
            if (not isinstance(course, Course)):
                raise ValueError
            cursor.execute("CALL update_course(:courseId, :title, :theory, :lab, :work, :description, :domainId, :termId)",  courseId = course.id, title = course.name, theory = course.theory_hours, lab = course.lab_hours, work = course.work_hours, description = course.description, domainId = course.domain.id, termId = course.term.id)            
            if not cursor.rowcount:
                raise oracledb.Error
    
    def delete_course(self, course): 
        '''Delete a course in DB for the given Course object id'''
        with self.__connection.cursor() as cursor:
            if (not isinstance(course, Course)):
                raise ValueError
            cursor.execute("CALL delete_course(:courseId)",  courseId = course.id)            
            if not cursor.rowcount:
                raise oracledb.Error
    
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

if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')
