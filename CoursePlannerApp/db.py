import os
from .term import Term
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
    #COURSE
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
    
    #DOMAIN
    def add_domain(self, domain): 
        '''Add a domain to the DB for the given Domain object'''
        with self.__connection.cursor() as cursor:
            if (not isinstance(domain, Domain)):
                raise ValueError
            cursor.execute("CALL add_domain(:domainToAdd)",  domainToAdd = domain)            
            if not cursor.rowcount:
                raise oracledb.Error
            
    def update_domain(self, domain): 
        '''Update a domain for the given Domain object'''
        with self.__connection.cursor() as cursor:
            if (not isinstance(domain, Domain)):
                raise ValueError
            cursor.execute("CALL update_domain(:domainToUpdate)", domainToUpdate = domain)            
            if not cursor.rowcount:
                raise oracledb.Error
            
    def delete_domain(self, domain): 
        '''Delete a domain in DB for the given Domain object id'''
        with self.__connection.cursor() as cursor:
            if (not isinstance(domain, Domain)):
                raise ValueError
            cursor.execute("CALL delete_domain(:domainId)", domainId = domain.id)            
            if not cursor.rowcount:
                raise oracledb.Error
            
    #TERM
    def add_term(self, term): 
        '''Add a term to the DB for the given Term object'''
        with self.__connection.cursor() as cursor:
            if (not isinstance(term, Term)):
                raise ValueError
            cursor.execute("CALL add_term(:termToAdd)", termToAdd = term)            
            if not cursor.rowcount:
                raise oracledb.Error
    
    def update_term(self, term): 
        '''Update a term for the given Term object'''
        with self.__connection.cursor() as cursor:
            if (not isinstance(term, Term)):
                raise ValueError
            cursor.execute("CALL update_term(:termToUpdate)", termToUpdate = term)            
            if not cursor.rowcount:
                raise oracledb.Error
            
    def delete_term(self, term): 
        '''Delete a term in DB for the given Term object id'''
        with self.__connection.cursor() as cursor:
            if (not isinstance(term, Term)):
                raise ValueError
            cursor.execute("CALL delete_term(:termId)", termId = term.id)            
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
