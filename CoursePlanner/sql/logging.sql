
--table to hold logs
create table audit_logs (
    --to keep track of logs in order
    log_id number generated always as identity,
    log_user varchar2(100),
    change_time timestamp,
    message varchar2(100)
);

--courses
    --update
    create or replace trigger after_courses_updated after update on courses for each row
    begin
        insert into audit_logs (log_user, change_time, message) values (USER, current_timestamp, 'updated: ' || :NEW.course_id);
    end;
    /
    --insert
    create or replace trigger after_courses_inserted after insert on courses for each row
    begin
        insert into audit_logs (log_user, change_time, message) values (USER, current_timestamp, 'updated: ' || :NEW.course_id);
    end;
    /
    --delete
    create or replace trigger after_courses_deleted after delete on courses for each row
    begin
        insert into audit_logs (log_user, change_time, message) values (USER, current_timestamp, 'deleted');
    end;
    /
    
--competencies
    --update
    create or replace trigger after_competencies_updated after update on competencies for each row
    begin
        insert into audit_logs (log_user, change_time, message) values (USER, current_timestamp, 'updated: ' || :NEW.competency_id);
    end;
    /
    --insert
    create or replace trigger after_competencies_inserted after insert on competencies for each row
    begin
        insert into audit_logs (log_user, change_time, message) values (USER, current_timestamp, 'updated: ' || :NEW.competency_id);
    end;
    /
    --delete
    create or replace trigger after_competencies_deleted after delete on competencies for each row
    begin
        insert into audit_logs (log_user, change_time, message) values (USER, current_timestamp, 'deleted');
    end;
    /