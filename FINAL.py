import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import pyttsx3
import pyjokes
import webbrowser  # chrome redirection
import time
import threading
import requests
from bs4 import BeautifulSoup
import random
import speech_recognition as sr



# Connect to SQLite Database
mycon = sqlite3.connect('myfirst.db')
mycursor = mycon.cursor()

# Text to speech function
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to tell a joke
def tell_joke():
    joke = pyjokes.get_joke()
    messagebox.showinfo("Joke", joke)
    speak(joke)

def app_main_menu():
    app_root = tk.Tk()
    app_root.title("Main Application - Student Companion")

    tk.Label(app_root, text="Welcome to Student Companion Application", font=('Helvetica', 16, 'bold')).pack(pady=20)

    # Define functions for each option
    def school_work():
        def school_work_menu():
            school_root = tk.Tk()
            school_root.title("School Work - Student Companion")

            def go_back():
                school_root.destroy()
                app_main_menu()

            def manage_timetable():
                timetable_root = tk.Tk()
                timetable_root.title("Manage Time Table")

                # Function to display the current time table
                def display_timetable():
                    display = tk.Toplevel(timetable_root)
                    display.title("Current Time Table")

                    # Define Treeview columns
                    columns = ('day', 'period_1', 'period_2', 'period_3')
                    timetable_tree = ttk.Treeview(display, columns=columns, show='headings')

                    # Define headings
                    timetable_tree.heading('day', text='Day')
                    timetable_tree.heading('period_1', text='Period 1')
                    timetable_tree.heading('period_2', text='Period 2')
                    timetable_tree.heading('period_3', text='Period 3')

                    # Format columns
                    timetable_tree.column('day', width=80)
                    timetable_tree.column('period_1', anchor='center', width=80)
                    timetable_tree.column('period_2', anchor='center', width=80)
                    timetable_tree.column('period_3', anchor='center', width=80)

                    # Insert data into the Treeview
                    try:
                        mycursor.execute("select * from classtimetable" + Username_i)
                        for row in mycursor.fetchall():
                            timetable_tree.insert('', tk.END, values=row)
                    except Exception as e:
                        messagebox.showerror("Error", "Failed to retrieve timetable: " + str(e))

                    timetable_tree.pack(side='top', fill='x')

                    scrollbar = ttk.Scrollbar(display, orient=tk.VERTICAL, command=timetable_tree.yview)
                    timetable_tree.configure(yscroll=scrollbar.set)
                    scrollbar.pack(side='right', fill='y')


                # Function to add a new timetable entry
                def add_timetable_entry():
                    add_window = tk.Toplevel(timetable_root)
                    add_window.title("Add/Update Timetable")

                    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
                    entries = {}

                    for i, day in enumerate(days):
                        tk.Label(add_window, text=f"{day}").grid(row=i, column=0, sticky='e')

                        for j in range(1, 4):
                            period_label = f"Period {j}:"
                            tk.Label(add_window, text=period_label).grid(row=i, column=(2 * j - 1), sticky='e')
                            entry = tk.Entry(add_window, width=20)
                            entry.grid(row=i, column=2 * j)
                            if day not in entries:
                                entries[day] = []
                            entries[day].append(entry)

                    def submit_all():
                        try:
                            mycursor.execute(f"DELETE FROM classtimetable{Username_i} WHERE DAY IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')")
                            for day, period_entries in entries.items():
                                periods = [entry.get() for entry in period_entries]
                                mycursor.execute(f"INSERT INTO classtimetable" + Username_i +"  (DAY, PERIOD_1, PERIOD_2, PERIOD_3) VALUES (?, ?, ?, ?)", 
                                                 (day, periods[0], periods[1], periods[2]))
                            mycon.commit()
                            messagebox.showinfo("Success", "Timetable updated successfully!")
                        except Exception as e:
                            messagebox.showerror("Error", "Failed to update timetable: " + str(e))
                        add_window.destroy()

                    tk.Button(add_window, text="Submit All", command=submit_all).grid(row=6, columnspan=6)

                # Function to delete the entire timetable
                def delete_timetable():
                    if messagebox.askyesno("Confirm", "Are you sure you want to delete the entire timetable?"):
                        try:
                            mycursor.execute("DELETE FROM classtimetable" + Username_i)
                            mycon.commit()
                            messagebox.showinfo("Success", "Timetable deleted successfully!")
                        except Exception as e:
                            messagebox.showerror("Error", "Failed to delete timetable: " + str(e))

                tk.Button(timetable_root, text="Display Time Table", command=display_timetable).pack(fill='x')
                tk.Button(timetable_root, text="Add Time Table Entry", command=add_timetable_entry).pack(fill='x')
                tk.Button(timetable_root, text="Delete Time Table", command=delete_timetable).pack(fill='x')
                tk.Button(timetable_root, text="Back", command=timetable_root.destroy).pack(fill='x')

                timetable_root.mainloop()


            def manage_todo_list():
                # check if the generation of multipele unique tables is happening and
                # generate all the features
                # fix the ai delay voice and make it come before all of the display or if possible do simultanously
                todo_root = tk.Tk()
                todo_root.title("Manage To-Do List")

                # Function to display the current to-do list
                def display_todo_list():
                    display = tk.Toplevel(todo_root)
                    display.title("Current To-Do List")
                    columns = ('sl', 'task', 'deadline_day', 'deadline_time')
                    todo_tree = ttk.Treeview(display, columns=columns, show='headings')
                    
                    # Define headings
                    for col in columns:
                        todo_tree.heading(col, text=col.capitalize().replace("_", " "))
                        todo_tree.column(col, anchor='center')

                    # Insert data into the Treeview
                    try:
                        mycursor.execute("SELECT * FROM ToDoList" + Username_i+ " ORDER BY DEADLINE_DAY, DEADLINE_TIME")
                        for row in mycursor.fetchall():
                            todo_tree.insert('', tk.END, values=row)
                    except Exception as e:
                        messagebox.showerror("Error", "Failed to retrieve to-do list: " + str(e))

                    todo_tree.pack(side='top', fill='both', expand=True)

                # Function to add a new task
                def add_task():
                    add_window = tk.Toplevel(todo_root)
                    add_window.title("Add New Task")

                    tk.Label(add_window, text="Task:").grid(row=0, column=0)
                    task_entry = tk.Entry(add_window, width=50)
                    task_entry.grid(row=0, column=1)

                    tk.Label(add_window, text="Deadline Day:").grid(row=1, column=0)
                    d_day_entry = tk.Entry(add_window, width=50)
                    d_day_entry.grid(row=1, column=1)

                    tk.Label(add_window, text="Deadline Time:").grid(row=2, column=0)
                    d_time_entry = tk.Entry(add_window, width=50)
                    d_time_entry.grid(row=2, column=1)

                    def submit_task():
                        task = task_entry.get()
                        d_day = d_day_entry.get()
                        d_time = d_time_entry.get()
                        try:
                            # Fetch the highest serial number from the ToDoList and increment by 1
                            mycursor.execute("SELECT COALESCE(MAX(SL), 0) FROM ToDoList"+Username_i)
                            max_sl = mycursor.fetchone()[0]
                            sl = max_sl + 1

                            # Insert the new task with the calculated serial number
                            mycursor.execute("INSERT INTO ToDoList" + Username_i +" (SL, TASK, DEADLINE_DAY, DEADLINE_TIME) VALUES (?, ?, ?, ?)", (sl, task, d_day, d_time))
                            mycon.commit()
                            messagebox.showinfo("Success", "Task added successfully!")
                            add_window.destroy()
                            display_todo_list()  # Refresh the display to include the new task
                        except Exception as e:
                            messagebox.showerror("Error", "Failed to add task: " + str(e))


                    tk.Button(add_window, text="Submit", command=submit_task).grid(row=3, column=0, columnspan=2)

                # Function to delete a task
                def delete_task():
                    delete_window = tk.Toplevel(todo_root)
                    delete_window.title("Delete Task")

                    tk.Label(delete_window, text="Enter SL of Task to Delete:").grid(row=0, column=0)
                    sl_entry = tk.Entry(delete_window, width=50)
                    sl_entry.grid(row=0, column=1)

                    def submit_delete():
                        sl = sl_entry.get()
                        try:
                            mycursor.execute("DELETE FROM ToDoList" + Username_i +" WHERE SL = ?", (sl,))
                            mycon.commit()
                            messagebox.showinfo("Success", "Task deleted successfully!")
                            delete_window.destroy()
                            display_todo_list()
                        except Exception as e:
                            messagebox.showerror("Error", "Failed to delete task: " + str(e))

                    tk.Button(delete_window, text="Delete", command=submit_delete).grid(row=1, column=0, columnspan=2)

                # Function to delete the entire to-do list
                def delete_all_tasks():
                    if messagebox.askyesno("Confirm", "Are you sure you want to delete all tasks?"):
                        try:
                            mycursor.execute("DELETE FROM ToDoList" + Username_i)
                            mycon.commit()
                            messagebox.showinfo("Success", "All tasks deleted successfully!")
                            display_todo_list()
                        except Exception as e:
                            messagebox.showerror("Error", "Failed to delete tasks: " + str(e))

                tk.Button(todo_root, text="Display To-Do List", command=display_todo_list).pack(fill='x')
                tk.Button(todo_root, text="Add New Task", command=add_task).pack(fill='x')
                tk.Button(todo_root, text="Delete a Task", command=delete_task).pack(fill='x')
                tk.Button(todo_root, text="Delete All Tasks", command=delete_all_tasks).pack(fill='x')
                tk.Button(todo_root, text="Back", command=todo_root.destroy).pack(fill='x')

                todo_root.mainloop()


            def educational_information():
                education_root = tk.Tk()
                education_root.title("Educational Information - Student Companion")

                # Function to search and open links
                def search_links():
                    search_window = tk.Toplevel(education_root)
                    search_window.title("Search Links")

                    tk.Label(search_window, text="Enter the subject:").grid(row=0, column=0)
                    subject_entry = tk.Entry(search_window)
                    subject_entry.grid(row=0, column=1)

                    # Frame to contain clickable links
                    links_frame = tk.Frame(search_window)
                    links_frame.grid(row=2, column=0, columnspan=2)

                    def search():
                        subject = subject_entry.get()
                        # Clear all previous link labels
                        for widget in links_frame.winfo_children():
                            widget.destroy()
                        try:
                            mycursor.execute(f"SELECT * FROM hyperlinks{Username_i} WHERE SUBJECT=?", (subject,))
                            links = mycursor.fetchall()
                            for index, link in enumerate(links):
                                link_label = tk.Label(links_frame, text=f"{link[0]} LINK: {link[1]}", fg="blue", cursor="hand2")
                                link_label.grid(row=index, column=0, sticky='w')
                                link_label.bind("<Button-1>", lambda e, url=link[1]: webbrowser.open(url))
                        except Exception as e:
                            error_label = tk.Label(links_frame, text="Error retrieving links.")
                            error_label.grid(row=0, column=0)

                    tk.Button(search_window, text="Search", command=search).grid(row=1, column=0)


                # Function to add new links
                def add_links():
                    add_window = tk.Toplevel(education_root)
                    add_window.title("Add Links")

                    tk.Label(add_window, text="Enter the field/subject of study:").grid(row=0, column=0)
                    subject_entry = tk.Entry(add_window)
                    subject_entry.grid(row=0, column=1)

                    tk.Label(add_window, text="Paste the link here:").grid(row=1, column=0)
                    link_entry = tk.Entry(add_window, width=50)
                    link_entry.grid(row=1, column=1)

                    def add_link():
                        subject = subject_entry.get()
                        link = link_entry.get()
                        try:
                            mycursor.execute(f"INSERT INTO hyperlinks{Username_i} (SUBJECT, LINK) VALUES (?, ?)", (subject, link))
                            mycon.commit()
                            messagebox.showinfo("Success", "Link added successfully!")
                            add_window.destroy()
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to add link: {e}")

                    tk.Button(add_window, text="Add Link", command=add_link).grid(row=2, column=0, columnspan=2)

                tk.Button(education_root, text="Search/Redirect Existing Links", command=search_links).pack(fill='x')
                tk.Button(education_root, text="Add New Links", command=add_links).pack(fill='x')
                tk.Button(education_root, text="Back", command=education_root.destroy).pack(fill='x')

                education_root.mainloop()


            def pomodoro_study_session():
                pomodoro_root = tk.Tk()
                pomodoro_root.title("Pomodoro Study Session")

                # Label to display the timer
                timer_label = tk.Label(pomodoro_root, text="25:00", font=("Helvetica", 48), fg="blue")
                timer_label.pack(pady=20)

                def countdown(count, mode="work"):
                    # Display the timer in MM:SS format
                    timer_label['text'] = f"{count // 60:02d}:{count % 60:02d}"
                    if count > 0:
                        # Call countdown again after 1 second
                        pomodoro_root.after(1000, countdown, count - 1, mode)
                    else:
                        # When countdown finishes, show a message
                        if mode == "work":
                            messagebox.showinfo("Time's up!", "Take a 5-minute break!")
                            start_break()  # Automatically start the break
                        else:
                            messagebox.showinfo("Break's over!", "Time to get back to work!")
                            timer_label['text'] = "25:00"  # Reset the timer for work session

                def start_pomodoro():
                    # Start countdown (25 minutes)
                    countdown(25 * 60, mode="work")

                def start_break():
                   # Reset the timer label and start countdown for a break (5 minutes)
                    timer_label['text'] = "05:00"
                    countdown(5 * 60, mode="break")


                # Button to start Pomodoro
                start_button = tk.Button(pomodoro_root, text="Start Pomodoro", command=start_pomodoro)
                start_button.pack(pady=10)

                # Button to start break
                break_button = tk.Button(pomodoro_root, text="Start Break", command=start_break)
                break_button.pack(pady=10)

                # Button to quit the session
                quit_button = tk.Button(pomodoro_root, text="Quit", command=pomodoro_root.destroy)
                quit_button.pack(pady=10)

                pomodoro_root.mainloop()

           # def manage_contacts():
                # Placeholder for managing contacts
           #     messagebox.showinfo("Contacts", "Manage your contacts...")
                # Implement contact management functionalities.

            tk.Button(school_root, text="1. Time Table", command=manage_timetable).pack(fill='x')
            tk.Button(school_root, text="2. To-Do List", command=manage_todo_list).pack(fill='x')
            tk.Button(school_root, text="3. Educational Information", command=educational_information).pack(fill='x')
            tk.Button(school_root, text="4. Pomodoro Study Session", command=pomodoro_study_session).pack(fill='x')
           # tk.Button(school_root, text="5. Contacts", command=manage_contacts).pack(fill='x')
            tk.Button(school_root, text="Back to Main Menu", command=go_back).pack(fill='x')

            school_root.mainloop()

        messagebox.showinfo("School Work", "Entering School Work...")
        app_root.destroy()
        school_work_menu()


    def relaxation():
        relaxation_root = tk.Tk()
        relaxation_root.title("Relaxation")

        tk.Label(relaxation_root, text="Time to ease the stress. Take a break and relax.", font=('Helvetica', 14)).pack(pady=20)

        def open_netflix():
            webbrowser.open('https://www.netflix.com/ae-en/')

        def open_prime_video():
            webbrowser.open('https://www.amazon.com/Amazon-Video/b/?&node=2858778011&ref=dvm_MLP_ROWNA_US_1')

        def open_youtube():
            webbrowser.open('https://www.youtube.com/')

        def open_youtube_music():
            webbrowser.open('https://music.youtube.com/')

        def open_google():
            webbrowser.open('https://www.google.com/')

        def search_google():
            search_query = search_entry.get()
            webbrowser.open(f'https://www.google.com/search?q={search_query}')

        tk.Button(relaxation_root, text="Netflix", command=open_netflix).pack(fill='x')
        tk.Button(relaxation_root, text="Prime Video", command=open_prime_video).pack(fill='x')
        tk.Button(relaxation_root, text="YouTube", command=open_youtube).pack(fill='x')
        tk.Button(relaxation_root, text="YouTube Music", command=open_youtube_music).pack(fill='x')
        tk.Button(relaxation_root, text="Google", command=open_google).pack(fill='x')

        # Search entry and button
        search_entry = tk.Entry(relaxation_root, width=50)
        search_entry.pack(pady=5)
        tk.Button(relaxation_root, text="Search on Google", command=search_google).pack(fill='x')

        # Speak to the user
        speak(f"{Username_i}, You have been working hard. Time to take a break and relax.")

        relaxation_root.mainloop()


    def health_section():
        health_root = tk.Tk()
        health_root.title("Health Section")

        # Function to start the meditation session
        def start_meditation_session():
            # Open a meditation YouTube video and an image to set the mood
            webbrowser.open(
                  'https://www.youtube.com/watch?v=inpok4MKVLM'
              )
            webbrowser.open(
                  'https://media.licdn.com/dms/image/D5612AQHgexT41RxevA/article-cover_image-shrink_720_1280/0/1683291132918?e=2147483647&v=beta&t=Anrh697XDZw4lVfWjjTsL2CCMao3-8GpdmRBsvPevJA'
              )
            # You can add an image to your application instead of opening it in a browser
            # if you have an image link or a local image you'd like to use
            # Image example: webbrowser.open('image_link_or_path_here')

        # Function to fetch latest health updates
        def latest_health_updates():
            # Open a health website with COVID updates
            webbrowser.open('https://www.medicalnewstoday.com/')
        
        # Function to get health suggestions from the web
        def get_health_suggestions():
            try:
                # Randomly select a tip from the database
                mycursor.execute("SELECT COUNT(*) FROM healthy_choices")
                max_id = mycursor.fetchone()[0]
                random_id = random.randint(1, max_id)
                mycursor.execute("SELECT TIPS FROM healthy_choices WHERE SL=?", (random_id,))
                tip = mycursor.fetchone()[0]

                # Update the text widget with the health tip
                messagebox.showinfo("Health Tip", tip)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch health tip: {e}")

        tk.Button(health_root, text="Start Meditation Session", command=start_meditation_session).pack(fill='x')
        tk.Button(health_root, text="Latest Health Updates", command=latest_health_updates).pack(fill='x')
        tk.Button(health_root, text="Get Health Suggestions", command=get_health_suggestions).pack(fill='x')
        tk.Button(health_root, text="Back", command=health_root.destroy).pack(fill='x')

        health_root.mainloop()

    # Call the health_section function to run the health section
    #health_section()

    def motivation_section():
        motivation_root = tk.Tk()
        motivation_root.title("Motivation Section")

        # Function to get and speak a random motivational quote
        def get_random_quote():
            # Static variable to remember the last quote index
            if 'last_index' not in get_random_quote.__dict__:
                get_random_quote.last_index = random.randint(1, 21) 

            mycursor = mycon.cursor()
            while True:
                x = random.randint(1, 21)  # Assuming you have 21 entries for quotes
                # Check if the new index is different from the last one
                if x != get_random_quote.last_index:
                    try:
                        mycursor.execute("SELECT * FROM motivation WHERE SL=?", (x,))
                        quote = mycursor.fetchone()
                        quote_text.set(quote[1])  # Update the label with the quote
                        motivation_root.update()  # Update the window to reflect the new quote
                        speak(quote_text.get())  # Speak out the quote
                        get_random_quote.last_index = x  # Remember the last quote index
                        break
                    except Exception as e:
                        messagebox.showerror("Error", f"Could not retrieve quote: {e}")
                        break

        # Label to display the motivational quote
        quote_text = tk.StringVar(motivation_root)
        tk.Label(motivation_root, textvariable=quote_text, wraplength=400, justify="center").pack(pady=20)

        # Button to get a new motivational quote
        tk.Button(motivation_root, text="Get Motivational Quote", command=get_random_quote).pack(pady=10)

        # Button to close the motivation section window
        tk.Button(motivation_root, text="Close", command=motivation_root.destroy).pack(pady=10)

        # Initialize with a random quote
        get_random_quote()

        motivation_root.mainloop()

    # Example usage:
    # Replace 'username_here' with the actual username or pass it as a variable
    #motivation_section()

    
    def feedback():
        messagebox.showinfo("Feedback", "Feature to be implemented...")
        speak("Feedback section coming soon.")

    def virtual_assistant_gui():
        import speech_recognition as sr
        r = sr.Recognizer()

        va_root = tk.Tk()
        va_root.title("Virtual Assistant")
        # Text area to show what the user said
        spoken_text = tk.StringVar(va_root, value="You said nothing yet...")
        spoken_label = tk.Label(va_root, textvariable=spoken_text, wraplength=300, justify="center", font=("Helvetica", 14))
        spoken_label.pack(pady=20)

        # Function to handle voice commands
        def listen_and_respond():
            with sr.Microphone() as source:
                try:
                    print("Listening...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    voice_data = r.recognize_google(audio).lower()
                    spoken_text.set(f"You said: {voice_data}")
                    print("You said:", voice_data)
                    respond(voice_data)
                except sr.UnknownValueError:
                    spoken_text.set("Sorry, I did not get that.")
                    print('Sorry, I did not get that')
                except sr.RequestError:
                    spoken_text.set("Sorry, my speech service is down.")
                    print('Sorry, my speech service is down')
        def secondary():
            with sr.Microphone() as source:
                
                    print("Listening...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    voice_data = r.recognize_google(audio).lower()
                    return voice_data
              
                
         
     
        # Response logic based on voice data
        def respond(voice_data):
            if 'name' in voice_data:
                names = [
                    'My name is Alexis, I am your personal assistant.',
                    'I am Alexis, your virtual assistant.',
                    'Hi, My name is Alexis, your personal assistant.'
                ]
                name_response = random.choice(names)
                speak(name_response)
            elif 'how are you' in voice_data:
                names = [
                    'Im well '+ Username_i+ ' what about you?',
                    'Im well thanks for asking.',
                   
                ]
                name_response = random.choice(names)
                speak(name_response)
                
            elif 'hey' in voice_data or 'hi ' in voice_data:
              
                speak('hey there!!')
            

            elif 'time' in voice_data:
                from time import ctime
                time_info = ctime()
                speak(f"The current time is {time_info}")

            elif 'play' in voice_data:
              speak('Which song shall I play for you ')
              music = secondary()
              url_m = 'https://www.youtube.com/results?search_query=' + music
              webbrowser.get().open(url_m)
              speak('Here is the song ' + music)

            elif 'weather' in voice_data:
              speak('Please name the city to know its weather')
              city = secondary()
              url_w = 'https://www.google.com/search?sxsrf=AOaemvJeg3r8fsTRg7E96LMxjxKY93eJow:1634062837879&q=weather+of+' + city + '&spell=1&sa=X&ved=2ahUKEwjWw_e3vsXzAhUUAWMBHb9RCGQQBSgAegQIARAx&biw=1707&bih=811&dpr=1.13'
              webbrowser.get().open(url_w)
              speak("Here is what I found for the weather of " + city)

            elif 'search' in voice_data:
              speak('What do you want to search for?')
              search = secondary()
              url_s = 'https://google.com/search?q=' + search
              webbrowser.get().open(url_s)
              speak('Here is what I have found for' + search)

            elif 'location' in voice_data:
              speak('What is the location?')
              location = secondary()
              url_l = 'https://google.com/maps/place/' + location + '/&amp;'
              webbrowser.get().open(url_l)
              speak('Here is your location' + location)


            elif 'open mail' in voice_data:
              speak('Opening mail')
              url_mail = 'https://accounts.google.com/ServiceLogin/signinchooser?service=mail&passive=true&rm=false&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F%3Ftab%3Drm%26ogbl&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
              webbrowser.get().open(url_mail)

            elif 'movies' in voice_data:
              speak('Here are some new movies in Cinemas')
              url_movies = 'https://google.com/search?q=new movies'
              webbrowser.get().open(url_movies)

            elif 'joke' in voice_data:
                import pyjokes
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)
                
            elif 'sing a song' in voice_data:
              speak(
                  'I particularly can not sing well, however I can play the song for you'
              )
              speak('Which song shall I play for you ')
              music = secondary()
              url_m = 'https://www.youtube.com/results?search_query=' + music
              webbrowser.get().open(url_m)
              speak('Here is the song ' + music)
              
            elif 'how are you' in voice_data :
              speak('I am doing great, what about you ')
              ans = secondary()
              if 'fine' in ans:
                speak('Thats nice to hear ')
              if 'fine' not in ans:
                speak(' No problem , do not worry things will be fine')

            elif 'bye'  in voice_data or 'exit' in voice_data or 'thank you' in voice_data :
                speak('Goodbye, feel free to interact with me anytime.')
                va_root.destroy()
                

            else:
                speak("I can't help with that yet, but I'm learning more every day!")

         # Circular button
        listen_button = tk.Button(va_root, text="Press to Speak", command=listen_and_respond)
        listen_button.pack(pady=20)
        listen_button.config(height=2, width=10)  # Adjust size as needed for circular appearance


        va_root.mainloop()

    def exit_app():
        app_root.destroy()
        main_menu()

    # Create buttons for each option
    tk.Button(app_root, text="School Work", command=school_work).pack(fill='x')
    tk.Button(app_root, text="Relaxation", command=relaxation).pack(fill='x')
    tk.Button(app_root, text="Health", command=health_section).pack(fill='x')
    tk.Button(app_root, text="Motivation", command=motivation_section).pack(fill='x')
    tk.Button(app_root, text="Virtual Assistant", command=virtual_assistant_gui).pack(fill='x')
    tk.Button(app_root, text="Feedback", command=feedback).pack(fill='x')    
    tk.Button(app_root, text="0 Exit App", command=exit_app).pack(fill='x')

    app_root.mainloop()

def create_signup_gui():
    root = tk.Tk()
    root.title("Signup - Student Companion Application")

    def signup():
        name = name_entry.get()
        grade = grade_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        mycursor.execute("SELECT * FROM sign_up WHERE USERNAME=?", (username,))
        if mycursor.fetchone():
            messagebox.showerror("Error", "Username already exists. Choose a different username.")
            speak("Error. Username already exists. Please choose a different username.")
            return

        sql = "INSERT INTO sign_up(NAME, GRADE, USERNAME, PASSWORD) VALUES (?, ?, ?, ?)"
        val = (name, grade, username, password)
        mycursor.execute(sql, val)
        mycon.commit()

        mycursor.execute(f'CREATE TABLE contacts{username}(NAME VARCHAR(20), EMAIL VARCHAR(20), PHONE INT)')
        mycursor.execute(f'CREATE TABLE hyperlinks{username}(SUBJECT VARCHAR(20), LINK VARCHAR(40))')
        mycursor.execute(f'CREATE TABLE ClassTimeTable{username}(DAY VARCHAR(20), PERIOD_1 VARCHAR(20), PERIOD_2 VARCHAR(20), PERIOD_3 VARCHAR(20))')
        mycursor.execute(f'CREATE TABLE ToDoList{username}(SL INT, TASK TEXT, DEADLINE_DAY VARCHAR(20), DEADLINE_TIME VARCHAR(90))')
        mycon.commit()

        messagebox.showinfo("Success", "Signup successful. Thank you!")
        speak("Signup successful. Thank you!")
        root.destroy()
        main_menu()

    def go_back():
        root.destroy()
        main_menu()

    tk.Label(root, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(root)
    name_entry.grid(row=0, column=1)

    tk.Label(root, text="Grade:").grid(row=1, column=0)
    grade_entry = tk.Entry(root)
    grade_entry.grid(row=1, column=1)

    tk.Label(root, text="Username:").grid(row=2, column=0)
    username_entry = tk.Entry(root)
    username_entry.grid(row=2, column=1)

    tk.Label(root, text="Password:").grid(row=3, column=0)
    password_entry = tk.Entry(root, show="*")
    password_entry.grid(row=3, column=1)

    tk.Button(root, text="Sign Up", command=signup).grid(row=4, column=1)
    tk.Button(root, text="Back", command=go_back).grid(row=4, column=0)

    root.mainloop()

def create_login_gui():
    login_root = tk.Tk()
    login_root.title("Login - Student Companion Application")

    def login():
        global Username_i
        Username_i = username_entry.get()
        password = password_entry.get()

        mycursor.execute("SELECT * FROM sign_up WHERE USERNAME=? AND PASSWORD=?", (Username_i, password))
        result = mycursor.fetchone()
        if result:
            messagebox.showinfo("Login", "Login Successful! Welcome, " + result[0])
            speak("Login successful. Welcome, " + result[0])
            login_root.destroy()
            app_main_menu()  # Open the main app menu after successful login
        else:
            messagebox.showerror("Login", "Invalid Username or Password")
            speak("Invalid Username or Password")

    def go_back():
        login_root.destroy()
        main_menu()

    tk.Label(login_root, text="Username:").grid(row=0, column=0)
    username_entry = tk.Entry(login_root)
    username_entry.grid(row=0, column=1)

    tk.Label(login_root, text="Password:").grid(row=1, column=0)
    password_entry = tk.Entry(login_root, show="*")
    password_entry.grid(row=1, column=1)

    tk.Button(login_root, text="Login", command=login).grid(row=2, column=1)
    tk.Button(login_root, text="Back", command=go_back).grid(row=2, column=0)

    login_root.mainloop()



def main_menu():
    root = tk.Tk()
    root.title("Student Companion Application - Main Menu")

    tk.Label(root, text="Welcome to Student Companion Application", font=('Helvetica', 16)).pack(pady=20)
    tk.Button(root, text="Sign Up", command=lambda: [root.destroy(), create_signup_gui()]).pack()
    tk.Button(root, text="Login", command=lambda: [root.destroy(), create_login_gui()]).pack()
   # tk.Button(root, text="Tell me a joke", command=tell_joke).pack()
    tk.Button(root, text="Exit", command=root.destroy).pack()

    root.mainloop()
#Username_i=None
main_menu()
