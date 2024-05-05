DROP TABLE IF EXISTS users;
CREATE TABLE Users ( 
    email VARCHAR(256),
    Userid Serial,
    Password VARCHAR(256),
    PRIMARY KEY (email)
    );

DROP TABLE IF EXISTS activities;
CREATE TABLE Activities(
    activity_id SERIAL,
    activity_name VARCHAR(100),
    Userid Integer,
    activity_details VARCHAR(500),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
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

INSERT INTO activities (activity_id, activity_name, userid, start_time, end_time) VALUES (0, 'Senior Projects', 1, '2024-04-08 15:40:00', '2024-04-08 17:40:00');
INSERT INTO activities (activity_id, activity_name, userid, start_time, end_time) VALUES (1, 'Databases', 1, '2024-04-08 15:40:00', '2024-04-08 17:40:00');
INSERT INTO activities (activity_id, activity_name, userid, start_time, end_time) VALUES (2, 'UI/UX', 1, '2024-04-08 15:40:00', '2024-04-08 17:40:00');

INSERT INTO tasks (task_id, userid, activity_id, task_name, task_details, task_duration, deadline, start_time, end_time) VALUES (1, 1, 0, 'Homework', 'Details of Task 1', NULL, NULL, '2024-04-08T15:40', '2024-04-08T17:00');
INSERT INTO tasks (task_id, userid, activity_id, task_name, task_details, task_duration, deadline, start_time, end_time) VALUES (2, 1, 1, 'Presentation', 'Details of Task 2', NULL, NULL, '2024-04-09T12:40', '2024-04-09T15:00');
INSERT INTO tasks (task_id, userid, activity_id, task_name, task_details, task_duration, deadline, start_time, end_time) VALUES (4, 1, 2, 'Homework', 'Details', NULL, NULL, '2024-04-09T12:40', '2024-04-09T15:00');
UPDATE tasks SET task_duration = AGE(end_time, start_time)  WHERE task_duration IS NULL;
UPDATE tasks SET deadline = end_time  WHERE deadline IS NULL;