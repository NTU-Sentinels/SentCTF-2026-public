CREATE TABLE users(

id INT AUTO_INCREMENT PRIMARY KEY,

username VARCHAR(50),

password VARCHAR(50)

);

INSERT INTO users(username,password)

VALUES

('CCDSadmin','CCDSStaff1234!'),

('thanos','Password123');



CREATE TABLE employees(

id INT AUTO_INCREMENT PRIMARY KEY,

name VARCHAR(100),

department VARCHAR(100),

email VARCHAR(100)

);

INSERT INTO employees(name,department,email)

VALUES

('John Tan','Computer Science','john.tan@ntu.edu.sg'),

('Sarah Lim','EEE','sarah.lim@ntu.edu.sg'),

('Daniel Lee','Finance','daniel.lee@ntu.edu.sg');



CREATE TABLE announcements(

id INT AUTO_INCREMENT PRIMARY KEY,

title VARCHAR(100),

body TEXT

);

INSERT INTO announcements(title,body)

VALUES

('Migration','Legacy portal scheduled for retirement.');



CREATE TABLE internal_notes(

id INT AUTO_INCREMENT PRIMARY KEY,

title VARCHAR(100),

note TEXT

);

INSERT INTO internal_notes(title,note)

VALUES

('Migration Notes','Remove old staff portal before December'),

('CTF Flag','sentCTF{replace_with_real_flag}');
