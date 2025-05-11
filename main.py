import streamlit as st
from db import *
from admin import *
st.set_page_config(layout="wide")

create_table_subjects()
create_table_teachers()
create_table_teachers_subjects()
create_table_classes()
create_table_subgroups()
create_table_lessons()

with st.sidebar:
    st.title('Расписание под рукой')
    actions = st.radio(
        "Возможности:",
        ("Просмотр расписания",
         "Панель управления администратора"
        )
        )

    #admin_dashboard = st.button("Панель управления администратора", use_container_width = True, type = "primary")


if actions == "Панель управления администратора":
    admin()

if actions == "Просмотр расписания":

    lessons = get_all_lessons()
    lessons['ФИО'] = lessons[['surname', 'name', 'lastname']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    lessons['subgroup_class'] = lessons[['subgroup', 'class']].apply(lambda row: ' / '.join(row.values.astype(str)), axis=1)
    teachers, _ = get_all_teachers_with_subjects()
    teachers['ФИО'] = teachers[['surname', 'name', 'lastname']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    select_teacher = st.selectbox('Учителя:', ['']+teachers['ФИО'].unique().tolist())
    classes = get_all_classes()
    select_class = st.selectbox('Классы', ['']+classes['class'].tolist())
    if select_teacher!='' and select_class=='':
        this_teacher = teachers[teachers['ФИО']==select_teacher]
        st.image(this_teacher['img'].tolist()[0].replace('\', "/"), width=200)
        st.header(select_teacher)
        st.subheader('Телефон: '+this_teacher['phone'].tolist()[0])
        if this_teacher['email'].tolist()[0]:
            st.subheader('Электронная почта: '+this_teacher['email'].tolist()[0])
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
            
        for i in range(14):
            st.divider()
            col1, col2, col3, col4, col5, col6, col7 = st.columns([5, 5, 5, 5, 5, 5, 5], vertical_alignment='center')
            with col1:
                st.write(time[i])
            with col2:
                this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==1) & (lessons['ФИО']==select_teacher)]
                if not this_lesson.empty:
                    st.write(this_lesson['subject'].tolist()[0])
                    st.write('Кабинет: ', this_lesson['room'].tolist()[0])
                    if this_lesson['subgroup'].tolist()[0]!='_':
                        st.write(this_lesson['subgroup_class'].tolist()[0])
                    else:
                        st.write(this_lesson['class'].tolist()[0])
            with col3:
                this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==2) & (lessons['ФИО']==select_teacher)]
                if not this_lesson.empty:
                    st.write(this_lesson['subject'].tolist()[0])
                    st.write('Кабинет: ', this_lesson['room'].tolist()[0])
                    if this_lesson['subgroup'].tolist()[0]!='_':
                        st.write(this_lesson['subgroup_class'].tolist()[0])
                    else:
                        st.write(this_lesson['class'].tolist()[0])
            with col4:
                this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==3) & (lessons['ФИО']==select_teacher)]
                if not this_lesson.empty:
                    st.write(this_lesson['subject'].tolist()[0])
                    st.write('Кабинет: ', this_lesson['room'].tolist()[0])
                    if this_lesson['subgroup'].tolist()[0]!='_':
                        st.write(this_lesson['subgroup_class'].tolist()[0])
                    else:
                        st.write(this_lesson['class'].tolist()[0])
            with col5:
                this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==4) & (lessons['ФИО']==select_teacher)]
                if not this_lesson.empty:
                    st.write(this_lesson['subject'].tolist()[0])
                    st.write('Кабинет: ', this_lesson['room'].tolist()[0])
                    if this_lesson['subgroup'].tolist()[0]!='_':
                        st.write(this_lesson['subgroup_class'].tolist()[0])
                    else:
                        st.write(this_lesson['class'].tolist()[0])
            with col6:
                this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==5) & (lessons['ФИО']==select_teacher)]
                if not this_lesson.empty:
                    st.write(this_lesson['subject'].tolist()[0])
                    st.write('Кабинет: ', this_lesson['room'].tolist()[0])
                    if this_lesson['subgroup'].tolist()[0]!='_':
                        st.write(this_lesson['subgroup_class'].tolist()[0])
                    else:
                        st.write(this_lesson['class'].tolist()[0])
            with col7:
                this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==6) & (lessons['ФИО']==select_teacher)]
                if not this_lesson.empty:
                    st.write(this_lesson['subject'].tolist()[0])
                    st.write('Кабинет: ', this_lesson['room'].tolist()[0])
                    if this_lesson['subgroup'].tolist()[0]!='_':
                        st.write(this_lesson['subgroup_class'].tolist()[0])
                    else:
                        st.write(this_lesson['class'].tolist()[0])
                    
    elif select_class!='':
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
            
        for i in range(14):
            st.divider()
            col1, col2, col3, col4, col5, col6, col7 = st.columns([5, 5, 5, 5, 5, 5, 5], vertical_alignment='center')
            with col1:
                st.write(time[i])
            with col2:
                if select_teacher == '':
                    this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==1) & (lessons['class']==select_class)]
                else:
                    this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==1) & (lessons['class']==select_class) & (lessons['ФИО']==select_teacher)]
                if not this_lesson.empty:
                    k=0
                    for index, row in this_lesson.iterrows():
                        if k>0: st.divider()
                        st.write(row['subject'])
                        if select_teacher == '':
                            st.write(row['ФИО'])
                        st.write('Кабинет: ', row['room'])
                        if row['subgroup']!='_':
                            st.write('Подгруппа: ', row['subgroup'])
                        k+=1
            with col3:
                if select_teacher == '':
                    this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==2) & (lessons['class']==select_class)]
                else:
                    this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==2) & (lessons['class']==select_class) & (lessons['ФИО']==select_teacher)]
                if not this_lesson.empty:
                    k=0
                    for index, row in this_lesson.iterrows():
                        if k>0: st.divider()
                        st.write(row['subject'])
                        if select_teacher == '':
                            st.write(row['ФИО'])
                        st.write('Кабинет: ', row['room'])
                        if row['subgroup']!='_':
                            st.write('Подгруппа: ', row['subgroup'])
                        k+=1
            with col4:
                if select_teacher == '':
                    this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==3) & (lessons['class']==select_class)]
                else:
                    this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==3) & (lessons['class']==select_class) & (lessons['ФИО']==select_teacher)]
                if not this_lesson.empty:
                    k=0
                    for index, row in this_lesson.iterrows():
                        if k>0: st.divider()
                        st.write(row['subject'])
                        if select_teacher == '':
                            st.write(row['ФИО'])
                        st.write('Кабинет: ', row['room'])
                        if row['subgroup']!='_':
                            st.write('Подгруппа: ', row['subgroup'])
                        k+=1
            with col5:
                if select_teacher == '':
                    this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==4) & (lessons['class']==select_class)]
                else:
                    this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==4) & (lessons['class']==select_class) & (lessons['ФИО']==select_teacher)]
                if not this_lesson.empty:
                    k=0
                    for index, row in this_lesson.iterrows():
                        if k>0: st.divider()
                        st.write(row['subject'])
                        if select_teacher == '':
                            st.write(row['ФИО'])
                        st.write('Кабинет: ', row['room'])
                        if row['subgroup']!='_':
                            st.write('Подгруппа: ', row['subgroup'])
                        k+=1
            with col6:
                if select_teacher == '':
                    this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==5) & (lessons['class']==select_class)]
                else:
                    this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==5) & (lessons['class']==select_class) & (lessons['ФИО']==select_teacher)]
                if not this_lesson.empty:
                    k=0
                    for index, row in this_lesson.iterrows():
                        if k>0: st.divider()
                        st.write(row['subject'])
                        if select_teacher == '':
                            st.write(row['ФИО'])
                        st.write('Кабинет: ', row['room'])
                        if row['subgroup']!='_':
                            st.write('Подгруппа: ', row['subgroup'])
                        k+=1
            with col7:
                if select_teacher == '':
                    this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==6) & (lessons['class']==select_class)]
                else:
                    this_lesson = lessons.loc[(lessons['time']==i+1) & (lessons['day_of_week']==6) & (lessons['class']==select_class) & (lessons['ФИО']==select_teacher)]
                if not this_lesson.empty:
                    k=0
                    for index, row in this_lesson.iterrows():
                        if k>0: st.divider()
                        st.write(row['subject'])
                        if select_teacher == '':
                            st.write(row['ФИО'])
                        st.write('Кабинет: ', row['room'])
                        if row['subgroup']!='_':
                            st.write('Подгруппа: ', row['subgroup'])
                        k+=1

