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
                                   work_hours=result[4], description=result[5], domain_id=result[6], term_id=result[7])
                newListCourse.append(newCourse)
            return newListCourse

    def get_specific_course(self, courseId):
        '''Returns a specific course'''
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT course_id, course_title, theory_hours, lab_hours, work_hours, description, domain_id, term_id FROM COURSES WHERE course_id=:courseId",
                courseId=courseId)
            for result in results:
                course = Course(id=result[0], name=result[1], theory_hours=result[2], lab_hours=result[3],
                                work_hours=result[4], description=result[5], domain_id=result[6], term_id=result[7])
            return course

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
            if (not isinstance(course, Course)):
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
                "SELECT domain_id, domain, domain_description FROM DOMAINS where domain_id = :domain_id",
                domain_id=course.domain_id)
            domain = [result for result in results if result[0] == course.domain_id]
            if domain is None:
                raise ValueError("Domain doesn't exist. Create a domain first")

            # Check if term exists
            results = cursor.execute("SELECT term_id FROM TERMS where term_id = :term_id", term_id=course.term_id)
            term = [result for result in results if result[0] == course.term_id]
            if term is None:
                raise ValueError("Term doesn't exist. Create a term first")

            # Insert data
            cursor.execute(
                "INSERT INTO COURSES (course_id, course_title, theory_hours, lab_hours, work_hours, description, domain_id, term_id) VALUES (:courseId, :title, :theory, :lab, :work, :description, :domain_id, :term_id)",
                courseId=course.id, title=course.name, theory=course.theory_hours, lab=course.lab_hours,
                work=course.work_hours, description=course.description, domain_id=course.domain_id,
                term_id=course.term_id)
            if not cursor.rowcount:
                raise oracledb.Error

    def update_course(self, course, oldCourseId):
        '''Update a coursefor the given Course object'''
        with self.__get_cursor() as cursor:
            if (not isinstance(course, Course)):
                raise ValueError

            ##Create course with the updated data            
            # Check if domain exists
            results = cursor.execute(
                "SELECT domain_id, domain, domain_description FROM DOMAINS where domain_id = :domain_id",
                domain_id=course.domain_id)
            domain = [result for result in results if result[0] == course.domain_id]
            if domain is None:
                raise ValueError("Domain doesn't exist. Create a domain first")

            # Check if term exists
            results = cursor.execute("SELECT term_id FROM TERMS where term_id = :term_id", term_id=course.term_id)
            term = [result for result in results if result[0] == course.term_id]
            if term is None:
                raise ValueError("Term doesn't exist. Create a term first")

            # Insert data
            cursor.execute(
                "INSERT INTO COURSES (course_id, course_title, theory_hours, lab_hours, work_hours, description, domain_id, term_id) VALUES (:courseId, :title, :theory, :lab, :work, :description, :domain_id, :term_id)",
                courseId=course.id, title=course.name, theory=course.theory_hours, lab=course.lab_hours,
                work=course.work_hours, description=course.description, domain_id=course.domain_id,
                term_id=course.term_id)
            if not cursor.rowcount:
                raise oracledb.Error

            ##Update bridgin tbl
            cursor.execute(
                "UPDATE COURSES_ELEMENTS SET course_id = :courseId WHERE course_id = :OldCourseId",
                OldCourseId=oldCourseId,
                courseId=course.id)
            if not cursor.rowcount:
                raise oracledb.Error

            ##Delete old course
            cursor.execute("DELETE FROM courses WHERE course_id = :courseId", courseId=oldCourseId)
            if not cursor.rowcount:
                raise oracledb.Error

    def delete_course(self, course):
        '''Delete a course in DB for the given Course object id'''
        with self.__get_cursor() as cursor:
            if (not isinstance(course, Course)):
                raise ValueError

            # Check if course exists in course_element table
            results = cursor.execute("SELECT * FROM COURSES_ELEMENTS where course_id = :courseId", courseId=course.id)
            nCourse = [result for result in results if result[0] == course.id]
            if nCourse is not []:
                cursor.execute("DELETE FROM courses_elements WHERE course_id = :courseId", courseId=course.id)

            cursor.execute("DELETE FROM courses WHERE course_id = :courseId", courseId=course.id)
            if not cursor.rowcount:
                raise oracledb.Error

    def get_domains_api(self, page_num=1, page_size=50):
        domains = []
        offset = (page_num - 1) * page_size
        prev_page = None
        next_page = None
        with self.__get_cursor() as cursor:
            results = cursor.execute('select count(*) from domains')
            count = results.fetchone()[0]
            results = cursor.execute(
                'select domain_id, domain, domain_description from domains order by domain_id offset :offset rows fetch next :page_size rows only',
                offset=offset, page_size=page_size)
            for row in results:
                domain = Domain(id=row[0], name=row[1],
                                description=row[2])
                domains.append(domain)
        if page_num > 1:
            prev_page = page_num - 1
        if len(domains) > 0 and (count / page_size) > page_num:
            next_page = page_num + 1
        return domains, prev_page, next_page, count

    def get_terms_api(self, page_num=1, page_size=50):
        terms = []
        offset = (page_num - 1) * page_size
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
        if len(terms) > 0 and (count / page_size) > page_num:
            next_page = page_num + 1
        return terms, prev_page, next_page, count

    def get_courses_api(self, page_num=1, page_size=50):
        courses = []
        offset = (page_num - 1) * page_size
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
                                description=row[5], domain_id=row[6], term_id=row[7])
                courses.append(course)
        if page_num > 1:
            prev_page = page_num - 1
        if len(courses) > 0 and (count / page_size) > page_num:
            next_page = page_num + 1
        return courses, prev_page, next_page, count

    def get_competencies_api(self, page_num=1, page_size=50):
        competencies = []
        offset = (page_num - 1) * page_size
        prev_page = None
        next_page = None
        with self.__get_cursor() as cursor:
            results = cursor.execute('select count(*) from competencies')
            count = results.fetchone()[0]
            # id, name, achievement, type
            results = cursor.execute(
                'select competency_id, COMPETENCY, COMPETENCY_ACHIEVEMENT, COMPETENCY_TYPE from competencies order by competency_id offset :offset rows fetch next :page_size rows only',
                offset=offset, page_size=page_size)
            for row in results:
                competency = Competency(id=row[0], name=row[1], achievement=row[2], type=row[3])
                competencies.append(competency)
        if page_num > 1:
            prev_page = page_num - 1
        if len(competencies) > 0 and (count / page_size) > page_num:
            next_page = page_num + 1
        return competencies, prev_page, next_page, count

    def get_elements_api(self, page_num=1, page_size=50):
        elements = []
        offset = (page_num - 1) * page_size
        prev_page = None
        next_page = None
        with self.__get_cursor() as cursor:
            results = cursor.execute('select count(*) from elements')
            count = results.fetchone()[0]
            # id, order, name, criteria, competencyId
            results = cursor.execute(
                'select element_id, ELEMENT_ORDER, ELEMENT, ELEMENT_CRITERIA, COMPETENCY_ID from elements order by element_id offset :offset rows fetch next :page_size rows only',
                offset=offset, page_size=page_size)
            for row in results:
                element = Element(id=row[0], order=row[1], name=row[2], criteria=row[3], competencyId=row[4])
                elements.append(element)
        if page_num > 1:
            prev_page = page_num - 1
        if len(elements) > 0 and (count / page_size) > page_num:
            next_page = page_num + 1
        return elements, prev_page, next_page, count

    def get_domains(self):
        with self.__get_cursor() as cursor:
            domains = []

            results = cursor.execute("SELECT domain_id, domain, domain_description FROM DOMAINS")

            for result in results:
                domains.append(Domain(id=result[0], name=result[1], description=result[2]))

            return domains

    def get_domain(self, domain_id):
        with self.__get_cursor() as cursor:
            results = cursor.execute("SELECT domain_id, domain, domain_description FROM DOMAINS WHERE domain_id = :domain_id", domain_id=domain_id)

            for result in results:
                domain = Domain(id=result[0], name=result[1], description=result[2])

            return domain

    def get_courses_in_domain(self, domain_id):
        '''Returns a specific domain'''
        with self.__get_cursor() as cursor:
            impactedCourse = []
            results = cursor.execute(
                "SELECT course_id, course_title, theory_hours, lab_hours, work_hours, description, domain_id, term_id FROM COURSES WHERE domain_id = :domain_id",
                domain_id=domain_id)
            for result in results:
                newCourse = Course(id=result[0], name=result[1], theory_hours=result[2], lab_hours=result[3],
                                   work_hours=result[4], description=result[5], domain_id=result[6], term_id=result[7])
                impactedCourse.append(newCourse)
            return impactedCourse

    def add_domain(self, domain):
        with self.__get_cursor() as cursor:
            if not isinstance(domain, Domain):
                raise TypeError

            cursor.execute("INSERT INTO domains (domain_id, domain, domain_description) VALUES (:domain_id, :domain, "
                           ":domain_description)",
                           domain_id=domain.id, domain=domain.name, domain_description=domain.description)

    def update_domain(self, domain):
        with self.__get_cursor() as cursor:
            if not isinstance(domain, Domain):
                raise TypeError

            cursor.execute("UPDATE domains SET domain = :domain, domain_description = :domain_description WHERE "
                           "domain_id = :domain_id",
                           domain=domain.name, domain_description=domain.description, domain_id=domain.id)

            if not cursor.rowcount:  # if no rows were updated
                raise KeyError

    def delete_domain(self, domain_id):
        with self.__get_cursor() as cursor:
            cursor.execute("DELETE FROM domains WHERE domain_id = :domain_id", domain_id=domain_id)

    def get_courses_in_term(self, term_id):
        '''Returns a specific domain'''
        with self.__get_cursor() as cursor:
            impactedCourse = []
            results = cursor.execute(
                "SELECT course_id, course_title, theory_hours, lab_hours, work_hours, description, domain_id, term_id FROM COURSES WHERE term_id = :term_id",
                term_id=term_id)
            for result in results:
                newCourse = Course(id=result[0], name=result[1], theory_hours=result[2], lab_hours=result[3],
                                   work_hours=result[4], description=result[5], domain_id=result[6], term_id=result[7])
                impactedCourse.append(newCourse)
            return impactedCourse

    def get_terms(self):
        with self.__get_cursor() as cursor:
            terms = []

            results = cursor.execute("SELECT term_id, term_name FROM TERMS")

            for result in results:
                terms.append(Term(id=result[0], name=result[1]))

            return terms

    def get_term(self, term_id):
        with self.__get_cursor() as cursor:
            results = cursor.execute("SELECT term_id, term_name FROM TERMS WHERE term_id=:term_id", term_id=term_id)

            for result in results:
                term = Term(id=result[0], name=result[1])

            return term

    def add_term(self, term):
        with self.__get_cursor() as cursor:
            if not isinstance(term, Term):
                raise TypeError

            cursor.execute("INSERT INTO TERMS (term_id, term_name) VALUES(:term_id, :term_name)", term_id=term.id,
                           term_name=term.name)

    def update_term(self, term):
        with self.__get_cursor() as cursor:
            if not isinstance(term, Term):
                raise TypeError

            cursor.execute("UPDATE terms SET term_name = :term_name WHERE term_id = :term_id", term_id=term.id,
                           term_name=term.name)

            if not cursor.rowcount:  # if no rows were updated
                raise KeyError

    def delete_term(self, term_id):
        with self.__get_cursor() as cursor:
            cursor.execute("DELETE FROM terms WHERE term_id = :term_id", term_id=term_id)

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

    def get_specific_competency(self, competencyId):
        '''Returns a specific competency'''
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT competency_id, competency, competency_achievement, competency_type FROM COMPETENCIES WHERE competency_id=:competencyId",
                competencyId=competencyId)
            for result in results:
                competency = Competency(id=result[0], name=result[1], achievement=result[2], type=result[3])
            return competency

    def add_competency(self, competency):
        '''Add a competency to the DB for the given Competency object'''
        with self.__get_cursor() as cursor:
            if (not isinstance(competency, Competency)):
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

    def update_competency(self, competency, oldCompetencyId):
        '''Update a competency for the given Competency object'''
        with self.__get_cursor() as cursor:
            if (not isinstance(competency, Competency)):
                raise ValueError

            ##Create competency with the updated data            
            # Insert data
            cursor.execute(
                "INSERT INTO COMPETENCIES (competency_id, competency, competency_achievement, competency_type) VALUES(:competencyId, :competencyName, :competencyAchievement, :competencyType)",
                competencyId=competency.id, competencyName=competency.name,
                competencyAchievement=competency.achievement, competencyType=competency.type)
            if not cursor.rowcount:
                raise oracledb.Error

            ##Update bridgin tbl
            cursor.execute(
                "UPDATE ELEMENTS SET competency_id = :competencyId WHERE competency_id = :OldCompetencyId",
                OldCompetencyId=oldCompetencyId,
                competencyId=competency.id)
            if not cursor.rowcount:
                raise oracledb.Error

            ##Delete old course
            cursor.execute("DELETE FROM COMPETENCIES WHERE competency_id = :competencyId", competencyId=oldCompetencyId)
            if not cursor.rowcount:
                raise oracledb.Error

    def delete_competency(self, competency):
        '''Delete a competency in DB for the given COmpetency object id'''
        with self.__get_cursor() as cursor:
            if (not isinstance(competency, Competency)):
                raise ValueError

            # Delete associated elements
            cursor.execute("DELETE FROM elements WHERE competency_id = :competencyId", competencyId=competency.id)
            if not cursor.rowcount:
                raise oracledb.Error

            cursor.execute("DELETE FROM competencies WHERE competency_id = :competencyId", competencyId=competency.id)
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

    def get_specific_element(self, elementId):
        '''Returns a specific domain'''
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT element_id, element_order, element, element_criteria, competency_id FROM ELEMENTS WHERE element_id = :elementId",
                elementId=elementId)
            for result in results:
                foundElement = Element(id=result[0], order=result[1], name=result[2], criteria=result[3],
                                       competencyId=result[4])
            return foundElement

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
            if (not isinstance(element, Element)):
                raise ValueError("Should be Element obj")
            # Check if Competency exists
            results = cursor.execute("SELECT * FROM COMPETENCIES where competency_id = :competencyId",
                                     competencyId=element.competencyId)
            nCompetency = [result for result in results if result[0] == element.competencyId]
            if nCompetency is None:
                raise ValueError("Competency doesn't exist. Create a competency first")
            # Insert Data
            cursor.execute(
                "INSERT INTO ELEMENTS (element_id, element_order, element, element_criteria, competency_id) VALUES (:elementId, :elementOrder, :elementName, :elementCriteria, :competencyId)",
                elementId=element.id, elementOrder=element.order, elementName=element.name,
                elementCriteria=element.criteria, competencyId=element.competencyId)
            if not cursor.rowcount:
                raise oracledb.Error

    def add_element_course_bridging(self, elementId, courseId, elementHours):
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
                "INSERT INTO COURSES_ELEMENTS (element_id, course_id,element_hours) VALUES(:elementId, :courseId,:elementHours)",
                elementId=elementId, courseId=courseId, elementHours=elementHours)
            if not cursor.rowcount:
                raise oracledb.Error

    def delete_element_course_bridging(self, elementId, courseId):
        '''Delete a record from the bridging table'''
        with self.__get_cursor() as cursor:
            cursor.execute(
                "DELETE FROM COURSES_ELEMENTS WHERE element_id = :elementId and course_id = :courseId",
                elementId=elementId, courseId=courseId)
            if not cursor.rowcount:
                raise oracledb.Error

    def get_sum_hours(self, courseId):
        '''Get records from the bridging table'''
        with self.__get_cursor() as cursor:
            hours = 0
            try:
                results = cursor.execute(
                    "SELECT SUM(element_hours) FROM COURSES_ELEMENTS WHERE course_id=:courseId",
                    courseId=courseId)
                for result in results:
                    if (result[0] is None):
                        return 0
                    hours = result[0]
            except TypeError:
                return 0
            return hours

    def update_element(self, element):
        '''Update a element for the given Competency object'''
        with self.__get_cursor() as cursor:
            if (not isinstance(element, Element)):
                raise ValueError
            cursor.execute(
                "UPDATE elements SET element_order = :elementOrder, element = :elementName, element_criteria = :elementCriteria, competency_Id = :competencyId WHERE element_id  = :elementId",
                elementId=element.id, elementOrder=element.order, elementName=element.name,
                elementCriteria=element.criteria, competencyId=element.competencyId)
            if not cursor.rowcount:
                raise oracledb.Error

    def delete_element(self, element):
        '''Delete a element for the given Element object'''
        with self.__get_cursor() as cursor:
            if not isinstance(element, Element):
                raise ValueError("Should be an Element obj")

            cursor.execute("DELETE FROM elements WHERE element_id = :elementId", elementId=element.id)
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
