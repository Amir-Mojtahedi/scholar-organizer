/** 
    This file is used to create the custom object types that will be used by our
    application. It will be called by the setup.sql file inorder to drop and
    recreate all the objects when the program is run.

*/


/**
    term_typ is an object that contains a number representing the NUMBER of the 
    term and a CHAR that represents the term's name (Name is the season the term
    is in)

*/
CREATE OR REPLACE TYPE term_typ IS OBJECT(
        term_id NUMBER(3),
        term_name CHAR(6)
    );
/
/**


*/

CREATE OR REPLACE TYPE domain_typ AS OBJECT(
        domain_id NUMBER, 
        domain VARCHAR2(25), 
        domain_description VARCHAR2(500)
    );
/    
CREATE OR REPLACE TYPE competency_typ AS OBJECT(
        competency_id CHAR(4),
        competency VARCHAR2(250),
        competency_achievement VARCHAR2(250),
        competency_type VARCHAR2(10)
    );
/
CREATE OR REPLACE TYPE element_typ AS OBJECT(
        
        element_order NUMBER,
        element VARCHAR2(250),
        element_criteria VARCHAR2(250),
        element_hours NUMBER,
        competency competency_typ
    );
/    
CREATE OR REPLACE TYPE element_array IS VARRAY(10) OF element_typ;
/   
CREATE OR REPLACE TYPE course_typ AS OBJECT(
        course_id CHAR(10),
        course_name VARCHAR2(50),
        theory_hours NUMBER,
        lab_hours NUMBER,
        work_hours NUMBER,
        course_description VARCHAR2(500),
        domain domain_typ,
        term term_typ
    );