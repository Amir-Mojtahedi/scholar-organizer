/** 
    Author: Christopher Kwok
    Courses package is a packages that contains all the procedures and functions
    that are required to add, update or delete information from a table.
    
    It also contains functions that are used to determine the values of the 
    calculated fields (ie the total hours of a course)
    
*/

CREATE OR REPLACE PACKAGE courses_package AS
    
    
    FUNCTION calculate_total_hours(courseid CHAR ) return NUMBER;
    FUNCTION calculate_credits(courseid CHAR) RETURN NUMBER;
    FUNCTION calculate_terminal(icourse_id CHAR, icompetency_id CHAR) RETURN boolean;
    
    PROCEDURE add_term (vterm IN term_typ);
    PROCEDURE add_domain(vdomain IN domain_typ);
    PROCEDURE add_competency(vcompetency IN competency_typ);
    PROCEDURE add_element(velement IN element_typ);
    PROCEDURE add_course(vcourse IN course_typ);
    PROCEDURE add_courses_elements(
        icourse_id IN CHAR,
        ielement_order IN NUMBER,
        icompetency_id IN VARCHAR2,
        ielement_hours IN NUMBER
        );
    PROCEDURE add_competency_and_elements(vcompetency IN competency_typ,velement_array IN element_array);
    
    PROCEDURE update_term( vterm IN term_typ);
    PROCEDURE update_domain(vdomain IN domain_typ);
    PROCEDURE update_course (
        i_courseid VARCHAR2,
        i_title VARCHAR2,
        i_theory NUMBER,
        i_lab NUMBER,
        i_work NUMBER,
        i_description VARCHAR2,
        i_domainid VARCHAR2,
        i_termid NUMBER
        );
    PROCEDURE update_competency(
        i_competencyid CHAR,
        i_competency VARCHAR2,
        i_competency_achievement VARCHAR2,
        i_competency_type VARCHAR2
    );
    
    
    PROCEDURE delete_term (vterm_id IN NUMBER);
    PROCEDURE delete_domain( vdomain_id IN NUMBER);
    PROCEDURE delete_competency (vcompetency_id IN CHAR);
    PROCEDURE delete_element(velement_id IN CHAR);
    PROCEDURE delete_course (vcourse_id IN CHAR);
    
    
END courses_package;
/


CREATE OR REPLACE PACKAGE BODY courses_package IS

    
    /**
        calculate_total_hours is a function that will calculate the total hours
        of a course based on the user supplied courseid. It searches the database
        for the lab hours, theory hours and multiplies the sum by 15 to determine
        how many hours in a semester are dedicated to that course.
        
        @param courseid is a char that represents a course in the database
        @return total number of hourse of the
    */
    FUNCTION calculate_total_hours( 
        courseid CHAR
    ) return NUMBER
    IS
        lab_time NUMBER;
        class_time NUMBER;
    BEGIN
        SELECT lab_hours, theory_hours INTO lab_time, class_time FROM Courses WHERE courseid = course_id;
        RETURN (lab_time + class_time) * 15;
    END;
    
    --Takes a courseid and returns a number representing the course credits based on hours.
    
    /**
        calculate_credits is a function that takes in a courseid and 
        returns the credit value of the course.  This is done by divinding
        the sum of the weekly lab, class and homework hours by three (3).
    
    */
    FUNCTION calculate_credits(
        courseid CHAR
        ) RETURN NUMBER
    IS
        lab_time NUMBER;
        class_time NUMBER;
        homework_time NUMBER;
    BEGIN
        SELECT lab_hours, theory_hours, work_hours INTO lab_time, class_time, homework_time FROM Courses WHERE courseid = course_id;
        RETURN (lab_time  + class_time + homework_time) / 3;
    END;
    
    FUNCTION calculate_terminal(icourse_id CHAR, icompetency_id CHAR) RETURN boolean 
    IS
        last_term NUMBER;
        current_term NUMBER;
    BEGIN
        SELECT MAX(term_id) INTO last_term FROM elements 
            INNER JOIN competencies USING (competency_id)
            INNER JOIN courses_elements USING (element_id) 
            INNER JOIN courses USING(course_id) WHERE competency_id = icompetency_id;
        SELECT term_id INTO current_term FROM courses WHERE course_id = icourse_id;
        
        return last_term = current_term;
    END;
        
    /**
        add_term is a procedure that takes a term_typ object and adds it's components
        into the terms table
    */
    PROCEDURE add_term (
        vterm IN term_typ
    )
    IS
        term_exists NUMBER;
    BEGIN
        SELECT COUNT(*) INTO term_exists FROM terms WHERE term_id = vterm.term_id;
        IF term_exists = 0 THEN
            INSERT INTO terms VALUES(vterm.term_id, vterm.term_name);
        END IF;
    END;
    
    
    /**
        update_term is a procedure that takes a term object with an
        existing term id and updates the record containing that term id
        NOTE: This procedure is currently unused.
    */
    PROCEDURE update_term( 
        vterm IN term_typ
    )
    IS
    BEGIN
        UPDATE terms SET term_name = vterm.term_name WHERE term_id = vterm.term_id;
    END;
    
    
    /**
        delete_term is a procedure that takes in a number representing a term id and 
        deletes the record that contains that id.
    */
    PROCEDURE delete_term (vterm_id IN NUMBER)
    IS
    BEGIN
        DELETE FROM terms WHERE term_id = vterm_id;
    END;
    
    /**
        add_domain is a procedure that taking in a domain_typ object and adds it's components
        to the domain table.    
    */
    PROCEDURE add_domain(
        vdomain IN domain_typ
        )
    IS
        domain_exists NUMBER;
    BEGIN
        SELECT COUNT(*) INTO domain_exists FROM domains WHERE domain_id = vdomain.domain_id;
        IF domain_exists = 0 THEN
            INSERT INTO domains VALUES( vdomain.domain_id, vdomain.domain, vdomain.domain_description);
        END IF;   
    END;
    
    /**
        update_domain is a procedure that takes in a domain object and updates the domains table
        record whose domain id matches.
        NOTE: This procedure is currently unused.
    */
    PROCEDURE update_domain(
        vdomain IN domain_typ
    )
    IS
    BEGIN
        UPDATE domains SET domain=vdomain.domain, domain_description = vdomain.domain_description
            WHERE domain_id = vdomain.domain_id;
    END;
    
    PROCEDURE delete_domain( vdomain_id IN NUMBER)
    IS
    BEGIN
        DELETE FROM domains WHERE domain_id = vdomain_id;
    END;

    /**
        add_competency is a procedure that takes in a competency_typ object and adds it's components
        to the competency table.
    */
    PROCEDURE add_competency(
        vcompetency IN competency_typ
    )
    IS
        competency_exists NUMBER;
    BEGIN
        SELECT COUNT(*) INTO competency_exists FROM competencies WHERE competency_id  = vcompetency.competency_id;
        IF competency_exists = 0 THEN
            INSERT INTO competencies VALUES(vcompetency.competency_id, vcompetency.competency,
                                            vcompetency.competency_achievement, 
                                            vcompetency.competency_type);
        END IF;
        
    END;
    
    /**
        update_competency is a procedure that takes in a value for each column in the competencies table and updates
        the record with the matching competency id. 
    */
    PROCEDURE update_competency(
        i_competencyid CHAR,
        i_competency VARCHAR2,
        i_competency_achievement VARCHAR2,
        i_competency_type VARCHAR2
    )
    IS
    BEGIN
     UPDATE competencies SET competency = i_competency, 
                            competency_achievement = i_competency_achievement,
                            competency_type = i_competency_type
                            WHERE competency_id = i_competencyid;
    END;
    
    /**
        delete_competency is a procdure that takes in a competency id and deletes the record of the competency
        with the matching competency id. 
        In order to do this it must also delete all the elements with the competency_id or else they will
        create parent key constraint conflicts.
    */
    
    PROCEDURE delete_competency (vcompetency_id IN CHAR)
    IS
    BEGIN
        DELETE FROM elements WHERE competency_id = vcompetency_id;
        DELETE FROM competencies WHERE competency_id = vcompetency_id;
    END;
    
    /**
        add_element is a procedure that takes in a element_typ object and adds it's components
        to the element table.
    */
    PROCEDURE add_element(
        velement IN element_typ
    )
    IS
        element_exists NUMBER;
    BEGIN
            INSERT INTO elements ( element, element_order, element_criteria, competency_id) 
                        VALUES(velement.element, 
                            velement.element_order, velement.element_criteria,
                                velement.competency.competency_id);
    
    END;
    
    /**
        delete_element is a procedure that takes in an element_id and deletes the
        record with the matching id in the courses_elements and elements table.
        courses_element deletion happens first to avoid parent key constraint conflicts.
    */
    PROCEDURE delete_element(velement_id IN CHAR)
    IS
    BEGIN
        DELETE FROM courses_elements WHERE element_id = velement_id;
        DELETE FROM elements WHERE element_id = velement_id;
    END;
    --
    /**
        add_course is a procedure that takes in a course_typ object and adds it's components to
        the courses table. 
        This also calls add_domain and add_term to add the course_typ's respective componenets into
        their tables.
    */
    PROCEDURE add_course(
        vcourse IN course_typ
    )
    IS
        course_exists NUMBER;
    BEGIN
        SELECT COUNT(*) INTO course_exists FROM courses WHERE course_id = vcourse.course_id;
        IF course_exists = 0 THEN
            INSERT INTO courses VALUES(
                        vcourse.course_id,
                        vcourse.course_name,
                        vcourse.theory_hours,
                        vcourse.lab_hours,
                        vcourse.work_hours,
                        vcourse.course_description,
                        vcourse.domain.domain_id,
                        vcourse.term.term_id
                        );
            courses_package.add_domain(vcourse.domain);
            courses_package.add_term(vcourse.term);

        END IF;
    END;
    
    /**
        update_course is a procedure that takes in all values for each column in the courses table
        and updates the columns of the record with the matching course_id
    */
    PROCEDURE update_course (
        i_courseid VARCHAR2,
        i_title VARCHAR2,
        i_theory NUMBER,
        i_lab NUMBER,
        i_work NUMBER,
        i_description VARCHAR2,
        i_domainid VARCHAR2,
        i_termid NUMBER
        )
    IS
    BEGIN
        UPDATE courses SET course_title = i_title,
                           theory_hours = i_theory,
                           lab_hours = i_lab,
                           work_hours = i_work,
                           description = i_description,
                           domain_id = i_domainid,
                           term_id = i_termid
                    WHERE course_id = i_courseid;
    END;
    
    /**
        delete_course is a procedure that takes in a course_id and deletes the records with the matching  
        id in the courses table as well as the records in the courses_elements bridging table.
    */
    PROCEDURE delete_course (vcourse_id IN CHAR)
    IS
        ce_exists NUMBER;
    BEGIN
        SELECT COUNT(*) INTO ce_exists FROM courses_elements WHERE course_id = vcourse_id;
        
        IF ce_exists !=0 THEN
            DELETE FROM courses_elements WHERE course_id = vcourse_id;
            END IF;
        DELETE FROM courses WHERE course_id = vcourse_id;
    END;
    
    /**
        add_courses_elements takes in values for that are required to add a record to courses_elements.
        As the element_ids are generated and are therefore not accessible to the user,
        a competency id and element order are used inorder to find the
        element's id. 
    */
    PROCEDURE add_courses_elements(
        icourse_id IN CHAR,
        ielement_order IN NUMBER,
        icompetency_id IN VARCHAR2,
        ielement_hours IN NUMBER
        )
    IS
        elem_id NUMBER;
    BEGIN
        SELECT element_id INTO elem_id FROM elements JOIN competencies USING (competency_id)
            WHERE element_order = ielement_order AND competency_id = icompetency_id;
    INSERT INTO courses_elements VALUES
        ( icourse_id, elem_id, ielement_hours);
    END;
    
    /**
        add_competency_and_elements is a procedure that takes in a competency_typ object
        and a varray of elements (element_varray) and adds both using the competency_typ's
        id to assosciate the elements.
        NOTE: This procedure is currently unused.
     */
    PROCEDURE add_competency_and_elements(
        vcompetency IN competency_typ,
        velement_array IN element_array
        )
    IS
    BEGIN
        add_competency(vcompetency);
        FOR elem IN 1 .. velement_array.COUNT LOOP
                add_element(velement_array(elem));
            END LOOP;
    END;
    
END courses_package;
/

COMMIT;