--creating all views
create or replace view view_courses as
    (select * from courses);
    
create or replace view view_courses_elements as
    (select * from courses 
     join courses_elements using(course_id)
     join elements using(element_id));
     
create or replace view view_courses_terms as
    (select * from courses
     join terms using(term_id));
     
create or replace view view_courses_domains as
    (select * from courses
     join domains using(domain_id));
     
create or replace view view_competencies as
    (select * from competencies);

create or replace view view_competencies_elements as
    (select * from competencies
     join elements using(competency_id));
     
create or replace view view_courses_elements_competencies as
    (select * from courses
     join courses_elements using(course_id)
     join elements using(element_id)
     join competencies using(competency_id));
     
CREATE OR REPLACE VIEW view_audit_logs
AS
    (SELECT * FROM audit_logs);