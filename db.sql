DROP TABLE IF EXISTS users;
CREATE TABLE Users ( 
    email VARCHAR(100),
    Userid Serial,
    Password VARCHAR(100),
    PRIMARY KEY (email)
    );

DROP TABLE IF EXISTS activities;
CREATE TABLE Activities(
    activity_id SERIAL,
    activity_name VARCHAR(100),
    Userid Integer,
    Time Date,
    PRIMARY KEY(activity_id, activity_name, Userid)
    );

DROP TABLE IF EXISTS tasks;
CREATE TABLE Tasks ( 
    Task_id SERIAL,
    Userid INTEGER,
    activity_id INTEGER,
    Task_name VARCHAR(100),
    Task_details VARCHAR(500),
    Task_duration Interval,
    Deadline DATE,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    PRIMARY KEY (task_id, Userid)
    );

INSERT INTO users (email, userid, password) VALUES ('dstekol@gmail.com',0, 'password1');
INSERT INTO users (email, userid, password) VALUES ('aliza@sucks.com',1, 'password2');
INSERT INTO users (email, userid, password) VALUES ('jakey@rocks.com',2,'password3');
INSERT INTO users (email, userid, password) VALUES ('serene@cult.com',3,'password4');
INSERT INTO users (email, userid, password) VALUES ('giuseppe@pizza.com', 4, 'password5');

INSERT INTO activities (activity_id, activity_name, userid, time) VALUES (0, 'Senior Projects', 1, '2024-04-08 15:40:00');
INSERT INTO activities (activity_id, activity_name, userid, time) VALUES (1, 'Databases', 1, '2024-04-08 15:40:00');
INSERT INTO activities (activity_id, activity_name, userid, time) VALUES (2, 'UI/UX', 1, '2024-04-08 15:40:00');

INSERT INTO tasks (task_id, userid, activity_id, task_name, task_details, task_duration, deadline, start_time, end_time) VALUES (1, 1, 0, 'Homework', 'Details of Task 1', NULL, NULL, '2024-04-08T15:40', '2024-04-08T17:00');
INSERT INTO tasks (task_id, userid, activity_id, task_name, task_details, task_duration, deadline, start_time, end_time) VALUES (2, 1, 1, 'Presentation', 'Details of Task 2', NULL, NULL, '2024-04-09T12:40', '2024-04-09T15:00');
INSERT INTO tasks (task_id, userid, activity_id, task_name, task_details, task_duration, deadline, start_time, end_time) VALUES (4, 1, 2, 'Homework', 'Details', NULL, NULL, '2024-04-09T12:40', '2024-04-09T15:00');
UPDATE tasks SET task_duration = AGE(end_time, start_time)  WHERE task_id = 1;