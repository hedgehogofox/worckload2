import streamlit as st
from db import *
import os
import pandas as pd
from streamlit_modal import Modal
from dateutil.relativedelta import relativedelta

def find_value (mas, a):
    k = 0
    if a!=[]:
        for i in range(len(mas)):
            if mas[i]==a[0]:
                k = i
                break
    return k

def admin():

    st.title("Вход в панель администратора")

    password = st.text_input("Введите пароль", type = "password", key = "1")
    
    if password != "1" and password !='':
        st.error("Неверный пароль!")
    elif password == "1":
        st.success("Вход выполнен!")

        tables = ["Предметы", "Учителя", "Классы", "Подгруппы", "Уроки"]
        choice_tables = st.radio("Выберите таблицу", tables, index=None)

        if choice_tables == "Предметы":
            subjects = get_all_subjects()
            subjects_edit = st.data_editor(subjects, num_rows = "dynamic", column_order=("subject",),
                                           column_config = {"subject": st.column_config.TextColumn("Предмет", required = True)})
            save = st.button('Сохранить изменения')
            if save:
                save_subjects(subjects_edit)


        
        if choice_tables == "Учителя":
            teachers, teachers_subjects_df = get_all_teachers()
            teachers_subjects = {}
            files={}
            for index, row in teachers.iterrows():
                files[row['id']]=row['img']
            subjects = get_all_subjects()
            teachers_edit = st.data_editor(teachers, num_rows = "dynamic", column_order=("surname", "name", "lastname", "email", "phone"),
                                           column_config = {"surname": st.column_config.TextColumn("Фамилия", required = True),
                                                            "name": st.column_config.TextColumn("Имя", required = True),
                                                            "lastname": st.column_config.TextColumn("Отчество"),
                                                            "email": st.column_config.TextColumn("Электронная почта", validate="^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$", required = True),
                                                            "phone": st.column_config.TextColumn("Номер телефона", validate="(?:\+|\d)[\d\-\(\) ]{9,}\d", required = True),
                                                            })
            save = st.button('Сохранить изменения')
            if save:
                teachers_edit['lastname'] = teachers_edit['lastname'].fillna('')
                save_teachers(teachers_edit, files)
            
            df, _ = get_all_teachers()

            col2, col3, col4, col5, col6, col7 = st.columns([5, 5, 5, 10, 10, 10])
            with col2:
                st.write("Фамилия")
            with col3:
                st.write("Имя")
            with col4:
                st.write("Отчество")
            with col5:
                st.write("Предметы")
            with col6:
                st.write("Файл с фото")
            with col7:
                st.write("Предпросмотр фото")
            
            docs = {}
            for index, row in df.iterrows():
                docs[row['id']]=row['img']
            for index, row in df.iterrows():
                col2, col3, col4, col5, col6, col7 = st.columns([5, 5, 5, 10, 10, 10])
                with col2:
                    st.write(row['surname'])
                with col3:
                    st.write(row['name'])
                with col4:
                    st.write(row['lastname'])
                with col5:
                    if not teachers_subjects_df[teachers_subjects_df.id_teacher==row['id']].empty:
                        part_df=teachers_subjects_df[teachers_subjects_df.id_teacher==row['id']]
                        subs = st.multiselect('', subjects['subject'].tolist(), part_df['subject'].tolist(), key = f'sub{row["id"]}' )
                        for sub in part_df['subject'].tolist():
                            if not sub in subs:
                                teachers_subjects_df = teachers_subjects_df[~((teachers_subjects_df.id_teacher==row['id']) & (teachers_subjects_df.subject==sub))]
                        for sub in subs:
                            if not sub in part_df['subject'].tolist():
                                teachers_subjects_df.loc[len(teachers_subjects_df)] = [None,row['id'],sub]
                    else:
                        subs = st.multiselect('', subjects['subject'].tolist(), key = f'sub{row["id"]}' )
                        for sub in subs:
                            teachers_subjects_df.loc[len(teachers_subjects_df)] = [None,row['id'],sub]
                with col6:
                    file=st.file_uploader("Выберите файл", type = ['jpg', 'png'], key = f"button_{index}", label_visibility = "hidden")
                    if file:
                        with open(os.path.join("media", file.name), "wb") as f:
                            f.write(file.getbuffer())
                        docs[row['id']]=f"media\{file.name}"
                with col7:
                    if row['id'] in docs.keys() and docs[row['id']]!="None" and docs[row['id']]:
                        st.image(docs[row['id']].replace('\\', '/'), use_column_width="always")

            save = st.button('Сохранить фото')
            if save:
                
                save_img(df, teachers_subjects_df, docs)

        if choice_tables == "Классы":
            classes = get_all_classes()
            classes_edit = st.data_editor(classes, num_rows = "dynamic", column_order=("class",),
                                           column_config = {"class": st.column_config.TextColumn("Класс", required = True)
                                                            })
            save = st.button('Сохранить изменения')
            if save:
                save_classes(classes_edit)

        if choice_tables == "Подгруппы":
            subgroups = get_all_subgroups()
            classes = get_all_classes()
            subgroups_edit = st.data_editor(subgroups, num_rows = "dynamic", column_order=("name", "class"),
                                           column_config = {"name": st.column_config.TextColumn("Подгруппа", required = True),
                                                            "class": st.column_config.SelectboxColumn("Класс", required = True, options=classes['class'].tolist()),
                                                            })
            save = st.button('Сохранить изменения')
            if save:
                subgroups_edit=subgroups_edit[subgroups_edit.name!='_']
                save_subgroups(subgroups_edit)


        #таблица "Песни"
        if choice_tables == "Уроки":
            if 'select_teacher' not in st.session_state:
                st.session_state['select_teacher'] = ''
            lessons = get_all_lessons()
            lessons['ФИО'] = lessons[['surname', 'name', 'lastname']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
            lessons['subgroup_class'] = lessons[['subgroup', 'class']].apply(lambda row: ' / '.join(row.values.astype(str)), axis=1)
            teachers, _ = get_all_teachers_with_subjects()
            teachers['ФИО'] = teachers[['surname', 'name', 'lastname']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
            select_teacher = st.selectbox('', teachers['ФИО'].unique().tolist(), label_visibility="hidden")
            
            if select_teacher!='':
                teacher_subjects = teachers[teachers['ФИО']==select_teacher]
                subjects = teacher_subjects['subject']
                subgroups = get_all_subgroups()
                subgroups['subgroup_class'] = subgroups[['name', 'class']].apply(lambda row: ' / '.join(row.values.astype(str)), axis=1)
                col1, col2, col3, col4, col5, col6, col7 = st.columns([5, 5, 5, 5, 5, 5, 5])  # Adjust column widths as needed
                with col1:
                    st.write("Время")
                with col2:
                    st.write("Понедельник")
                with col3:
                    st.write("Вторник")
                with col4:
                    st.write("Среда")  
                with col5:
                    st.write("Четверг")  # Header for the button column
                with col6:
                    st.write("Пятница")
                with col7:
                    st.write("Суббота")
                time = {0: '8:00 - 8:40', 1: '8:50 - 9:30', 2: '9:40 - 10:20', 3: '10:35 - 11:15',
                        4: '11:30 - 12:10', 5: '12:20 - 13:00', 6: '13:10 - 13:50', 7: '14:10 - 14:50',
                        8: '15:00 - 15:40', 9: ' 15:50 - 16:30', 10: '16:40 - 17:20', 11: '17:30 - 18:10',
                        12: '18:20 - 19:00', 13: '19:10 - 19:50'}

                new_df = pd.DataFrame(columns = lessons.columns)

                for i in range(14):
                    st.divider()
                    col1, col2, col3, col4, col5, col6, col7 = st.columns([5, 5, 5, 5, 5, 5, 5], vertical_alignment='center')
                    with col1:
                        st.write(time[i])
                    with col2:
                        this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==1) & (lessons['ФИО']==select_teacher)]
                        subject = st.selectbox('Предмет:',
                                               ['']+subjects.tolist(),
                                               index = find_value(['']+subjects.tolist(), this_lesson['subject'].tolist()),
                                               key = f'1{i}')
                        if this_lesson['room'].tolist()!=[]:
                            room = st.text_input('Кабинет:',
                                                 value = this_lesson['room'].tolist()[0],
                                                 key = f'r1{i}')
                        else:
                            room = st.text_input('Кабинет:',
                                                 key = f'r1{i}')
                        busy_df = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==1)]
                        busy_classes = busy_df['class'].tolist()
                        for j in range(len(busy_classes)):
                            busy_classes[j] = '_ / ' + busy_classes[j]
                        busy_subgroups = busy_df['subgroup_class'].tolist()
                        empty_subgroups = list(set(subgroups['subgroup_class'].tolist())-set(busy_subgroups) - set(busy_classes))
                        empty = ['']+empty_subgroups
                        empty += this_lesson['subgroup_class'].tolist()
                        group = st.selectbox('Класс:',
                                                 empty,
                                                 index = find_value(empty, this_lesson['subgroup_class'].tolist()), key = f'g1{i}')
                        if subject!='' and room and group!='':
                            new_df.loc[len(new_df)]={'time':i+1, 'day_of_week':1, 'surname':select_teacher.split(' ')[0],
                                                         'name':select_teacher.split(' ')[1], 'lastname':select_teacher.split(' ')[2], 'room':room, 'subject':subject,
                                                         'class':group.split(' / ')[1], 'subgroup':group.split(' / ')[0]}
                    with col3:
                        this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==2) & (lessons['ФИО']==select_teacher)]
                        subject = st.selectbox('Предмет:',
                                               ['']+subjects.tolist(),
                                               index = find_value(['']+subjects.tolist(), this_lesson['subject'].tolist()),
                                               key = f'2{i}')
                        if this_lesson['room'].tolist()!=[]:
                            room = st.text_input('Кабинет:',
                                                 value = this_lesson['room'].tolist()[0],
                                                 key = f'r2{i}')
                        else:
                            room = st.text_input('Кабинет:',
                                                 key = f'r2{i}')
                        busy_df = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==2)]
                        busy_classes = busy_df['class'].tolist()
                        for j in range(len(busy_classes)):
                            busy_classes[j] = '_ / ' + busy_classes[j]
                        busy_subgroups = busy_df['subgroup_class'].tolist()
                        empty_subgroups = list(set(subgroups['subgroup_class'].tolist())-set(busy_subgroups) - set(busy_classes))
                        empty = ['']+empty_subgroups
                        empty += this_lesson['subgroup_class'].tolist()
                        group = st.selectbox('Класс:',
                                                 empty,
                                                 index = find_value(empty, this_lesson['subgroup_class'].tolist()), key = f'g2{i}')
                        if subject!='' and room and group!='':
                            new_df.loc[len(new_df)]={'time':i+1, 'day_of_week':2, 'surname':select_teacher.split(' ')[0],
                                                         'name':select_teacher.split(' ')[1], 'lastname':select_teacher.split(' ')[2], 'room':room, 'subject':subject,
                                                         'class':group.split(' / ')[1], 'subgroup':group.split(' / ')[0]}
                    with col4:
                        this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==3) & (lessons['ФИО']==select_teacher)]
                        subject = st.selectbox('Предмет:',
                                               ['']+subjects.tolist(),
                                               index = find_value(['']+subjects.tolist(), this_lesson['subject'].tolist()),
                                               key = f'3{i}')
                        if this_lesson['room'].tolist()!=[]:
                            room = st.text_input('Кабинет:',
                                                 value = this_lesson['room'].tolist()[0],
                                                 key = f'r3{i}')
                        else:
                            room = st.text_input('Кабинет:',
                                                 key = f'r3{i}')
                        busy_df = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==3)]
                        busy_classes = busy_df['class'].tolist()
                        for j in range(len(busy_classes)):
                            busy_classes[j] = '_ / ' + busy_classes[j]
                        busy_subgroups = busy_df['subgroup_class'].tolist()
                        empty_subgroups = list(set(subgroups['subgroup_class'].tolist())-set(busy_subgroups) - set(busy_classes))
                        empty = ['']+empty_subgroups
                        empty += this_lesson['subgroup_class'].tolist()
                        group = st.selectbox('Класс:',
                                                 empty,
                                                 index = find_value(empty, this_lesson['subgroup_class'].tolist()), key = f'g3{i}')
                        if subject!='' and room and group!='':
                            new_df.loc[len(new_df)]={'time':i+1, 'day_of_week':3, 'surname':select_teacher.split(' ')[0],
                                                         'name':select_teacher.split(' ')[1], 'lastname':select_teacher.split(' ')[2], 'room':room, 'subject':subject,
                                                         'class':group.split(' / ')[1], 'subgroup':group.split(' / ')[0]}
                    with col5:
                        this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==4) & (lessons['ФИО']==select_teacher)]
                        subject = st.selectbox('Предмет:',
                                               ['']+subjects.tolist(),
                                               index = find_value(['']+subjects.tolist(), this_lesson['subject'].tolist()),
                                               key = f'4{i}')
                        if this_lesson['room'].tolist()!=[]:
                            room = st.text_input('Кабинет:',
                                                 value = this_lesson['room'].tolist()[0],
                                                 key = f'r4{i}')
                        else:
                            room = st.text_input('Кабинет:',
                                                 key = f'r4{i}')
                        busy_df = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==4)]
                        busy_classes = busy_df['class'].tolist()
                        for j in range(len(busy_classes)):
                            busy_classes[j] = '_ / ' + busy_classes[j]
                        busy_subgroups = busy_df['subgroup_class'].tolist()
                        empty_subgroups = list(set(subgroups['subgroup_class'].tolist())-set(busy_subgroups) - set(busy_classes))
                        empty = ['']+empty_subgroups
                        empty += this_lesson['subgroup_class'].tolist()
                        group = st.selectbox('Класс:',
                                                 empty,
                                                 index = find_value(empty, this_lesson['subgroup_class'].tolist()), key = f'g4{i}')
                        if subject!='' and room and group!='':
                            new_df.loc[len(new_df)]={'time':i+1, 'day_of_week':4, 'surname':select_teacher.split(' ')[0],
                                                         'name':select_teacher.split(' ')[1], 'lastname':select_teacher.split(' ')[2], 'room':room, 'subject':subject,
                                                         'class':group.split(' / ')[1], 'subgroup':group.split(' / ')[0]}
                    with col6:
                        this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==5) & (lessons['ФИО']==select_teacher)]
                        subject = st.selectbox('Предмет:',
                                               ['']+subjects.tolist(),
                                               index = find_value(['']+subjects.tolist(), this_lesson['subject'].tolist()),
                                               key = f'5{i}')
                        if this_lesson['room'].tolist()!=[]:
                            room = st.text_input('Кабинет:',
                                                 value = this_lesson['room'].tolist()[0],
                                                 key = f'r5{i}')
                        else:
                            room = st.text_input('Кабинет:',
                                                 key = f'r5{i}')
                        busy_df = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==5)]
                        busy_classes = busy_df['class'].tolist()
                        for j in range(len(busy_classes)):
                            busy_classes[j] = '_ / ' + busy_classes[j]
                        busy_subgroups = busy_df['subgroup_class'].tolist()
                        empty_subgroups = list(set(subgroups['subgroup_class'].tolist())-set(busy_subgroups) - set(busy_classes))
                        empty = ['']+empty_subgroups
                        empty += this_lesson['subgroup_class'].tolist()
                        group = st.selectbox('Класс:',
                                                 empty,
                                                 index = find_value(empty, this_lesson['subgroup_class'].tolist()), key = f'g5{i}')
                        if subject!='' and room and group!='':
                            new_df.loc[len(new_df)]={'time':i+1, 'day_of_week':5, 'surname':select_teacher.split(' ')[0],
                                                         'name':select_teacher.split(' ')[1], 'lastname':select_teacher.split(' ')[2], 'room':room, 'subject':subject,
                                                         'class':group.split(' / ')[1], 'subgroup':group.split(' / ')[0]}
                    with col7:
                        this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==6) & (lessons['ФИО']==select_teacher)]
                        subject = st.selectbox('Предмет:',
                                               ['']+subjects.tolist(),
                                               index = find_value(['']+subjects.tolist(), this_lesson['subject'].tolist()),
                                               key = f'6{i}')
                        if this_lesson['room'].tolist()!=[]:
                            room = st.text_input('Кабинет:',
                                                 value = this_lesson['room'].tolist()[0],
                                                 key = f'r6{i}')
                        else:
                            room = st.text_input('Кабинет:',
                                                 key = f'r6{i}')
                        busy_df = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==6)]
                        busy_classes = busy_df['class'].tolist()
                        for j in range(len(busy_classes)):
                            busy_classes[j] = '_ / ' + busy_classes[j]
                        busy_subgroups = busy_df['subgroup_class'].tolist()
                        empty_subgroups = list(set(subgroups['subgroup_class'].tolist())-set(busy_subgroups) - set(busy_classes))
                        empty = ['']+empty_subgroups
                        empty += this_lesson['subgroup_class'].tolist()
                        group = st.selectbox('Класс:',
                                                 empty,
                                                 index = find_value(empty, this_lesson['subgroup_class'].tolist()), key = f'g6{i}')
                        if subject!='' and room and group!='':
                            new_df.loc[len(new_df)]={'time':i+1, 'day_of_week':6, 'surname':select_teacher.split(' ')[0],
                                                         'name':select_teacher.split(' ')[1], 'lastname':select_teacher.split(' ')[2], 'room':room, 'subject':subject,
                                                         'class':group.split(' / ')[1], 'subgroup':group.split(' / ')[0]}
                    
            new_df = pd.concat([new_df, lessons.loc[lessons['ФИО']!=select_teacher]], ignore_index=True)
            save = st.button('Сохранить изменения')
            if save:
                #st.write(new_df)
                save_lessons(new_df[['day_of_week', 'time', 'subject', 'surname', 'name', 'lastname', 'room', 'class', 'subgroup']])

            count = st.button('Подсчетать количества уроков за некоторый период')
            modal = Modal(
                f"Подсчёт количества уроков за некоторый период для учителя {st.session_state['select_teacher']}:",
                key="demo-modal",
                padding=10,  # по умолчанию
                max_width=500  # по умолчанию
            )
            
            if count:
                st.session_state['select_teacher'] = select_teacher
                modal.open()

            if modal.is_open():
                with modal.container():
                    start = st.date_input('Дата начала периода')
                    end = st.date_input("Дата конца периода (невключительно)", value=start+relativedelta(days=+1), min_value=start+relativedelta(days=+1))
                    week = {0: 0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
                    i = start
                    while i!=end:
                        week[i.weekday()]+=1
                        i+=relativedelta(days=+1)
                    #st.write(week)
                    count_lessons = 0
                    for i in range (6):
                        this_day_of_week = lessons.loc[(lessons['day_of_week']==i+1) & (lessons['ФИО']==st.session_state['select_teacher'])]
                        count_lessons += len(this_day_of_week) * week[i]
                    result = st.button('Показать результат')
                    if result:
                        st.write ('Общее число уроков за заданный период:', count_lessons)

            
