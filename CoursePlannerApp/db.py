import os

import oracledb

from CoursePlannerApp.objects.competency import Competency
from CoursePlannerApp.objects.course import Course
from CoursePlannerApp.objects.domain import Domain
from CoursePlannerApp.objects.element import Element
from CoursePlannerApp.objects.group import Group
from CoursePlannerApp.objects.term import Term
from CoursePlannerApp.objects.user import User


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

    # COURSE
    def get_courses(self):
        '''Returns all Courses objects in a list'''
        with self.__get_cursor() as cursor:
            newListCourse = []
            results = cursor.execute(
                "SELECT course_id, course_title, theory_hours, lab_hours, work_hours, description, domain_id, term_id FROM COURSES")
            for result in results:
                newCourse = Course(id=result[0], name=result[1], theory_hours=result[2], lab_hours=result[3],
                                   work_hours=result[4], description=result[5], domainId=result[6], termId=result[7])
                newListCourse.append(newCourse)
            return newListCourse

    def get_course(self, courseId):
        '''Returns a specific course'''
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT course_id, course_title, theory_hours, lab_hours, work_hours, description, domain_id, term_id FROM COURSES WHERE course_id=:courseId",
                courseId=courseId)
            for result in results:
                course = Course(id=result[0], name=result[1], theory_hours=result[2], lab_hours=result[3],
                                work_hours=result[4], description=result[5], domainId=result[6], termId=result[7])
                return course
            
            return None

    def get_course_competencies(self, course_id):
        '''Returns a specific competencies for a course'''
        with self.__get_cursor() as cursor:
            competenciesList = []
            results = cursor.execute(
                "SELECT UNIQUE competency_id,competency,competency_achievement,competency_type FROM COURSES JOIN COURSES_ELEMENTS USING(course_id) JOIN ELEMENTS USING(element_id) JOIN COMPETENCIES USING(competency_id) WHERE course_id=:course_id",
                course_id=course_id)
            for result in results:
                competency = Competency(id=result[0], name=result[1], achievement=result[2], type=result[3])
                competenciesList.append(competency)
            return competenciesList

    def get_competency_elements(self, competency_id):
        '''Returns a specific elements for a competency'''
        with self.__get_cursor() as cursor:
            elementsList = []
            results = cursor.execute(
                "SELECT UNIQUE element_id,element_order,element,element_criteria,competency_id FROM elements JOIN competencies USING(competency_id) WHERE competency_id=:competency_id",
                competency_id=competency_id)
            for result in results:
                element = Element(id=result[0], order=result[1], name=result[2], criteria=result[3],
                                  competencyId=result[4])
                elementsList.append(element)
            return elementsList


    def add_course(self, course):
        '''Add a course to the DB for the given Course object'''
        with self.__get_cursor() as cursor:
            # Check Type
            if not isinstance(course, Course):
                raise ValueError("Should be a Course obj")

            # Check if course doesn't already exist
            results = cursor.execute(
                "SELECT course_id, course_title, theory_hours, lab_hours, work_hours, description, domain_id, term_id FROM COURSES where course_id = :courseId or course_title = :courseName",
                courseId=course.id, courseName=course.name)
            nCourse = [result for result in results if (result[0] == course.id or result[1] == course.name)]
            if not (nCourse == []):
                raise ValueError("Course already exist")

            # Check if domain exists
            results = cursor.execute(
                "SELECT domain_id, domain, domain_description FROM DOMAINS where domain_id = :domainId",
                domainId=course.domainId)
            domain = [result for result in results if result[0] == course.domainId]
            if domain is None:
                raise ValueError("Domain doesn't exist. Create a domain first")

            # Check if term exists
            results = cursor.execute("SELECT term_id FROM TERMS where term_id = :termId", termId=course.termId)
            term = [result for result in results if result[0] == course.termId]
            if term is None:
                raise ValueError("Term doesn't exist. Create a term first")

            # Insert data
            cursor.execute(
                "INSERT INTO COURSES (course_id, course_title, theory_hours, lab_hours, work_hours, description, domain_id, term_id) VALUES (:courseId, :title, :theory, :lab, :work, :description, :domainId, :termId)",
                courseId=course.id, title=course.name, theory=course.theory_hours, lab=course.lab_hours,
                work=course.work_hours, description=course.description, domainId=course.domainId, termId=course.termId)
            if not cursor.rowcount:
                raise oracledb.Error

    def update_course(self, course):
        '''Update a coursefor the given Course object'''
        with self.__get_cursor() as cursor:
            if not isinstance(course, Course):
                raise ValueError
            cursor.execute(
                "UPDATE COURSES SET course_title = :title, theory_hours = :theory, lab_hours = :lab, work_hours = :work, description = :description, domain_id = :domainId, term_id = :termId WHERE course_id = :courseId",
                courseId=course.id, title=course.name, theory=course.theory_hours, lab=course.lab_hours,
                work=course.work_hours, description=course.description, domainId=course.domainId, termId=course.termId)
            if not cursor.rowcount:
                raise oracledb.Error

    def delete_course(self, course_id):
        '''Delete a course in DB for the given Course object id'''
        with self.__get_cursor() as cursor:
            cursor.execute("DELETE FROM COURSES WHERE course_id = :courseId", courseId=course_id)

    # DOMAIN
    def get_domains(self):
        '''Returns all Domains objects in a list'''
        with self.__get_cursor() as cursor:
            newListDomain = []
            results = cursor.execute("SELECT domain_id, domain, domain_description FROM DOMAINS")
            for result in results:
                newDomain = Domain(id=result[0], name=result[1], description=result[2])
                newListDomain.append(newDomain)
            return newListDomain

    def get_domains_api(self, page_num=1, page_size=50):
        domains = []
        offset = (page_num-1)*page_size
        prev_page = None
        next_page = None
        with self.__get_cursor() as cursor:
            results = cursor.execute('select count(*) from domains')
            count = results.fetchone()[0]
            results = cursor.execute('select domain_id, domain, domain_description from domains order by domain_id offset :offset rows fetch next :page_size rows only', offset=offset, page_size=page_size)
            for row in results:
                domain = Domain(id=row[0], name=row[1],
                                description=row[2])
                domains.append(domain)
        if page_num > 1:
            prev_page = page_num - 1
        if len(domains) > 0 and (count/page_size) > page_num:
            next_page = page_num + 1
        return domains, prev_page, next_page, count

    def get_terms_api(self, page_num=1, page_size=50):
        terms = []
        offset = (page_num-1)*page_size
        prev_page = None
        next_page = None
        with self.__get_cursor() as cursor:
            results = cursor.execute('select count(*) from terms')
            count = results.fetchone()[0]
            results = cursor.execute('select term_id, TERM_NAME from terms order by term_id offset :offset rows fetch '
                                     'next :page_size rows only', offset=offset, page_size=page_size)
            for row in results:
                term = Term(id=row[0], name=row[1])
                terms.append(term)
        if page_num > 1:
            prev_page = page_num - 1
        if len(terms) > 0 and (count/page_size) > page_num:
            next_page = page_num + 1
        return terms, prev_page, next_page, count

    def get_courses_api(self, page_num=1, page_size=50):
        courses = []
        offset = (page_num-1)*page_size
        prev_page = None
        next_page = None
        with self.__get_cursor() as cursor:
            results = cursor.execute('select count(*) from courses')
            count = results.fetchone()[0]
            results = cursor.execute('select course_id, course_title, theory_hours, lab_hours, work_hours, '
                                     'description, domain_id, term_id from courses order by course_id offset :offset '
                                     'rows fetch next :page_size rows only', offset=offset, page_size=page_size)
            for row in results:
                course = Course(id=row[0], name=row[1], theory_hours=row[2], lab_hours=row[3], work_hours=row[4],
                                description=row[5], domainId=row[6], termId=row[7])
                courses.append(course)
        if page_num > 1:
            prev_page = page_num - 1
        if len(courses) > 0 and (count/page_size) > page_num:
            next_page = page_num + 1
        return courses, prev_page, next_page, count

    def get_competencies_api(self, page_num=1, page_size=50):
        competencies = []
        offset = (page_num-1)*page_size
        prev_page = None
        next_page = None
        with self.__get_cursor() as cursor:
            results = cursor.execute('select count(*) from competencies')
            count = results.fetchone()[0]
            #id, name, achievement, type
            results = cursor.execute('select competency_id, COMPETENCY, COMPETENCY_ACHIEVEMENT, COMPETENCY_TYPE from competencies order by competency_id offset :offset rows fetch next :page_size rows only', offset=offset, page_size=page_size)
            for row in results:
                competency = Competency(id=row[0], name=row[1], achievement=row[2], type=row[3])
                competencies.append(competency)
        if page_num > 1:
            prev_page = page_num - 1
        if len(competencies) > 0 and (count/page_size) > page_num:
            next_page = page_num + 1
        return competencies, prev_page, next_page, count

    def get_elements_api(self, page_num=1, page_size=10):
        elements = []
        offset = (page_num-1)*page_size
        prev_page = None
        next_page = None
        with self.__get_cursor() as cursor:
            results = cursor.execute('select count(*) from elements')
            count = results.fetchone()[0]
            #id, order, name, criteria, competencyId
            results = cursor.execute('select element_id, ELEMENT_ORDER, ELEMENT, ELEMENT_CRITERIA, COMPETENCY_ID from elements order by element_id offset :offset rows fetch next :page_size rows only', offset=offset, page_size=page_size)
            for row in results:
                element = Element(id=row[0], order=row[1], name=row[2], criteria=row[3], competencyId=row[4])
                elements.append(element)
        if page_num > 1:
            prev_page = page_num - 1
        if len(elements) > 0 and (count/page_size) > page_num:
            next_page = page_num + 1
        return elements, prev_page, next_page, count

    def get_domain(self, domainId):
        '''Returns a specific domain'''
        with self.__get_cursor() as cursor:
            domain = None

            results = cursor.execute(
                "SELECT domain_id, domain, domain_description FROM DOMAINS WHERE domain_id = :domainId",
                domainId=domainId)
            for result in results:
                domain = Domain(id=result[0], name=result[1], description=result[2])
            return domain

    def get_courses_in_domain(self, domainId):
        '''Returns a specific domain'''
        with self.__get_cursor() as cursor:
            impactedCourse = []
            results = cursor.execute(
                "SELECT course_id, course_title, theory_hours, lab_hours, work_hours, description, domain_id, term_id FROM COURSES WHERE domain_id = :domainId",
                domainId=domainId)
            for result in results:
                newCourse = Course(id=result[0], name=result[1], theory_hours=result[2], lab_hours=result[3],
                                   work_hours=result[4], description=result[5], domainId=result[6], termId=result[7])
                impactedCourse.append(newCourse)
            return impactedCourse

    def add_domain(self, domain):
        '''Add a domain to the DB for the given Domain object'''
        with self.__get_cursor() as cursor:
            if not isinstance(domain, Domain):
                raise ValueError("Should be domain obj")

            # Check if domain doesn't already exist
            results = cursor.execute("SELECT domain FROM DOMAINS where domain_id = :domainId", domainId=domain.id)
            nDomain = [result for result in results if result[0] == domain.id]
            if not (nDomain == []):
                raise ValueError("Domain already exist")

            # Insert data
            cursor.execute(
                "INSERT INTO DOMAINS (domain_id, domain, domain_description) VALUES(:domainId, :domainName, :domainDescription)",
                domainId=domain.id, domainName=domain.name, domainDescription=domain.description)
            if not cursor.rowcount:
                raise oracledb.Error

    def update_domain(self, domain):
        '''Update a domain for the given Domain object'''
        with self.__get_cursor() as cursor:
            if not isinstance(domain, Domain):
                raise ValueError
            cursor.execute(
                "UPDATE domains SET domain = :domainName, domain_description = :domainDescription WHERE domain_id = :domainId",
                domainName=domain.name, domainDescription=domain.description, domainId=domain.id)
            if not cursor.rowcount:
                raise oracledb.Error

    def delete_domain(self, domainId):
        '''Delete a domain in DB for the given Domain object id'''
        with self.__get_cursor() as cursor:
            coursesToDelete = []
            results = cursor.execute("SELECT course_id from Courses WHERE domain_id= :domainId",domainId=domainId)
            for result in results:
                courseId = result[0]
                coursesToDelete.append(courseId)
            for courseId in coursesToDelete:
                cursor.execute("DELETE FROM courses_elements WHERE course_id = :courseId" , courseId=courseId)
            
            cursor.execute("DELETE FROM courses WHERE domain_id= :domainId" , domainId=domainId)

            cursor.execute("DELETE FROM domains WHERE domain_id = :domainId", domainId=domainId)

    # TERM
    def get_terms(self):
        '''Returns all Term objects in a list'''
        with self.__get_cursor() as cursor:
            newListTerm = []
            results = cursor.execute("SELECT term_id, term_name  FROM TERMS")
            for result in results:
                newTerm = Term(id=result[0], name=result[1])
                newListTerm.append(newTerm)
            return newListTerm

    def get_term(self, termId):
        '''Returns a specific term'''
        with self.__get_cursor() as cursor:
            results = cursor.execute("SELECT term_id, term_name FROM TERMS WHERE term_id=:termId", termId=termId)
            for result in results:
                foundTerm = Term(id=result[0], name=result[1])
                return foundTerm
            return None

    def get_courses_in_term(self, termId):
        '''Returns a specific domain'''
        with self.__get_cursor() as cursor:
            impactedCourse = []
            results = cursor.execute(
                "SELECT course_id, course_title, theory_hours, lab_hours, work_hours, description, domain_id, term_id FROM COURSES WHERE term_id = :termId",
                termId=termId)
            for result in results:
                newCourse = Course(id=result[0], name=result[1], theory_hours=result[2], lab_hours=result[3],
                                   work_hours=result[4], description=result[5], domainId=result[6], termId=result[7])
                impactedCourse.append(newCourse)
            return impactedCourse

    def add_term(self, term):
        '''Add a term to the DB for the given Term object'''
        with self.__get_cursor() as cursor:
            if not isinstance(term, Term):
                raise ValueError("Should be a Term obj")

            # Check if term doesn't already exist
            results = cursor.execute("SELECT * FROM TERMS where term_id = :termId", termId=term.id)
            nTerm = [result for result in results if (result[0] == term.id)]
            if not (nTerm == []):
                raise ValueError("Term already exist")

                # Insert data
            cursor.execute("INSERT INTO TERMS (term_id, term_name) VALUES(:termId, :termName)", termId=term.id,
                           termName=term.name)
            if not cursor.rowcount:
                raise oracledb.Error

    def update_term(self, term):
        '''Update a term for the given Term object'''
        with self.__get_cursor() as cursor:
            if not isinstance(term, Term):
                raise ValueError
            cursor.execute("UPDATE terms SET term_name = :termName WHERE term_id = :termId", termId=term.id,
                           termName=term.name)
            if not cursor.rowcount:
                raise oracledb.Error

    def delete_term(self, term_id):
        '''Delete a term in DB for the given Term object id'''
        with self.__get_cursor() as cursor:
            courseToDelete = []
            results = cursor.execute("SELECT course_id FROM Courses WHERE term_id = :termId", termId = term_id)
            for result in results:
                courseId = result[0]
                courseToDelete.append(courseId)
            
            for courseId in courseToDelete:
                cursor.execute("DELETE FROM courses_elements WHERE course_id = :courseId", courseId=courseId)
            
            cursor.execute("DELETE FROM courses WHERE term_id = :termId", termId = term_id)
            
            cursor.execute("DELETE FROM terms WHERE term_id = :termId", termId = term_id)

    # COMPETENCY
    def get_competencies(self):
        '''Returns all Competency objects in a list'''
        with self.__get_cursor() as cursor:
            newListCompetency = []
            results = cursor.execute(
                "SELECT competency_id, competency, competency_achievement, competency_type  FROM COMPETENCIES")
            for result in results:
                newCompetency = Competency(id=result[0], name=result[1], achievement=result[2], type=result[3])
                newListCompetency.append(newCompetency)
            return newListCompetency

    def get_competency(self, competencyId):
        '''Returns a specific competency'''
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT competency_id, competency, competency_achievement, competency_type FROM COMPETENCIES WHERE competency_id=:competencyId",
                competencyId=competencyId)
            for result in results:
                competency = Competency(id=result[0], name=result[1], achievement=result[2], type=result[3])
                return competency
            return None

    def add_competency(self, competency):
        '''Add a competency to the DB for the given Competency object'''
        with self.__get_cursor() as cursor:
            if not isinstance(competency, Competency):
                raise ValueError("Should be Competency obj")

            # Check if competency doesn't already exist
            results = cursor.execute(
                "SELECT * FROM COMPETENCIES where competency_id = :competencyId or competency = :competencyName",
                competencyId=competency.id, competencyName=competency.name)
            nCompetency = [result for result in results if (result[0] == competency.id or result[1] == competency.name)]
            if not (nCompetency == []):
                raise ValueError("Competency already exist")

            # Insert data
            cursor.execute(
                "INSERT INTO COMPETENCIES (competency_id, competency, competency_achievement, competency_type) VALUES(:competencyId, :competencyName, :competencyAchievement, :competencyType)",
                competencyId=competency.id, competencyName=competency.name,
                competencyAchievement=competency.achievement, competencyType=competency.type)
            if not cursor.rowcount:
                raise oracledb.Error

    def update_competency(self, competency):
        '''Update a competency for the given Competency object'''
        with self.__get_cursor() as cursor:
            if not isinstance(competency, Competency):
                raise ValueError
            cursor.execute(
                "UPDATE COMPETENCIES SET competency = :competencyName, competency_achievement = :competencyAchievement, competency_type = :competencyType WHERE competency_id = :competencyId",
                competencyId=competency.id, competencyName=competency.name,
                competencyAchievement=competency.achievement, competencyType=competency.type)
            if not cursor.rowcount:
                raise oracledb.Error

    def delete_competency(self, competency_id):
        '''Delete a competency in DB for the given COmpetency object id'''
        with self.__get_cursor() as cursor:

            # Delete associated elements
            cursor.execute("DELETE FROM elements WHERE competency_id = :competencyId", competencyId=competency_id)
            

            cursor.execute("DELETE FROM competencies WHERE competency_id = :competencyId", competencyId=competency_id)
            if not cursor.rowcount:
                raise oracledb.Error

    # ELEMENT
    def get_elements(self):
        '''Returns all Element objects in a list'''
        with self.__get_cursor() as cursor:
            newListElement = []
            results = cursor.execute(
                "SELECT element_id, element_order, element, element_criteria, competency_id FROM ELEMENTS")
            for result in results:
                newElement = Element(id=result[0], order=result[1], name=result[2], criteria=result[3],
                                     competencyId=result[4])
                newListElement.append(newElement)
            return newListElement

    def get_element(self, elementId):
        '''Returns a specific domain'''
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT element_id, element_order, element, element_criteria, competency_id FROM ELEMENTS WHERE element_id = :elementId",
                elementId=elementId)
            for result in results:
                foundElement = Element(id=result[0], order=result[1], name=result[2], criteria=result[3],
                                       competencyId=result[4])
                return foundElement
            return None

    def get_elements_covered_by_a_course(self, courseId):
        '''Returns all the Elements covered by a specific course'''
        with self.__get_cursor() as cursor:
            newListElement = []
            results = cursor.execute(
                "SELECT element_id, element_order, element, element_criteria, competency_id FROM ELEMENTS JOIN courses_elements USING(element_id) JOIN courses USING(course_id) JOIN competencies USING(competency_id) WHERE course_id=:courseId",
                courseId=courseId)
            for result in results:
                newElement = Element(id=result[0], order=result[1], name=result[2], criteria=result[3],
                                     competencyId=result[4])
                newListElement.append(newElement)
            return newListElement

    def add_element(self, element):
        '''Add an element to the DB for the given Element object'''
        with self.__get_cursor() as cursor:
            if not isinstance(element, Element):
                raise ValueError("Should be Element obj")
            
            # Check if Competency exists
            results = cursor.execute("SELECT * FROM COMPETENCIES where competency_id = :competencyId",
                                     competencyId=element.competencyId)
            nCompetency = [result for result in results if result[0] == element.competencyId]
            if nCompetency is None:
                raise ValueError("Competency doesn't exist. Create a competency first")
            # Insert Data
            cursor.execute(
                "INSERT INTO ELEMENTS (element_order, element, element_criteria, competency_id) VALUES (:elementOrder, :elementName, :elementCriteria, :competencyId)",
                elementOrder=element.order, elementName=element.name,
                elementCriteria=element.criteria, competencyId=element.competencyId)
            if not cursor.rowcount:
                raise oracledb.Error

    def add_element_course_bridging(self,elementId,courseId,elementHours):
        '''Add a record to the bridging table'''
        with self.__get_cursor() as cursor:
            # Check if the record doesn't already exist in the bridging table
            results = cursor.execute(
                "SELECT course_id, element_id FROM COURSES_ELEMENTS where element_id = :elementId and course_id = :courseId",
                elementId=elementId, courseId=courseId)
            for result in results:
                if result:
                    raise ValueError("record already exists")
            cursor.execute(
                "INSERT INTO COURSES_ELEMENTS (element_id, course_id,element_hours) VALUES(:elementId, :courseId,:elementHours)",elementId=elementId, courseId=courseId,elementHours=elementHours)
            if not cursor.rowcount:
                raise oracledb.Error

    def delete_element_course_bridging(self,elementId,courseId):
        '''Delete a record from the bridging table'''
        with self.__get_cursor() as cursor:
            cursor.execute(
                "DELETE FROM COURSES_ELEMENTS WHERE element_id = :elementId and course_id = :courseId",
                elementId=elementId, courseId=courseId)
            if not cursor.rowcount:
                raise oracledb.Error

    def get_sum_hours(self,courseId):
        '''Get records from the bridging table'''
        with self.__get_cursor() as cursor:
            hours=0
            try:
                results = cursor.execute(
                    "SELECT SUM(element_hours) FROM COURSES_ELEMENTS WHERE course_id=:courseId",
                    courseId=courseId)
                for result in results:
                    if result[0] is None:
                        return 0
                    hours=result[0]
            except TypeError:
                return 0
            return hours

    def update_element(self, element):
        '''Update a element for the given Competency object'''
        with self.__get_cursor() as cursor:
            if not isinstance(element, Element):
                raise ValueError
            cursor.execute(
                "UPDATE elements SET element_order = :elementOrder, element = :elementName, element_criteria = :elementCriteria, competency_Id = :competencyId WHERE element_id  = :elementId",
                elementId=element.id, elementOrder=element.order, elementName=element.name,
                elementCriteria=element.criteria, competencyId=element.competencyId)
            if not cursor.rowcount:
                raise oracledb.Error

    def delete_element(self, element_id):
        '''Delete a element for the given Element object'''
        with self.__get_cursor() as cursor:

            cursor.execute("DELETE FROM courses_elements WHERE element_id = :elementId", elementId=element_id)
            
            cursor.execute("DELETE FROM elements WHERE element_id = :elementId", elementId=element_id)
            

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

    def get_users(self):
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                'select id, group_id, email, password, name, blocked from courseapp_users order by id')
            users = []
            for row in results:
                user = User(id=row[0], group_id=row[1], email=row[2],
                            password=row[3], name=row[4], blocked=row[5] == 1)
                users.append(user)
            return users

    def add_user(self, user):
        if not isinstance(user, User):
            raise TypeError("You must provide a user object to this function.")
        with self.__get_cursor() as cursor:
            cursor.execute(
                'insert into courseapp_users (group_id, email, password, name) values (:group_id, :email, :password, :name)',
                email=user.email,
                password=user.password,
                name=user.name,
                group_id=user.group_id)

    def get_user(self, id):
        if not isinstance(id, int):
            raise TypeError("Id must be an integer")
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                'select id, group_id, email, password, name, blocked from courseapp_users where id=:id', id=id)
            for row in results:
                user = User(id=row[0], group_id=row[1], email=row[2],
                            password=row[3], name=row[4], blocked=row[5] == 1)
                return user
        return None

    def get_user_by_email(self, email):
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                'select id, group_id, email, password, name, blocked from courseapp_users where email=:email',
                email=email)
            for row in results:
                user = User(id=row[0], group_id=row[1], email=row[2],
                            password=row[3], name=row[4], blocked=row[5] == 1)
                return user
        return None

    def delete_user_by_id(self, id):
        if not isinstance(id, int):
            raise TypeError("Id must be an integer")
        with self.__get_cursor() as cursor:
            cursor.execute('delete from courseapp_users where id=:id', id=id)

    def update_user(self, user):
        if not isinstance(user, User):
            raise TypeError("You must provide a user object to this function.")
        with self.__get_cursor() as cursor:
            cursor.execute(
                'update courseapp_users set group_id=:group_id, email=:email, password=:password, name=:name, blocked=:blocked where id=:id',
                group_id=user.group_id,
                email=user.email,
                password=user.password,
                name=user.name,
                id=user.id,
                blocked=1 if user.blocked else 0)

    def delete_user(self, user):
        if not isinstance(user, User):
            raise TypeError("You must provide a user object to this function.")
        with self.__get_cursor() as cursor:
            cursor.execute('delete from courseapp_users where id=:id', id=user.id)

    def get_groups(self):
        with self.__get_cursor() as cursor:
            results = cursor.execute('select id, name from courseapp_groups order by id')
            groups = []
            for row in results:
                groups.append(Group(id=row[0], name=row[1]))
            return groups

    def get_group(self, id):
        if not isinstance(id, int):
            raise TypeError("Id must be an integer")
        with self.__get_cursor() as cursor:
            results = cursor.execute('select id, name from courseapp_groups where id=:id', id=id)
            for row in results:
                group = Group(id=row[0], name=row[1])
                return group
        return None

    def add_group(self, group):
        if not isinstance(group, Group):
            raise TypeError("You must provide a group object to this function.")
        with self.__get_cursor() as cursor:
            cursor.execute('insert into courseapp_groups (name) values (:name)',
                           name=group.name)

    def update_group(self, group):
        if not isinstance(group, Group):
            raise TypeError("You must provide a group object to this function.")
        with self.__get_cursor() as cursor:
            cursor.execute('update courseapp_groups set name=:name where id=:id',
                           id=group.id,
                           name=group.name)

    def delete_group(self, group):
        if not isinstance(group, Group):
            raise TypeError("You must provide a group object to this function.")
        with self.__get_cursor() as cursor:
            # delete all users first
            cursor.execute('delete from courseapp_users where group_id=:id',
                           id=group.id)

            # finally, delete group
            cursor.execute('delete from courseapp_groups where id=:id',
                           id=group.id)


if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')