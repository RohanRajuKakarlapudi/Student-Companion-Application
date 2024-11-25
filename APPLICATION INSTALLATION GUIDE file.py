import sqlite3

print('____________________________________________________________________________________________________________________________________________________')



mycon = sqlite3.connect('myfirst.db')
# Please open command prompt from the START by entering cmd
# STEP 1 Please pip install the following commands in the command prompt
'''
pip install webbrowser
pip install pygame
pip install moviepy
pip install time
pip install PIL
pip install pandas
pip install pyttsx3

pip install pipwin
pipwin install pyaudio

pip install pyjokes
pip install SpeechRecognition
pip install pysimplegui
'''

# STEP 2 copy paste the following statement in sql, create database SCAPP_TRIAL
# STEP 3 once done open student companion app.py file and change the database name to SCAPP_TRIAL
# STEP 4 please sign up and enjoy the application features
# STEP 5 feel free to provide a feedback, this helps us improve the features of our app
# ENJOY !!!

mycursor=mycon.cursor() 
database='SCAPP_TRIAL'

try:
    mycursor.execute('create table contacts(NAME varchar(20),EMAIL varchar(20),PHONE int)')
    mycursor.execute('create table hyperlinks(SUBJECT varchar(20),LINK varchar(40))')
    mycursor.execute('create table healthy_choices(SL int,TIPS varchar(1000))')
    mycursor.execute('create table sign_up(NAME varchar(40),GRADE int,USERNAME varchar(40),PASSWORD varchar(40))')
    mycursor.execute('create table ClassTimeTable(DAY varchar(20),PERIOD_1 VARCHAR(20),PERIOD_2 VARCHAR(20),PERIOD_3 VARCHAR(20)) ')
    mycursor.execute('create table ToDoList(TASK text,DEADLINE_DAY VARCHAR(20),DEADLINE_TIME VARCHAR(90)) ')
    mycursor.execute('create table motivation(sl int,QUOTES text) ')

except:
    l=[(1,'Limit sugary drinks'),
       (2,'Eat nuts and seeds'),
       (3,'Avoid ultra-processed foods that contain additives like sugar, highly refined oil, salt and other artificial flavorings and preservatievs'),
       (4,'Dont fear coffee, coffee is loaded with rich antioxidants'),
       (5,'Eat fatty fish , a great source of imega-3 fatty acids')
       (6,'Choose whole grain bread instead of refined')
       (7,'Add Greek yogurt to your diet')
       (8,'Drink enough water')
       (9,'Bake or roast instead of grilling or frying')
       (10,'Take omega-3 and vitamin D supplements')]
       
    for x in range(10):
        query="insert into healthy_choices(SL, TIPS) VALUES (%s, %s )"
        val=l[x]
        mycursor.execute(query, val)
        mycon.commit()

    l2=[
        (1,'Push harder than yesterday if you want a different tomorrow'),
        (2,"Nothing is impossible. The word itself says I'm possible"),
        (3,'The best view comes after the hardest climb'),
        (4,' Stay positive. Work hard. Make it happen'),
        (5,' Give your stress Wings and let it fly away'),
        (6,'Inhale confidence, exhale doubt'),
        (7,'To be the best, you must handle the worst'),
        (8,' Life is a journey, not a race'),
        (9,'All progress takes place outside the comfort zone'),
        (10,'No masterpiece was ever created by a lazy artist')
        ]    
    for y in range(10):
        que='insert into motivation(sl, QUOTES) values (%s, %s)'
        vl=l2[y]
        mycursor.execute(que,vl)
        mycon.commit()    
        
    
'''
SQL QUERIES

create database SCAPP_TRIAL;
use SCAPP;

create table contacts(NAME varchar(20),EMAIL varchar(20),PHONE int);
create table hyperlinks(SUBJECT varchar(20),LINK varchar(40));
create table healthy_choices(SL int,TIPS varchar(1000));
create table sign_up(NAME varchar(40),GRADE int,USERNAME varchar(40),PASSWORD varchar(40));
create table ClassTimeTable(DAY varchar(20),PERIOD_1 VARCHAR(20),PERIOD_2 VARCHAR(20),PERIOD_3 VARCHAR(20));
create table ToDoList(TASK text,DEADLINE_DAY VARCHAR(20),DEADLINE_TIME VARCHAR(90));
create table motivation(sl int,QUOTES text);

insert into healthy_choices values(1,'Limit sugary drinks');
insert into healthy_choices values(2,'Eat nuts and seeds');
insert into healthy_choices values(3,'Avoid ultra-processed foods that contain additives like sugar, highly refined oil, salt and other artificial flavorings and preservatievs');
insert into healthy_choices values(4,'Don’t fear coffee, coffee is loaded with rich antioxidants');
insert into healthy_choices values(5,'Eat fatty fish , a great source of imega-3 fatty acids');
insert into healthy_choices values(6,'Choose whole grain bread instead of refined');
insert into healthy_choices values(7,'Add Greek yogurt to your diet');
insert into healthy_choices values(8,'Drink enough water');
insert into healthy_choices values(9,'Bake or roast instead of grilling or frying');
insert into healthy_choices values(10,'Take omega-3 and vitamin D supplements');

insert into motivation values(1,'Push harder than yesterday if you want a different tomorrow');
insert into motivation values(2,'Nothing is impossible. The word itself says 'I'm possible'');
insert into motivation values(3,'The best view comes after the hardest climb');
insert into motivation values(4,' Stay positive. Work hard. Make it happen');
insert into motivation values(5,' Give your stress Wings and let it fly away');
insert into motivation values(6,'Inhale confidence, exhale doubt');
insert into motivation values(7,'To be the best, you must handle the worst');
insert into motivation values(8,' Life is a journey, not a race');
insert into motivation values(9,'All progress takes place outside the comfort zone');
insert into motivation values(10,'No masterpiece was ever created by a lazy artist');
'''
