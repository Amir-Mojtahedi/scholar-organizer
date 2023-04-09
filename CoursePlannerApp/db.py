import os
from .competency import Competency
from .element import Element
from .term import Term
from .domain import Domain
from .course import Course
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
    
    #COMPETENCY
    def get_competencies(self):
        '''Returns all Competency objects in a list'''
        with self.__connection.cursor() as cursor:
            newListCompetency = []
            results = cursor.execute("SELECT * FROM COMPETENCIES")
            for result in results:
                newCompetency = Competency(id = result[0], name = result[1], achievement= result[2], type= result[3])
                newListCompetency.append(newCompetency)
            return newListCompetency
        
    def add_competency(self, competency): 
        '''Add a competency to the DB for the given Competency object'''
        with self.__connection.cursor() as cursor:
            if (not isinstance(competency, Competency)):
                raise ValueError
            cursor.execute("CALL add_competency(:competencyToAdd)", competencyToAdd = competency)            
            if not cursor.rowcount:
                raise oracledb.Error
            
    def update_competency(self, competency): 
        '''Update a competency for the given Competency object'''
        with self.__connection.cursor() as cursor:
            if (not isinstance(competency, Competency)):
                raise ValueError
            cursor.execute("CALL update_competency(:competencyId, :competency, :competency_achievement)", competencyId = competency.id, competency = competency.name, competency_achievement = competency.achievement, competency_type = competency.type)            
            if not cursor.rowcount:
                raise oracledb.Error
    
    def delete_competency(self, competency): 
        '''Delete a competency in DB for the given COmpetency object id'''
        with self.__connection.cursor() as cursor:
            if (not isinstance(competency, Competency)):
                raise ValueError
            cursor.execute(" CALL delete_competency(:competencyId)", competencyId = competency.id)            
            if not cursor.rowcount:
                raise oracledb.Error
    
    #ELEMENT 
    def get_elements(self):
        '''Returns all Element objects in a list'''
        with self.__connection.cursor() as cursor:
            newListElement = []
            results = cursor.execute("SELECT  * FROM COMPETENCIES")
            for result in results:
                newElement = Element(order= result[0], name= result[1], criteria= result[2], hours= result[3], competency= result[4])
                newListElement.append(newElement)
            return newListElement
        
    def add_element(self, element): 
        '''Add an element to the DB for the given Element object'''
        with self.__connection.cursor() as cursor:
            if (not isinstance(element, Element)):
                raise ValueError
            cursor.execute("CALL add_element(:elementToAdd)", elementToAdd = element)            
            if not cursor.rowcount:
                raise oracledb.Error
            
    def delete_element(self, element): 
            '''Delete a element for the given Element object'''
            with self.__connection.cursor() as cursor:
                if (not isinstance(element, Element)):
                    raise ValueError
                cursor.execute(" CALL delete_element(:elementId)", elementId = element.id)                  
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
    def add_user(self, user):
        if not isinstance(user, User):
            raise TypeError("You must provide a user object to this function.")
        with self.__get_cursor() as cursor:
            cursor.execute('insert into courseapp_users (email, password, name) values (:email, :password, :name)',
                           email = user.email,
                           password = user.password,
                           name = user.name)
    def get_user(self, email):
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        with self.__get_cursor() as cursor:
            results = cursor.execute('select id, email, password, name from courseapp_users where email=:email', email=email)
            for row in results:
                user = User(id=row[0], email=row[1],
                    password=row[2], name=row[3])
                return user
        return None
    
    def get_user_by_id(self, id):
        if not isinstance(id, int):
            raise TypeError("Id must be an integer")
        with self.__get_cursor() as cursor:
            results = cursor.execute('select id, email, password, name from courseapp_users where id=:id', id=id)
            for row in results:
                user = User(id=row[0], email=row[1],
                    password=row[2], name=row[3])
                return user
        return None

if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')


