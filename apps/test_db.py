import dbconnect as db

def adduserstable():
    sqlcode = """CREATE TABLE users (
        user_id serial primary key not null,
        user_name varchar(32) unique,
        user_password varchar(64) not null,
        user_modified_on timestamp without time zone default now(),
        user_delete_ind bool default false
    )"""
    db.modifydatabase(sqlcode, [])


def addmembersex():
    sqlcode = """ INSERT INTO member_sex (
    sex_name
    )
    VALUES (%s)"""
    db.modifydatabase(sqlcode, ['Male'])
    db.modifydatabase(sqlcode, ['Female'])

def addcivilstatus():
    sqlcode = """ INSERT INTO civilstatus (
    civil_status
    )
    VALUES (%s)"""
    db.modifydatabase(sqlcode, ['Single'])
    db.modifydatabase(sqlcode, ['Married'])
    db.modifydatabase(sqlcode, ['Separated'])
    db.modifydatabase(sqlcode, ['Widowed'])

def addmembershiptype():
    sqlcode = """ INSERT INTO membershiptype (
    membership
    )
    VALUES (%s)"""
    db.modifydatabase(sqlcode, ['Member'])
    db.modifydatabase(sqlcode, ['Walk-in'])


def addinstructorstable():
    sqlcode = """CREATE TABLE instructors (
        instructor_id SERIAL PRIMARY KEY,
        instructorfname VARCHAR(64) NOT NULL,
        instructorlname VARCHAR(64) NOT NULL,
        instructor_address VARCHAR(64) NOT NULL,
        instructor_contactnumber VARCHAR(64) NOT NULL,
        instructor_birthdate DATE NOT NULL,
        instructor_email VARCHAR(64) NOT NULL,
        sex_id INT,
        FOREIGN KEY (sex_id) REFERENCES member_sex(sex_id),
        class_id INT,
        class_schedule VARCHAR(64),
        added_by_user_id INT,
        FOREIGN KEY (class_id) REFERENCES class_info(class_id),
        FOREIGN KEY (added_by_user_id) REFERENCES users(user_id)
    )"""
    db.modifydatabase(sqlcode, [])

def addinstructor_classtable():
    sqlcode = """ CREATE TABLE instructor_class (
    instructor_id INT,
    class_id INT,
    PRIMARY KEY (instructor_id, class_id),
    FOREIGN KEY (instructor_id) REFERENCES instructor_info (instructor_id),
    FOREIGN KEY (class_id) REFERENCES class_info (class_id)
)"""
    db.modifydatabase(sqlcode, [])

print('done')

