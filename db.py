import sqlite3
import pandas as pd
import streamlit as st
import math

#таблица "subjects"
def create_table_subjects():
    conn = create_connection_all()
    cursor = conn.cursor()
    cursor.executescript('''
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT UNIQUE NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def save_subjects(subjects):
    conn = create_connection_all()
    cursor = conn.cursor()
    cursor.execute('DELETE from subjects')
    for index, row in subjects.iterrows():
        if not row['id'] or math.isnan(row['id']):
            if subjects['id'].max() and not math.isnan(subjects['id'].max()):
                row['id'] = subjects['id'].max() + 1
            else:
                row['id'] = 1
        cursor.execute('INSERT INTO subjects VALUES (?, ?)', row.tolist())
    st.success("Изменения успешно сохранены!")
    conn.commit()
    conn.close()

def get_all_subjects():
    conn = create_connection_all()
    query = f"SELECT * FROM subjects"
    subjects = pd.read_sql_query(query, conn)
    return subjects


#таблица "teachers"
def create_connection_all():
    conn = sqlite3.connect('database.db')
    return conn

def create_table_teachers():
    conn = create_connection_all()
    cursor = conn.cursor()
    cursor.executescript('''
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY,
        surname TEXT NOT NULL,
        name TEXT NOT NULL,
        lastname TEXT NOT NULL,
        email TEXT UNIQUE,
        phone VARCHAR(20) UNIQUE NOT NULL,
        img TEXT,
        UNIQUE (surname, name, lastname)
    )
    ''')
    conn.commit()
    conn.close()

def create_table_teachers_subjects():
    conn = create_connection_all()
    cursor = conn.cursor()
    cursor.executescript('''
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS teachers_subjects (
        id INTEGER PRIMARY KEY,
        id_teacher INTEGER,
        id_subject INTEGER,
        FOREIGN KEY (id_teacher) REFERENCES teachers(id) on delete cascade,
        FOREIGN KEY (id_subject) REFERENCES subjects(id) on delete cascade
    )
    ''')
    conn.commit()
    conn.close()

def save_teachers(teachers,files):
    conn = create_connection_all()
    cursor = conn.cursor()
    cursor.execute('DELETE from teachers')
    for index, row in teachers.iterrows():
        if not row['id'] or math.isnan(row['id']):
            if teachers['id'].max() and not math.isnan(teachers['id'].max()):
                row['id'] = teachers['id'].max()+1
            else:
                row['id'] = 1
        row_list = row.tolist()
        s_start = 'INSERT INTO teachers(id, surname, name, lastname, '
        s_end = f' VALUES ({row_list[0]}, "{row_list[1]}", "{row_list[2]}", "{row_list[3]}", '
        if row_list[0] in files.keys():
            s_start += 'img, '
            s_end += f'"{files[row_list[0]]}", '
        if row_list[4]:
            s_start += 'email, '
            s_end += f'"{row_list[4]}", '
        s_start += 'phone) '
        s_end += f'"{row_list[5]}")'
        s_start += s_end
        cursor.execute(s_start)
    st.success("Изменения успешно сохранены!")
    conn.commit()
    conn.close()

def save_img(teachers, teachers_subjects, docs):
    conn = create_connection_all()
    cursor = conn.cursor()
    cursor.execute('DELETE from teachers_subjects')
    if teachers_subjects['id'].max() and not math.isnan(teachers_subjects['id'].max()):
        k = teachers_subjects['id'].max()+1
    else:
        k=1
    for index, row in teachers_subjects.iterrows():
        if not row['id'] or math.isnan(row['id']):
            row['id'] = k
            k+=1
        row_list = row.tolist()
        query = f'SELECT id FROM subjects where subject = "{row_list[2]}"'
        id_subject = pd.read_sql_query(query, conn)['id']
        s_start = f'INSERT INTO teachers_subjects(id, id_teacher, id_subject) VALUES ({row_list[0]}, {row_list[1]}, {id_subject.tolist()[0]})'
        cursor.execute(s_start)
    for index, row in teachers.iterrows():
        if row["id"] in docs.keys():
            cursor.execute(f'UPDATE teachers SET img="{docs[row["id"]]}" WHERE id={row["id"]}')
    st.success("Изменения успешно сохранены!")
    conn.commit()
    conn.close()

def get_all_teachers():
    conn = create_connection_all()
    query = f'''SELECT * FROM teachers'''
    teachers = pd.read_sql_query(query, conn)
    query2 = f"SELECT teachers_subjects.id, id_teacher, subject FROM teachers_subjects left outer join subjects on teachers_subjects.id_subject=subjects.id"
    teachers_subjects = pd.read_sql_query(query2, conn)
    return teachers, teachers_subjects

def get_all_teachers_with_subjects():
    conn = create_connection_all()
    query = f'''SELECT surname, name, lastname, phone, subject, img, email FROM teachers
left outer join teachers_subjects on teachers_subjects.id_teacher=teachers.id
left outer join subjects on teachers_subjects.id_subject=subjects.id'''
    teachers = pd.read_sql_query(query, conn)
    query2 = f"SELECT teachers_subjects.id, id_teacher, subject FROM teachers_subjects left outer join subjects on teachers_subjects.id_subject=subjects.id"
    teachers_subjects = pd.read_sql_query(query2, conn)
    return teachers, teachers_subjects


#таблица "groups"

def create_table_classes():
    conn = create_connection_all()
    cursor = conn.cursor()
    cursor.executescript('''
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY,
        class TEXT NOT NULL UNIQUE
    )
    ''')
    conn.commit()
    conn.close()

def save_classes(classes):
    conn = create_connection_all()
    cursor = conn.cursor()
    cursor.execute('DELETE from classes')
    for index, row in classes.iterrows():
        if not row['id'] or math.isnan(row['id']):
            if classes['id'].max() and not math.isnan(classes['id'].max()):
                row['id'] = classes['id'].max() + 1
            else:
                row['id'] = 1
        cursor.execute('INSERT INTO classes VALUES (?, ?)', row.tolist())
    st.success("Изменения успешно сохранены!")
    conn.commit()
    conn.close()

def get_all_classes():
    conn = create_connection_all()
    query = f"SELECT * FROM classes"
    classes = pd.read_sql_query(query, conn)
    return classes


#таблица "subgroups"

def create_table_subgroups():
    conn = create_connection_all()
    cursor = conn.cursor()
    cursor.executescript('''
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS subgroups (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        id_class INTEGER NOT NULL,
        FOREIGN KEY (id_class) REFERENCES classes(id) on delete cascade,
        UNIQUE(name, id_class)
    )
    ''')
    conn.commit()
    conn.close()

def save_subgroups(subgroups):
    conn = create_connection_all()
    cursor = conn.cursor()
    cursor.execute('DELETE from subgroups')
    k=1
    for index, row in get_all_classes().iterrows():
        while k in subgroups['id'].tolist():
            k+=1
        row_list = row.tolist()
        s_start = f'INSERT INTO subgroups(id, name, id_class) VALUES ({k}, "_", {row_list[0]})'
        cursor.execute(s_start)
        k+=1
    for index, row in subgroups.iterrows():
        if not row['id'] or math.isnan(row['id']):
            query = f'''SELECT subgroups.id, name, classes.class FROM subgroups
            left outer join classes on subgroups.id_class = classes.id'''
            subgroups_df = pd.read_sql_query(query, conn)
            if subgroups_df['id'].max() and not math.isnan(subgroups_df['id'].max()):
                row['id'] = subgroups_df['id'].max()+1
            else:
                row['id'] = 1
        row_list = row.tolist()
        query = f'SELECT id FROM classes WHERE class="{row_list[2]}"'
        id_class = pd.read_sql_query(query, conn)['id']
        s_start = 'INSERT INTO subgroups(id, name'
        s_end = f' VALUES ({row_list[0]}, "{row_list[1]}"'
        if id_class.tolist()!=[]:
            s_start += ', id_class'
            s_end += f', {id_class.tolist()[0]}'
        s_start += ') '
        s_end += f')'
        s_start += s_end
        cursor.execute(s_start)
    st.success("Изменения успешно сохранены!")
    conn.commit()
    conn.close()

def get_all_subgroups():
    conn = create_connection_all()
    query = f'''SELECT subgroups.id, name, classes.class FROM subgroups
left outer join classes on subgroups.id_class = classes.id'''
    subgroups = pd.read_sql_query(query, conn)
    return subgroups



def create_table_lessons():
    conn = create_connection_all()
    cursor = conn.cursor()
    cursor.executescript('''
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day_of_week INTEGER NOT NULL,
        time INTEGER INTEGER NOT NULL,
        id_teacher_subject INTEGER NOT NULL,
        room TEXT NOT NULL,
        id_subgroup INTEGER NOT NULL,
        FOREIGN KEY (id_teacher_subject) REFERENCES teachers_subjects(id) on delete cascade,
        FOREIGN KEY (id_subgroup) REFERENCES subgroups(id) on delete cascade,
        UNIQUE (day_of_week, id_teacher_subject, time)
    )
    ''')
    conn.commit()
    conn.close()

def save_lessons(lessons):
    conn = create_connection_all()
    cursor = conn.cursor()
    cursor.execute('DELETE from lessons')
    for index, row in lessons.iterrows():
        row_list = row.tolist()
        query = f'SELECT id FROM classes WHERE class="{row_list[7]}"'
        id_class = pd.read_sql_query(query, conn)['id']
        query = f'SELECT id FROM subgroups WHERE id_class={id_class.tolist()[0]} and name = "{row_list[8]}"'
        id_subgroup = pd.read_sql_query(query, conn)['id']
        query = f'SELECT id FROM subjects WHERE subject="{row_list[2]}"'
        id_subject = pd.read_sql_query(query, conn)['id']
        query = f'SELECT id FROM teachers WHERE surname="{row_list[3]}" and name="{row_list[4]}" and lastname="{row_list[5]}"'
        id_teacher = pd.read_sql_query(query, conn)['id']
        query = f'SELECT id FROM teachers_subjects WHERE id_teacher={id_teacher.tolist()[0]} and id_subject={id_subject.tolist()[0]}'
        id_teacher_subject = pd.read_sql_query(query, conn)['id']
        s_start = 'INSERT INTO lessons(day_of_week, time, room, id_teacher_subject'
        s_end = f' VALUES ({row_list[0]}, "{row_list[1]}", "{row_list[6]}", {id_teacher_subject.tolist()[0]}'
        s_start += ', id_subgroup'
        s_end += f', {id_subgroup.tolist()[0]}'
        s_start += ') '
        s_end += f')'
        s_start += s_end
        cursor.execute(s_start)
    st.success("Изменения успешно сохранены!")
    conn.commit()
    conn.close()

def get_all_lessons():
    conn = create_connection_all()
    query = f'''SELECT lessons.id, day_of_week, time, subjects.subject, teachers.surname, teachers.name,
teachers.lastname, teachers.phone, room, subgroups.name as subgroup, classes.class FROM lessons
left outer join teachers_subjects on lessons.id_teacher_subject = teachers_subjects.id
left outer join subjects on teachers_subjects.id_subject = subjects.id
left outer join teachers on teachers_subjects.id_teacher = teachers.id
left outer join subgroups on lessons.id_subgroup = subgroups.id
left outer join classes on subgroups.id_class = classes.id'''
    lessons = pd.read_sql_query(query, conn)
    return lessons




