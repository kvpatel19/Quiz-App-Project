import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
import random
from mysql.connector import Error

# Function to create connection to MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',      # MySQL host (usually localhost)
            database='quiz_app',   # Your database name
            user='root',           # Your MySQL username
            password=''            # Your MySQL password
        )
        return connection
    except Error as e:
        messagebox.showerror("Error", f"Error: {e}")
        return None

# Function to validate login credentials
def validate_login(username, password):
    connection = create_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    connection.close()
    
    if user and user[2] == password:  # user[2] is the password field
        return True
    return False

# Function for handling user registration
def register_user(username, password, email):
    connection = create_connection()
    if connection is None:
        return False
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
    user = cursor.fetchone()
    
    if user:
        messagebox.showerror("Error", "Username or Email already exists!")
        connection.close()
        return False
    
    cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
    connection.commit()
    connection.close()
    
    messagebox.showinfo("Success", "User registered successfully!")
    return True

# Quiz App Class
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.current_question_index = 0
        self.score = 0
        self.questions = []
        self.previous_page = None

        # Set window size
        self.root.geometry("375x400")
        self.root.resizable(True, True)  # Allow resizing the window
        
        # Remove the window border and title bar
        #self.root.overrideredirect(true)  # This will remove the border and title bar

        
        # Set background color for the main window
        self.root.config(bg="#FFB6C1")  # Light grey background
        
        # Show login screen first
        self.show_login_page()

    def show_login_page(self):
        self.clear_window()
        
        self.label = tk.Label(self.root, text="Username:", font=("Arial", 14), bg="#FFB6C1")
        self.label.pack(pady=10)
        
        self.username_entry = tk.Entry(self.root, font=("Arial", 14), width=30, bg="#FFFFFF")
        self.username_entry.pack(pady=10)

        self.label = tk.Label(self.root, text="Password:", font=("Arial", 14), bg="#FFB6C1")
        self.label.pack(pady=10)

        self.password_entry = tk.Entry(self.root, font=("Arial", 14), show="*", width=30, bg="#FFFFFF")
        self.password_entry.pack(pady=10)

        self.login_button = tk.Button(self.root, text="Login", font=("Arial", 14), width=30, command=self.on_login, bg="#DB7093", fg="white")
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self.root, text="Don't have an account? Register", font=("Arial", 14), width=30, command=self.show_register_page, bg="#DB7093", fg="white")
        self.register_button.pack(pady=10)

    def on_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Input Needed", "Please fill in both fields.")
            return
        
        if validate_login(username, password):
            messagebox.showinfo("Login Success", f"Welcome {username}!")
            self.username = username  # Store the username after login
            self.show_category_page()  # Show category page after login
        else:
            messagebox.showerror("Login Failed", "Invalid credentials, please try again.")

    def show_register_page(self):
        self.previous_page = "login"
        self.clear_window()

        self.label = tk.Label(self.root, text="Username:", font=("Arial", 14), bg="#FFB6C1")
        self.label.pack(pady=10)
        
        self.username_entry_reg = tk.Entry(self.root, font=("Arial", 14), width=30, bg="#ffffff")
        self.username_entry_reg.pack(pady=10)

        self.label = tk.Label(self.root, text="Password:", font=("Arial", 14), bg="#FFB6C1")
        self.label.pack(pady=10)

        self.password_entry_reg = tk.Entry(self.root, font=("Arial", 14), show="*", width=30, bg="#ffffff")
        self.password_entry_reg.pack(pady=10)

        self.label = tk.Label(self.root, text="Email:", font=("Arial", 14), bg="#FFB6C1")
        self.label.pack(pady=10)

        self.email_entry_reg = tk.Entry(self.root, font=("Arial", 14), width=30, bg="#ffffff")
        self.email_entry_reg.pack(pady=10)

        self.register_button = tk.Button(self.root, text="Register", font=("Arial", 14), width=30, command=self.on_register, bg="#DB7093", fg="white")
        self.register_button.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Back to Login", font=("Arial", 14), width=30, command=self.show_login_page, bg="#DB7093", fg="white")
        self.back_button.pack(pady=10)

    def on_register(self):
        username = self.username_entry_reg.get()
        password = self.password_entry_reg.get()
        email = self.email_entry_reg.get()
        
        if not username or not password or not email:
            messagebox.showwarning("Input Needed", "Please fill in all fields.")
            return
        
        if register_user(username, password, email):
            self.show_login_page()  # Go back to login page after successful registration

    def show_category_page(self):
        self.previous_page = "login"
        self.clear_window()

        self.label = tk.Label(self.root, text="Select Category", font=("Arial", 16), bg="#FFB6C1")
        self.label.pack(pady=20)

        categories = self.fetch_categories()
        self.category_buttons = []
        for category in categories:
            button = tk.Button(self.root, text=category[1], width=30, command=lambda c=category: self.select_category(c[0]), bg="#FFE4E1", fg="black")
            button.pack(pady=5)
            self.category_buttons.append(button)

        self.back_button = tk.Button(self.root, text="Back to Login", font=("Arial", 14), width=30, command=self.show_login_page, bg="#DB7093", fg="white")
        self.back_button.pack(pady=10)

    def fetch_categories(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        conn.close()
        return categories

    def select_category(self, category_id):
        self.category_id = category_id
        self.show_level_page()

    def show_level_page(self):
        self.previous_page = "category"
        self.clear_window()

        self.label = tk.Label(self.root, text="Select Level", font=("Arial", 16), bg="#FFB6C1")
        self.label.pack(pady=20)

        levels = self.fetch_levels()
        self.level_buttons = []
        for level in levels:
            button = tk.Button(self.root, text=level[1], width=30, command=lambda l=level: self.select_level(l[0]), bg="#FFE4E1", fg="black")
            button.pack(pady=5)
            self.level_buttons.append(button)

        self.back_button = tk.Button(self.root, text="Back to Categories", font=("Arial", 14), width=30, command=self.show_category_page, bg="#DB7093", fg="white")
        self.back_button.pack(pady=10)

    def fetch_levels(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM levels")
        levels = cursor.fetchall()
        conn.close()
        return levels

    def select_level(self, level_id):
        self.level_id = level_id
        self.questions = self.fetch_questions(self.category_id, self.level_id)
        random.shuffle(self.questions)
        self.ask_question()

    def fetch_questions(self, category_id, level_id):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM questions WHERE category_id = %s AND level_id = %s""", (category_id, level_id))
        questions = cursor.fetchall()
        conn.close()
        return questions

    def ask_question(self):
        if self.current_question_index >= 20 or self.current_question_index >= len(self.questions):
            self.show_score()
            return

        question = self.questions[self.current_question_index]
        self.display_question(question)

    def display_question(self, question):
        self.clear_window()

        question_text = question[3]
        options = [question[4], question[5], question[6], question[7]]
        self.correct_answer = question[8]

        self.label = tk.Label(self.root, text=question_text, font=("Arial", 14), wraplength=350, bg="#FFB6C1")
        self.label.pack(pady=20)

        self.option_buttons = []
        for i, option in enumerate(options):
            button = tk.Button(self.root, text=option, width=50, command=lambda i=i: self.check_answer(i + 1), bg="#FFE4E1", fg="black")
            button.pack(pady=5)
            self.option_buttons.append(button)

    def check_answer(self, answer):
        if answer == self.correct_answer:
            self.score += 1

        self.current_question_index += 1
        self.ask_question()

    def show_score(self):
        self.clear_window()

        self.label = tk.Label(self.root, text=f"Your final score is: {self.score} / 20", font=("Arial", 16), bg="#FFB6C1")
        self.label.pack(pady=20)

        # Button to Exit the app
        button_exit = tk.Button(self.root, text="Exit", width=30, command=self.exit_app, bg="#DB7093", fg="white")
        button_exit.pack(pady=10)

        # Button to Logout
        button_logout = tk.Button(self.root, text="Logout", width=30, command=self.logout, bg="#DB7093", fg="white")
        button_logout.pack(pady=10)

    def logout(self):
        # Clear stored data (reset the score and question index)
        self.username = None
        self.score = 0
        self.current_question_index = 0
        self.questions = []

        # Return to login page
        self.show_login_page()

    def exit_app(self):
        result = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if result:
            self.root.destroy()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Create the main window
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
