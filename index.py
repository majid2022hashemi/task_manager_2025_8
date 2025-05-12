import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import sql
from datetime import datetime

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management System")
        self.root.geometry("1000x700")

        # Database connection
        self.db_connection = self.connect_to_db()

        # Current user state
        self.current_user = None
        self.user_role = None

        # Setup UI
        self.setup_login_ui()

    def connect_to_db(self):
        """Connect to PostgreSQL database"""
        try:
            conn = psycopg2.connect(
                dbname="task_manager_db",
                user="majid",
                password="1361MAJIDhashemi",  # Use real password here
                host="localhost"
            )
            return conn
        except Exception as e:
            messagebox.showerror("Error", f"Database connection failed:\\n{str(e)}")
            self.root.destroy()

    def setup_login_ui(self):
        """Login screen UI"""
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)

        ttk.Label(frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        login_button = ttk.Button(frame, text="Login", command=self.authenticate)
        login_button.grid(row=2, column=1, pady=10, sticky="e")

        # Set focus to username field
        self.username_entry.focus_set()

    def authenticate(self):
        """User authentication"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            cursor = self.db_connection.cursor()
            query = sql.SQL("""
                SELECT id, role FROM users
                WHERE username = %s AND password = %s AND is_active = TRUE
            """)
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                self.current_user = result[0]
                self.user_role = result[1]

                if self.user_role == 'admin':
                    self.setup_admin_dashboard()
                else:
                    self.setup_user_dashboard()
            else:
                messagebox.showerror("Error", "Invalid username or password")

        except Exception as e:
            messagebox.showerror("Error", f"Login error:\\n{str(e)}")

    def setup_admin_dashboard(self):
        """Admin dashboard"""
        self.clear_window()

        # Menu bar
        menubar = tk.Menu(self.root)

        # Users menu
        users_menu = tk.Menu(menubar, tearoff=0)
        users_menu.add_command(label="Manage Users", command=self.manage_users)
        users_menu.add_command(label="Add New User", command=self.add_new_user)
        menubar.add_cascade(label="Users", menu=users_menu)

        # Projects menu
        projects_menu = tk.Menu(menubar, tearoff=0)
        projects_menu.add_command(label="All Projects", command=self.view_all_projects)
        projects_menu.add_command(label="My Projects", command=self.view_my_projects)
        menubar.add_cascade(label="Projects", menu=projects_menu)

        # Tasks menu
        tasks_menu = tk.Menu(menubar, tearoff=0)
        tasks_menu.add_command(label="All Tasks", command=self.view_all_tasks)
        tasks_menu.add_command(label="My Tasks", command=self.view_my_tasks)
        menubar.add_cascade(label="Tasks", menu=tasks_menu)

        # Reports menu
        reports_menu = tk.Menu(menubar, tearoff=0)
        reports_menu.add_command(label="User Performance", command=self.user_performance_report)
        reports_menu.add_command(label="Project Status", command=self.project_status_report)
        menubar.add_cascade(label="Reports", menu=reports_menu)

        # Logout
        menubar.add_command(label="Logout", command=self.logout)

        self.root.config(menu=menubar)

        # Show summary
        self.show_admin_summary()

    def setup_user_dashboard(self):
        """Regular user dashboard"""
        self.clear_window()

        # Menu bar
        menubar = tk.Menu(self.root)

        # Projects menu
        projects_menu = tk.Menu(menubar, tearoff=0)
        projects_menu.add_command(label="My Projects", command=self.view_my_projects)
        menubar.add_cascade(label="Projects", menu=projects_menu)

        # Tasks menu
        tasks_menu = tk.Menu(menubar, tearoff=0)
        tasks_menu.add_command(label="My Tasks", command=self.view_my_tasks)
        tasks_menu.add_command(label="Assigned Tasks", command=self.view_assigned_tasks)
        menubar.add_cascade(label="Tasks", menu=tasks_menu)

        # Profile menu
        profile_menu = tk.Menu(menubar, tearoff=0)
        profile_menu.add_command(label="View Profile", command=self.view_profile)
        profile_menu.add_command(label="Edit Profile", command=self.edit_profile)
        menubar.add_cascade(label="Profile", menu=profile_menu)

        # Logout
        menubar.add_command(label="Logout", command=self.logout)

        self.root.config(menu=menubar)

        # Show summary
        self.show_user_summary()

    def show_admin_summary(self):
        """Admin summary view"""
        summary_frame = ttk.Frame(self.root, padding="20")
        summary_frame.pack(fill="both", expand=True)

        # User stats
        users_stats = self.get_users_stats()
        ttk.Label(summary_frame, text=f"Total Users: {users_stats['total']}", font=('Tahoma', 12)).pack(anchor="w")
        ttk.Label(summary_frame, text=f"Active Users: {users_stats['active']}", font=('Tahoma', 12)).pack(anchor="w")

        # Project stats
        projects_stats = self.get_projects_stats()
        ttk.Label(summary_frame, text=f"Total Projects: {projects_stats['total']}", font=('Tahoma', 12)).pack(anchor="w")

        # Task stats
        tasks_stats = self.get_tasks_stats()
        ttk.Label(summary_frame, text=f"Total Tasks: {tasks_stats['total']}", font=('Tahoma', 12)).pack(anchor="w")

    def get_users_stats(self):
        """Get user statistics"""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            total = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = TRUE")
            active = cursor.fetchone()[0]

            return {'total': total, 'active': active}
        except Exception as e:
            messagebox.showerror("Error", f"Error getting user stats:\\n{str(e)}")
            return {'total': 0, 'active': 0}

    def get_projects_stats(self):
        """Get project statistics"""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM projects")
            total = cursor.fetchone()[0]

            return {'total': total}
        except Exception as e:
            messagebox.showerror("Error", f"Error getting project stats:\\n{str(e)}")
            return {'total': 0}

    def get_tasks_stats(self):
        """Get task statistics"""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM tasks")
            total = cursor.fetchone()[0]

            return {'total': total}
        except Exception as e:
            messagebox.showerror("Error", f"Error getting task stats:\\n{str(e)}")
            return {'total': 0}

    def manage_users(self):
        """User management for admin"""
        self.clear_window()

        # Create Treeview for users
        columns = ("id", "username", "email", "role", "is_active")
        tree = ttk.Treeview(self.root, columns=columns, show="headings")

        # Configure columns
        tree.heading("id", text="ID")
        tree.heading("username", text="Username")
        tree.heading("email", text="Email")
        tree.heading("role", text="Role")
        tree.heading("is_active", text="Active")

        tree.column("id", width=50, anchor="center")
        tree.column("username", width=150)
        tree.column("email", width=200)
        tree.column("role", width=100, anchor="center")
        tree.column("is_active", width=50, anchor="center")

        # Populate Treeview with user data
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id, username, email, role, is_active FROM users ORDER BY id")

            for row in cursor.fetchall():
                tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error getting user list:\\n{str(e)}")

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Management buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        edit_button = ttk.Button(button_frame, text="Edit User", command=lambda: self.edit_user(tree))
        edit_button.pack(side="left", padx=5)

        toggle_button = ttk.Button(button_frame, text="Toggle Active", command=lambda: self.toggle_user_active(tree))
        toggle_button.pack(side="left", padx=5)

        back_button = ttk.Button(button_frame, text="Back", command=self.setup_admin_dashboard)
        back_button.pack(side="right", padx=5)

    def edit_user(self, tree):
        """Edit selected user"""
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user")
            return

        user_data = tree.item(selected_item)['values']
        self.show_edit_user_form(user_data)

    def show_edit_user_form(self, user_data):
        """Show user edit form"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit User {user_data[1]}")
        edit_window.geometry("400x300")

        ttk.Label(edit_window, text="Username:").pack(pady=(10,0))
        username_entry = ttk.Entry(edit_window)
        username_entry.pack(pady=5)
        username_entry.insert(0, user_data[1])

        ttk.Label(edit_window, text="Email:").pack()
        email_entry = ttk.Entry(edit_window)
        email_entry.pack(pady=5)
        email_entry.insert(0, user_data[2])

        ttk.Label(edit_window, text="Role:").pack()
        role_var = tk.StringVar(value=user_data[3])
        role_combobox = ttk.Combobox(edit_window, textvariable=role_var, values=["admin", "user"], state="readonly")
        role_combobox.pack(pady=5)

        is_active_var = tk.BooleanVar(value=user_data[4])
        ttk.Checkbutton(edit_window, text="Active", variable=is_active_var).pack(pady=5)

        def save_changes():
            """Save user changes"""
            try:
                cursor = self.db_connection.cursor()
                query = sql.SQL("""
                    UPDATE users
                    SET username = %s, email = %s, role = %s, is_active = %s, updated_at = NOW()
                    WHERE id = %s
                """)
                cursor.execute(query, (
                    username_entry.get(),
                    email_entry.get(),
                    role_var.get(),
                    is_active_var.get(),
                    user_data[0]
                ))
                self.db_connection.commit()
                messagebox.showinfo("Success", "Changes saved successfully")
                edit_window.destroy()
                self.manage_users()  # Refresh user list
            except Exception as e:
                messagebox.showerror("Error", f"Error saving changes:\\n{str(e)}")

        save_button = ttk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.pack(pady=10)

    def toggle_user_active(self, tree):
        """Toggle user active status"""
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user")
            return

        user_data = tree.item(selected_item)['values']
        new_status = not user_data[4]

        try:
            cursor = self.db_connection.cursor()
            query = sql.SQL("UPDATE users SET is_active = %s WHERE id = %s")
            cursor.execute(query, (new_status, user_data[0]))
            self.db_connection.commit()

            # Update Treeview
            tree.item(selected_item, values=(
                user_data[0],
                user_data[1],
                user_data[2],
                user_data[3],
                new_status
            ))

            messagebox.showinfo("Success", f"User status changed to {'active' if new_status else 'inactive'}")
        except Exception as e:
            messagebox.showerror("Error", f"Error changing user status:\\n{str(e)}")

    def add_new_user(self):
        """Add new user"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New User")
        add_window.geometry("400x400")

        ttk.Label(add_window, text="Username:").pack(pady=(10,0))
        username_entry = ttk.Entry(add_window)
        username_entry.pack(pady=5)

        ttk.Label(add_window, text="Email:").pack()
        email_entry = ttk.Entry(add_window)
        email_entry.pack(pady=5)

        ttk.Label(add_window, text="Password:").pack()
        password_entry = ttk.Entry(add_window, show="*")
        password_entry.pack(pady=5)

        ttk.Label(add_window, text="Confirm Password:").pack()
        confirm_password_entry = ttk.Entry(add_window, show="*")
        confirm_password_entry.pack(pady=5)

        ttk.Label(add_window, text="Full Name:").pack()
        fullname_entry = ttk.Entry(add_window)
        fullname_entry.pack(pady=5)

        ttk.Label(add_window, text="Role:").pack()
        role_var = tk.StringVar(value="user")
        role_combobox = ttk.Combobox(add_window, textvariable=role_var, values=["admin", "user"], state="readonly")
        role_combobox.pack(pady=5)

        is_active_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(add_window, text="Active", variable=is_active_var).pack(pady=5)

        def save_new_user():
            """Save new user"""
            if password_entry.get() != confirm_password_entry.get():
                messagebox.showerror("Error", "Passwords do not match")
                return

            try:
                cursor = self.db_connection.cursor()
                query = sql.SQL("""
                    INSERT INTO users
                    (username, email, password, full_name, role, is_active, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                """)
                cursor.execute(query, (
                    username_entry.get(),
                    email_entry.get(),
                    password_entry.get(),
                    fullname_entry.get(),
                    role_var.get(),
                    is_active_var.get()
                ))
                self.db_connection.commit()
                messagebox.showinfo("Success", "New user added successfully")
                add_window.destroy()
                self.manage_users()  # Refresh user list
            except Exception as e:
                messagebox.showerror("Error", f"Error adding new user:\\n{str(e)}")

        save_button = ttk.Button(add_window, text="Save User", command=save_new_user)
        save_button.pack(pady=10)

    def view_all_projects(self):
        """View all projects (admin)"""
        self.clear_window()

        # Create Treeview for projects
        columns = ("id", "name", "owner", "created_at")
        tree = ttk.Treeview(self.root, columns=columns, show="headings")

        # Configure columns
        tree.heading("id", text="ID")
        tree.heading("name", text="Project Name")
        tree.heading("owner", text="Owner")
        tree.heading("created_at", text="Created At")

        tree.column("id", width=50, anchor="center")
        tree.column("name", width=200)
        tree.column("owner", width=150)
        tree.column("created_at", width=120)

        # Populate Treeview with project data
        try:
            cursor = self.db_connection.cursor()
            query = sql.SQL("""
                SELECT p.id, p.name, u.username, p.created_at
                FROM projects p
                JOIN users u ON p.owner_id = u.id
                ORDER BY p.id
            """)
            cursor.execute(query)

            for row in cursor.fetchall():
                tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error getting project list:\\n{str(e)}")

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Management buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        view_button = ttk.Button(button_frame, text="View Details", command=lambda: self.view_project_details(tree))
        view_button.pack(side="left", padx=5)

        back_button = ttk.Button(button_frame, text="Back", command=self.setup_admin_dashboard)
        back_button.pack(side="right", padx=5)

    def view_project_details(self, tree):
        """View project details"""
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a project")
            return

        project_data = tree.item(selected_item)['values']

        details_window = tk.Toplevel(self.root)
        details_window.title(f"Project Details: {project_data[1]}")
        details_window.geometry("600x500")

        # Show basic project info
        info_frame = ttk.Frame(details_window, padding="10")
        info_frame.pack(fill="x")

        ttk.Label(info_frame, text=f"Project Name: {project_data[1]}", font=('Tahoma', 12, 'bold')).pack(anchor="w")
        ttk.Label(info_frame, text=f"Project Owner: {project_data[2]}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Created At: {project_data[3]}").pack(anchor="w")

        # Get project description from database
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT description FROM projects WHERE id = %s", (project_data[0],))
            description = cursor.fetchone()[0] or "No description available"

            ttk.Label(info_frame, text="Description:").pack(anchor="w")
            desc_text = tk.Text(info_frame, height=5, width=60, wrap="word")
            desc_text.pack(fill="x", pady=5)
            desc_text.insert("1.0", description)
            desc_text.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"Error getting project info:\\n{str(e)}")

        # Show project tasks
        tasks_frame = ttk.LabelFrame(details_window, text="Project Tasks", padding="10")
        tasks_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "title", "status", "priority", "due_date")
        tasks_tree = ttk.Treeview(tasks_frame, columns=columns, show="headings")

        tasks_tree.heading("id", text="ID")
        tasks_tree.heading("title", text="Title")
        tasks_tree.heading("status", text="Status")
        tasks_tree.heading("priority", text="Priority")
        tasks_tree.heading("due_date", text="Due Date")

        tasks_tree.column("id", width=50, anchor="center")
        tasks_tree.column("title", width=200)
        tasks_tree.column("status", width=100)
        tasks_tree.column("priority", width=80)
        tasks_tree.column("due_date", width=100)

        try:
            cursor = self.db_connection.cursor()
            query = sql.SQL("""
                SELECT t.id, t.title, s.name, pl.level, t.due_date
                FROM tasks t
                JOIN status s ON t.status_id = s.id
                JOIN priority_levels pl ON t.priority_id = pl.id
                WHERE t.id IN (
                    SELECT task_id FROM project_tasks WHERE project_id = %s
                )
                ORDER BY t.due_date
            """)
            cursor.execute(query, (project_data[0],))

            for row in cursor.fetchall():
                tasks_tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error getting task list:\\n{str(e)}")

        tasks_tree.pack(fill="both", expand=True)

    def view_my_projects(self):
        """View current user's projects"""
        self.clear_window()

        # Create Treeview for projects
        columns = ("id", "name", "created_at")
        tree = ttk.Treeview(self.root, columns=columns, show="headings")

        # Configure columns
        tree.heading("id", text="ID")
        tree.heading("name", text="Project Name")
        tree.heading("created_at", text="Created At")

        tree.column("id", width=50, anchor="center")
        tree.column("name", width=300)
        tree.column("created_at", width=120)

        # Populate Treeview with user's projects
        try:
            cursor = self.db_connection.cursor()
            query = sql.SQL("""
                SELECT id, name, created_at
                FROM projects
                WHERE owner_id = %s
                ORDER BY created_at DESC
            """)
            cursor.execute(query, (self.current_user,))

            for row in cursor.fetchall():
                tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error getting project list:\\n{str(e)}")

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Management buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        view_button = ttk.Button(button_frame, text="View Details", command=lambda: self.view_project_details(tree))
        view_button.pack(side="left", padx=5)

        add_button = ttk.Button(button_frame, text="New Project", command=self.add_new_project)
        add_button.pack(side="left", padx=5)

        back_button = ttk.Button(button_frame, text="Back",
                               command=self.setup_admin_dashboard if self.user_role == 'admin' else self.setup_user_dashboard)
        back_button.pack(side="right", padx=5)

    def add_new_project(self):
        """Add new project"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Project")
        add_window.geometry("500x400")

        ttk.Label(add_window, text="Project Name:").pack(pady=(10,0))
        name_entry = ttk.Entry(add_window)
        name_entry.pack(pady=5, fill="x", padx=10)

        ttk.Label(add_window, text="Description:").pack()
        desc_text = tk.Text(add_window, height=10, wrap="word")
        desc_text.pack(pady=5, fill="both", expand=True, padx=10)

        def save_project():
            """Save new project"""
            try:
                cursor = self.db_connection.cursor()
                query = sql.SQL("""
                    INSERT INTO projects
                    (name, description, owner_id, created_at)
                    VALUES (%s, %s, %s, NOW())
                """)
                cursor.execute(query, (
                    name_entry.get(),
                    desc_text.get("1.0", "end-1c"),
                    self.current_user
                ))
                self.db_connection.commit()
                messagebox.showinfo("Success", "New project added successfully")
                add_window.destroy()
                self.view_my_projects()  # Refresh project list
            except Exception as e:
                messagebox.showerror("Error", f"Error adding new project:\\n{str(e)}")

        button_frame = ttk.Frame(add_window)
        button_frame.pack(fill="x", pady=10, padx=10)

        save_button = ttk.Button(button_frame, text="Save Project", command=save_project)
        save_button.pack(side="right")

        cancel_button = ttk.Button(button_frame, text="Cancel", command=add_window.destroy)
        cancel_button.pack(side="left")

    def view_all_tasks(self):
        """View all tasks (admin)"""
        self.clear_window()

        # Create Treeview for tasks
        columns = ("id", "title", "project", "assignee", "status", "priority", "due_date")
        tree = ttk.Treeview(self.root, columns=columns, show="headings")

        # Configure columns
        tree.heading("id", text="ID")
        tree.heading("title", text="Title")
        tree.heading("project", text="Project")
        tree.heading("assignee", text="Assignee")
        tree.heading("status", text="Status")
        tree.heading("priority", text="Priority")
        tree.heading("due_date", text="Due Date")

        tree.column("id", width=50, anchor="center")
        tree.column("title", width=200)
        tree.column("project", width=150)
        tree.column("assignee", width=100)
        tree.column("status", width=80)
        tree.column("priority", width=80)
        tree.column("due_date", width=100)

        # Populate Treeview with task data
        try:
            cursor = self.db_connection.cursor()
            query = sql.SQL("""
                SELECT t.id, t.title, p.name, u.username, s.name, pl.level, t.due_date
                FROM tasks t
                LEFT JOIN projects p ON t.project_id = p.id
                JOIN users u ON t.user_id = u.id
                JOIN status s ON t.status_id = s.id
                JOIN priority_levels pl ON t.priority_id = pl.id
                ORDER BY t.due_date
            """)
            cursor.execute(query)

            for row in cursor.fetchall():
                tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error getting task list:\\n{str(e)}")

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Management buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        view_button = ttk.Button(button_frame, text="View Details", command=lambda: self.view_task_details(tree))
        view_button.pack(side="left", padx=5)

        back_button = ttk.Button(button_frame, text="Back", command=self.setup_admin_dashboard)
        back_button.pack(side="right", padx=5)

    def view_my_tasks(self):
        """View current user's tasks"""
        self.clear_window()

        # Create Treeview for tasks
        columns = ("id", "title", "project", "status", "priority", "due_date")
        tree = ttk.Treeview(self.root, columns=columns, show="headings")

        # Configure columns
        tree.heading("id", text="ID")
        tree.heading("title", text="Title")
        tree.heading("project", text="Project")
        tree.heading("status", text="Status")
        tree.heading("priority", text="Priority")
        tree.heading("due_date", text="Due Date")

        tree.column("id", width=50, anchor="center")
        tree.column("title", width=250)
        tree.column("project", width=150)
        tree.column("status", width=100)
        tree.column("priority", width=80)
        tree.column("due_date", width=100)

        # Populate Treeview with user's tasks
        try:
            cursor = self.db_connection.cursor()
            query = sql.SQL("""
                SELECT t.id, t.title, p.name, s.name, pl.level, t.due_date
                FROM tasks t
                LEFT JOIN projects p ON t.project_id = p.id
                JOIN status s ON t.status_id = s.id
                JOIN priority_levels pl ON t.priority_id = pl.id
                WHERE t.user_id = %s
                ORDER BY t.due_date
            """)
            cursor.execute(query, (self.current_user,))

            for row in cursor.fetchall():
                tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error getting task list:\\n{str(e)}")

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Management buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        view_button = ttk.Button(button_frame, text="View Details", command=lambda: self.view_task_details(tree))
        view_button.pack(side="left", padx=5)

        add_button = ttk.Button(button_frame, text="New Task", command=self.add_new_task)
        add_button.pack(side="left", padx=5)

        back_button = ttk.Button(button_frame, text="Back",
                               command=self.setup_admin_dashboard if self.user_role == 'admin' else self.setup_user_dashboard)
        back_button.pack(side="right", padx=5)

    def view_task_details(self, tree):
        """View task details"""
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task")
            return

        task_data = tree.item(selected_item)['values']

        details_window = tk.Toplevel(self.root)
        details_window.title(f"Task Details: {task_data[1]}")
        details_window.geometry("700x600")

        # Show basic task info
        info_frame = ttk.Frame(details_window, padding="10")
        info_frame.pack(fill="x")

        ttk.Label(info_frame, text=f"Title: {task_data[1]}", font=('Tahoma', 12, 'bold')).pack(anchor="w")

        # Show project if exists
        if len(task_data) > 2 and task_data[2]:
            ttk.Label(info_frame, text=f"Project: {task_data[2]}").pack(anchor="w")

        ttk.Label(info_frame, text=f"Status: {task_data[3]}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Priority: {task_data[4]}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Due Date: {task_data[5]}").pack(anchor="w")

        # Get full task description from database
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT description FROM tasks WHERE id = %s", (task_data[0],))
            description = cursor.fetchone()[0] or "No description available"

            ttk.Label(info_frame, text="Description:").pack(anchor="w")
            desc_text = tk.Text(info_frame, height=5, width=60, wrap="word")
            desc_text.pack(fill="x", pady=5)
            desc_text.insert("1.0", description)
            desc_text.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"Error getting task info:\\n{str(e)}")

        # Show subtasks
        subtasks_frame = ttk.LabelFrame(details_window, text="Subtasks", padding="10")
        subtasks_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("title", "is_completed")
        subtasks_tree = ttk.Treeview(subtasks_frame, columns=columns, show="headings")

        subtasks_tree.heading("title", text="Title")
        subtasks_tree.heading("is_completed", text="Completed")

        subtasks_tree.column("title", width=300)
        subtasks_tree.column("is_completed", width=100, anchor="center")

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT title, is_completed FROM subtasks WHERE task_id = %s", (task_data[0],))

            for row in cursor.fetchall():
                subtasks_tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error getting subtask list:\\n{str(e)}")

        subtasks_tree.pack(fill="both", expand=True)

        # Show comments
        comments_frame = ttk.LabelFrame(details_window, text="Comments", padding="10")
        comments_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("user", "content", "created_at")
        comments_tree = ttk.Treeview(comments_frame, columns=columns, show="headings")

        comments_tree.heading("user", text="User")
        comments_tree.heading("content", text="Comment")
        comments_tree.heading("created_at", text="Date")

        comments_tree.column("user", width=100)
        comments_tree.column("content", width=300)
        comments_tree.column("created_at", width=120)

        try:
            cursor = self.db_connection.cursor()
            query = sql.SQL("""
                SELECT u.username, c.content, c.created_at
                FROM comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.task_id = %s
                ORDER BY c.created_at DESC
            """)
            cursor.execute(query, (task_data[0],))

            for row in cursor.fetchall():
                comments_tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error getting comment list:\\n{str(e)}")

        comments_tree.pack(fill="both", expand=True)

        # Show edit buttons if user is task owner
        if self.user_role == 'admin' or (len(task_data) > 2 and task_data[2] == self.current_user):
            button_frame = ttk.Frame(details_window)
            button_frame.pack(pady=10)

            edit_button = ttk.Button(button_frame, text="Edit Task", command=lambda: self.edit_task(task_data[0]))
            edit_button.pack(side="left", padx=5)

            add_subtask_button = ttk.Button(button_frame, text="Add Subtask", command=lambda: self.add_subtask(task_data[0]))
            add_subtask_button.pack(side="left", padx=5)

            add_comment_button = ttk.Button(button_frame, text="Add Comment", command=lambda: self.add_comment(task_data[0]))
            add_comment_button.pack(side="left", padx=5)

    def add_new_task(self):
        """Add new task"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Task")
        add_window.geometry("600x500")

        # Get user's projects
        projects = []
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id, name FROM projects WHERE owner_id = %s", (self.current_user,))
            projects = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error getting project list:\\n{str(e)}")

        # Get statuses
        statuses = []
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id, name FROM status")
            statuses = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error getting status list:\\n{str(e)}")

        # Get priorities
        priorities = []
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id, level FROM priority_levels")
            priorities = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error getting priority list:\\n{str(e)}")

        # Get users (for admin)
        users = []
        if self.user_role == 'admin':
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("SELECT id, username FROM users WHERE is_active = TRUE")
                users = cursor.fetchall()
            except Exception as e:
                messagebox.showerror("Error", f"Error getting user list:\\n{str(e)}")

        # Task creation form
        form_frame = ttk.Frame(add_window, padding="10")
        form_frame.pack(fill="both", expand=True)

        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky="e", pady=5)
        title_entry = ttk.Entry(form_frame)
        title_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(form_frame, text="Project:").grid(row=1, column=0, sticky="e", pady=5)
        project_var = tk.StringVar()
        project_combobox = ttk.Combobox(form_frame, textvariable=project_var)
        project_combobox['values'] = [f"{p[0]} - {p[1]}" for p in projects]
        project_combobox.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(form_frame, text="Status:").grid(row=2, column=0, sticky="e", pady=5)
        status_var = tk.StringVar()
        status_combobox = ttk.Combobox(form_frame, textvariable=status_var, state="readonly")
        status_combobox['values'] = [s[1] for s in statuses]
        status_combobox.current(0)
        status_combobox.grid(row=2, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(form_frame, text="Priority:").grid(row=3, column=0, sticky="e", pady=5)
        priority_var = tk.StringVar()
        priority_combobox = ttk.Combobox(form_frame, textvariable=priority_var, state="readonly")
        priority_combobox['values'] = [p[1] for p in priorities]
        priority_combobox.current(0)
        priority_combobox.grid(row=3, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(form_frame, text="Due Date:").grid(row=4, column=0, sticky="e", pady=5)
        due_date_entry = ttk.Entry(form_frame)
        due_date_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=5)
        due_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        if self.user_role == 'admin':
            ttk.Label(form_frame, text="Assignee:").grid(row=5, column=0, sticky="e", pady=5)
            assignee_var = tk.StringVar()
            assignee_combobox = ttk.Combobox(form_frame, textvariable=assignee_var)
            assignee_combobox['values'] = [f"{u[0]} - {u[1]}" for u in users]
            assignee_combobox.grid(row=5, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(form_frame, text="Description:").grid(row=6, column=0, sticky="ne", pady=5)
        desc_text = tk.Text(form_frame, height=8, wrap="word")
        desc_text.grid(row=6, column=1, sticky="nsew", pady=5, padx=5)

        # Configure row/column weights for expansion
        form_frame.grid_rowconfigure(6, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        def save_task():
            """Save new task"""
            try:
                # Get values from form
                project_id = project_var.get().split(" - ")[0] if project_var.get() else None
                status_id = [s[0] for s in statuses if s[1] == status_var.get()][0]
                priority_id = [p[0] for p in priorities if p[1] == priority_var.get()][0]

                if self.user_role == 'admin':
                    assignee_id = assignee_var.get().split(" - ")[0] if assignee_var.get() else self.current_user
                else:
                    assignee_id = self.current_user

                # Save to database
                cursor = self.db_connection.cursor()
                query = sql.SQL("""
                    INSERT INTO tasks
                    (title, description, due_date, user_id, status_id, priority_id, project_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """)
                cursor.execute(query, (
                    title_entry.get(),
                    desc_text.get("1.0", "end-1c"),
                    due_date_entry.get(),
                    assignee_id,
                    status_id,
                    priority_id,
                    project_id if project_id else None
                ))
                self.db_connection.commit()
                messagebox.showinfo("Success", "New task added successfully")
                add_window.destroy()
                self.view_my_tasks()  # Refresh task list
            except Exception as e:
                messagebox.showerror("Error", f"Error adding new task:\\n{str(e)}")

        button_frame = ttk.Frame(add_window)
        button_frame.pack(fill="x", pady=10, padx=10)

        save_button = ttk.Button(button_frame, text="Save Task", command=save_task)
        save_button.pack(side="right")

        cancel_button = ttk.Button(button_frame, text="Cancel", command=add_window.destroy)
        cancel_button.pack(side="left")

    def edit_task(self, task_id):
        """Edit existing task"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.geometry("600x500")

        # Get current task info
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                SELECT title, description, due_date, user_id, status_id, priority_id, project_id
                FROM tasks
                WHERE id = %s
            """, (task_id,))
            task_data = cursor.fetchone()

            if not task_data:
                messagebox.showerror("Error", "Task not found")
                edit_window.destroy()
                return
        except Exception as e:
            messagebox.showerror("Error", f"Error getting task info:\\n{str(e)}")
            edit_window.destroy()
            return

        # Get projects
        projects = []
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id, name FROM projects WHERE owner_id = %s", (self.current_user,))
            projects = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error getting project list:\\n{str(e)}")

        # Get statuses
        statuses = []
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id, name FROM status")
            statuses = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error getting status list:\\n{str(e)}")

        # Get priorities
        priorities = []
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id, level FROM priority_levels")
            priorities = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error getting priority list:\\n{str(e)}")

        # Get users (for admin)
        users = []
        if self.user_role == 'admin':
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("SELECT id, username FROM users WHERE is_active = TRUE")
                users = cursor.fetchall()
            except Exception as e:
                messagebox.showerror("Error", f"Error getting user list:\\n{str(e)}")

        # Task edit form
        form_frame = ttk.Frame(edit_window, padding="10")
        form_frame.pack(fill="both", expand=True)

        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky="e", pady=5)
        title_entry = ttk.Entry(form_frame)
        title_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        title_entry.insert(0, task_data[0])

        ttk.Label(form_frame, text="Project:").grid(row=1, column=0, sticky="e", pady=5)
        project_var = tk.StringVar()
        project_combobox = ttk.Combobox(form_frame, textvariable=project_var)
        project_combobox['values'] = [f"{p[0]} - {p[1]}" for p in projects]

        # Set current project if exists
        if task_data[6]:
            for p in projects:
                if p[0] == task_data[6]:
                    project_var.set(f"{p[0]} - {p[1]}")
                    break

        project_combobox.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(form_frame, text="Status:").grid(row=2, column=0, sticky="e", pady=5)
        status_var = tk.StringVar()
        status_combobox = ttk.Combobox(form_frame, textvariable=status_var, state="readonly")
        status_combobox['values'] = [s[1] for s in statuses]

        # Set current status
        for s in statuses:
            if s[0] == task_data[4]:
                status_var.set(s[1])
                break

        status_combobox.grid(row=2, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(form_frame, text="Priority:").grid(row=3, column=0, sticky="e", pady=5)
        priority_var = tk.StringVar()
        priority_combobox = ttk.Combobox(form_frame, textvariable=priority_var, state="readonly")
        priority_combobox['values'] = [p[1] for p in priorities]

        # Set current priority
        for p in priorities:
            if p[0] == task_data[5]:
                priority_var.set(p[1])
                break

        priority_combobox.grid(row=3, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(form_frame, text="Due Date:").grid(row=4, column=0, sticky="e", pady=5)
        due_date_entry = ttk.Entry(form_frame)
        due_date_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=5)
        due_date_entry.insert(0, task_data[2])

        if self.user_role == 'admin':
            ttk.Label(form_frame, text="Assignee:").grid(row=5, column=0, sticky="e", pady=5)
            assignee_var = tk.StringVar()
            assignee_combobox = ttk.Combobox(form_frame, textvariable=assignee_var)
            assignee_combobox['values'] = [f"{u[0]} - {u[1]}" for u in users]

            # Set current assignee
            for u in users:
                if u[0] == task_data[3]:
                    assignee_var.set(f"{u[0]} - {u[1]}")
                    break

            assignee_combobox.grid(row=5, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(form_frame, text="Description:").grid(row=6, column=0, sticky="ne", pady=5)
        desc_text = tk.Text(form_frame, height=8, wrap="word")
        desc_text.grid(row=6, column=1, sticky="nsew", pady=5, padx=5)
        desc_text.insert("1.0", task_data[1] if task_data[1] else "")

        # Configure row/column weights for expansion
        form_frame.grid_rowconfigure(6, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        def save_changes():
            """Save task changes"""
            try:
                # Get values from form
                project_id = project_var.get().split(" - ")[0] if project_var.get() else None
                status_id = [s[0] for s in statuses if s[1] == status_var.get()][0]
                priority_id = [p[0] for p in priorities if p[1] == priority_var.get()][0]

                if self.user_role == 'admin':
                    assignee_id = assignee_var.get().split(" - ")[0] if assignee_var.get() else self.current_user
                else:
                    assignee_id = self.current_user

                # Save to database
                cursor = self.db_connection.cursor()
                query = sql.SQL("""
                    UPDATE tasks
                    SET title = %s, description = %s, due_date = %s,
                        user_id = %s, status_id = %s, priority_id = %s,
                        project_id = %s
                    WHERE id = %s
                """)
                cursor.execute(query, (
                    title_entry.get(),
                    desc_text.get("1.0", "end-1c"),
                    due_date_entry.get(),
                    assignee_id,
                    status_id,
                    priority_id,
                    project_id if project_id else None,
                    task_id
                ))
                self.db_connection.commit()
                messagebox.showinfo("Success", "Changes saved successfully")
                edit_window.destroy()
                self.view_my_tasks()  # Refresh task list
            except Exception as e:
                messagebox.showerror("Error", f"Error saving changes:\\n{str(e)}")

        button_frame = ttk.Frame(edit_window)
        button_frame.pack(fill="x", pady=10, padx=10)

        save_button = ttk.Button(button_frame, text="Save Changes", command=save_changes)
        save_button.pack(side="right")

        cancel_button = ttk.Button(button_frame, text="Cancel", command=edit_window.destroy)
        cancel_button.pack(side="left")

    def add_subtask(self, task_id):
        """Add subtask to task"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Subtask")
        add_window.geometry("400x300")

        ttk.Label(add_window, text="Title:").pack(pady=(10,0))
        title_entry = ttk.Entry(add_window)
        title_entry.pack(pady=5, fill="x", padx=10)

        ttk.Label(add_window, text="Description:").pack()
        desc_text = tk.Text(add_window, height=8, wrap="word")
        desc_text.pack(pady=5, fill="both", expand=True, padx=10)

        is_completed_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(add_window, text="Completed", variable=is_completed_var).pack(pady=5)

        def save_subtask():
            """Save new subtask"""
            try:
                cursor = self.db_connection.cursor()
                query = sql.SQL("""
                    INSERT INTO subtasks
                    (task_id, title, description, is_completed, created_at)
                    VALUES (%s, %s, %s, %s, NOW())
                """)
                cursor.execute(query, (
                    task_id,
                    title_entry.get(),
                    desc_text.get("1.0", "end-1c"),
                    is_completed_var.get()
                ))
                self.db_connection.commit()
                messagebox.showinfo("Success", "New subtask added successfully")
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error adding new subtask:\\n{str(e)}")

        button_frame = ttk.Frame(add_window)
        button_frame.pack(fill="x", pady=10, padx=10)

        save_button = ttk.Button(button_frame, text="Save Subtask", command=save_subtask)
        save_button.pack(side="right")

        cancel_button = ttk.Button(button_frame, text="Cancel", command=add_window.destroy)
        cancel_button.pack(side="left")

    def add_comment(self, task_id):
        """Add comment to task"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Comment")
        add_window.geometry("400x300")

        ttk.Label(add_window, text="Your Comment:").pack(pady=(10,0))
        comment_text = tk.Text(add_window, height=10, wrap="word")
        comment_text.pack(pady=5, fill="both", expand=True, padx=10)

        def save_comment():
            """Save new comment"""
            content = comment_text.get("1.0", "end-1c").strip()
            if not content:
                messagebox.showwarning("Warning", "Please enter comment text")
                return

            try:
                cursor = self.db_connection.cursor()
                query = sql.SQL("""
                    INSERT INTO comments
                    (task_id, user_id, content, created_at)
                    VALUES (%s, %s, %s, NOW())
                """)
                cursor.execute(query, (
                    task_id,
                    self.current_user,
                    content
                ))
                self.db_connection.commit()
                messagebox.showinfo("Success", "Comment added successfully")
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error adding comment:\\n{str(e)}")

        button_frame = ttk.Frame(add_window)
        button_frame.pack(fill="x", pady=10, padx=10)

        save_button = ttk.Button(button_frame, text="Post Comment", command=save_comment)
        save_button.pack(side="right")

        cancel_button = ttk.Button(button_frame, text="Cancel", command=add_window.destroy)
        cancel_button.pack(side="left")

    def view_assigned_tasks(self):
        """View tasks assigned to user (for regular users)"""
        self.clear_window()

        # Create Treeview for tasks
        columns = ("id", "title", "project", "status", "priority", "due_date")
        tree = ttk.Treeview(self.root, columns=columns, show="headings")

        # Configure columns
        tree.heading("id", text="ID")
        tree.heading("title", text="Title")
        tree.heading("project", text="Project")
        tree.heading("status", text="Status")
        tree.heading("priority", text="Priority")
        tree.heading("due_date", text="Due Date")

        tree.column("id", width=50, anchor="center")
        tree.column("title", width=250)
        tree.column("project", width=150)
        tree.column("status", width=100)
        tree.column("priority", width=80)
        tree.column("due_date", width=100)

        # Populate Treeview with assigned tasks
        try:
            cursor = self.db_connection.cursor()
            query = sql.SQL("""
                SELECT t.id, t.title, p.name, s.name, pl.level, t.due_date
                FROM tasks t
                LEFT JOIN projects p ON t.project_id = p.id
                JOIN status s ON t.status_id = s.id
                JOIN priority_levels pl ON t.priority_id = pl.id
                WHERE t.user_id = %s AND p.owner_id != %s
                ORDER BY t.due_date
            """)
            cursor.execute(query, (self.current_user, self.current_user))

            for row in cursor.fetchall():
                tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error getting task list:\\n{str(e)}")

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Management buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        view_button = ttk.Button(button_frame, text="View Details", command=lambda: self.view_task_details(tree))
        view_button.pack(side="left", padx=5)

        back_button = ttk.Button(button_frame, text="Back", command=self.setup_user_dashboard)
        back_button.pack(side="right", padx=5)

    def view_profile(self):
        """View user profile"""
        profile_window = tk.Toplevel(self.root)
        profile_window.title("User Profile")
        profile_window.geometry("400x300")

        try:
            cursor = self.db_connection.cursor()

            # Get basic user info
            cursor.execute("""
                SELECT username, email, full_name, created_at, role
                FROM users
                WHERE id = %s
            """, (self.current_user,))
            user_data = cursor.fetchone()

            # Get profile info
            cursor.execute("""
                SELECT avatar_url, bio
                FROM user_profiles
                WHERE user_id = %s
            """, (self.current_user,))
            profile_data = cursor.fetchone()

            # Display info
            info_frame = ttk.Frame(profile_window, padding="10")
            info_frame.pack(fill="both", expand=True)

            ttk.Label(info_frame, text=f"Username: {user_data[0]}", font=('Tahoma', 12, 'bold')).pack(anchor="w")
            ttk.Label(info_frame, text=f"Email: {user_data[1]}").pack(anchor="w")

            if user_data[2]:
                ttk.Label(info_frame, text=f"Full Name: {user_data[2]}").pack(anchor="w")

            ttk.Label(info_frame, text=f"Member Since: {user_data[3]}").pack(anchor="w")
            ttk.Label(info_frame, text=f"Role: {user_data[4]}").pack(anchor="w")

            if profile_data:
                if profile_data[1]:
                    ttk.Label(info_frame, text="About Me:").pack(anchor="w")
                    bio_text = tk.Text(info_frame, height=4, wrap="word")
                    bio_text.pack(fill="x", pady=5)
                    bio_text.insert("1.0", profile_data[1])
                    bio_text.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"Error getting profile info:\\n{str(e)}")
            profile_window.destroy()

    def edit_profile(self):
        """Edit user profile"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Profile")
        edit_window.geometry("400x400")

        try:
            cursor = self.db_connection.cursor()

            # Get basic user info
            cursor.execute("""
                SELECT username, email, full_name
                FROM users
                WHERE id = %s
            """, (self.current_user,))
            user_data = cursor.fetchone()

            # Get profile info
            cursor.execute("""
                SELECT avatar_url, bio
                FROM user_profiles
                WHERE user_id = %s
            """, (self.current_user,))
            profile_data = cursor.fetchone()

            # Edit form
            form_frame = ttk.Frame(edit_window, padding="10")
            form_frame.pack(fill="both", expand=True)

            ttk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky="e", pady=5)
            username_entry = ttk.Entry(form_frame)
            username_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
            username_entry.insert(0, user_data[0])
            username_entry.config(state="readonly")

            ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky="e", pady=5)
            email_entry = ttk.Entry(form_frame)
            email_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
            email_entry.insert(0, user_data[1])
            email_entry.config(state="readonly")

            ttk.Label(form_frame, text="Full Name:").grid(row=2, column=0, sticky="e", pady=5)
            fullname_entry = ttk.Entry(form_frame)
            fullname_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
            if user_data[2]:
                fullname_entry.insert(0, user_data[2])

            ttk.Label(form_frame, text="Avatar URL:").grid(row=3, column=0, sticky="e", pady=5)
            avatar_entry = ttk.Entry(form_frame)
            avatar_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=5)
            if profile_data and profile_data[0]:
                avatar_entry.insert(0, profile_data[0])

            ttk.Label(form_frame, text="About Me:").grid(row=4, column=0, sticky="ne", pady=5)
            bio_text = tk.Text(form_frame, height=5, wrap="word")
            bio_text.grid(row=4, column=1, sticky="nsew", pady=5, padx=5)
            if profile_data and profile_data[1]:
                bio_text.insert("1.0", profile_data[1])

            # Configure row/column weights for expansion
            form_frame.grid_rowconfigure(4, weight=1)
            form_frame.grid_columnconfigure(1, weight=1)

            def save_changes():
                """Save profile changes"""
                try:
                    cursor = self.db_connection.cursor()

                    # Update basic info
                    cursor.execute("""
                        UPDATE users
                        SET full_name = %s, updated_at = NOW()
                        WHERE id = %s
                    """, (
                        fullname_entry.get() if fullname_entry.get() else None,
                        self.current_user
                    ))

                    # Update or create profile
                    if profile_data:
                        cursor.execute("""
                            UPDATE user_profiles
                            SET avatar_url = %s, bio = %s
                            WHERE user_id = %s
                        """, (
                            avatar_entry.get() if avatar_entry.get() else None,
                            bio_text.get("1.0", "end-1c") if bio_text.get("1.0", "end-1c").strip() else None,
                            self.current_user
                        ))
                    else:
                        cursor.execute("""
                            INSERT INTO user_profiles
                            (user_id, avatar_url, bio)
                            VALUES (%s, %s, %s)
                        """, (
                            self.current_user,
                            avatar_entry.get() if avatar_entry.get() else None,
                            bio_text.get("1.0", "end-1c") if bio_text.get("1.0", "end-1c").strip() else None
                        ))

                    self.db_connection.commit()
                    messagebox.showinfo("Success", "Profile changes saved successfully")
                    edit_window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Error saving changes:\\n{str(e)}")

            button_frame = ttk.Frame(edit_window)
            button_frame.pack(fill="x", pady=10, padx=10)

            save_button = ttk.Button(button_frame, text="Save Changes", command=save_changes)
            save_button.pack(side="right")

            cancel_button = ttk.Button(button_frame, text="Cancel", command=edit_window.destroy)
            cancel_button.pack(side="left")

        except Exception as e:
            messagebox.showerror("Error", f"Error getting profile info:\\n{str(e)}")
            edit_window.destroy()

    def user_performance_report(self):
        """User performance report (admin)"""
        report_window = tk.Toplevel(self.root)
        report_window.title("User Performance Report")
        report_window.geometry("800x600")

        try:
            cursor = self.db_connection.cursor()

            # Get user performance stats
            cursor.execute("""
                SELECT
                    u.id, u.username,
                    COUNT(t.id) AS total_tasks,
                    SUM(CASE WHEN s.name = 'Completed' THEN 1 ELSE 0 END) AS completed_tasks,
                    SUM(CASE WHEN t.due_date < CURRENT_DATE AND s.name != 'Completed' THEN 1 ELSE 0 END) AS overdue_tasks
                FROM users u
                LEFT JOIN tasks t ON u.id = t.user_id
                LEFT JOIN status s ON t.status_id = s.id
                WHERE u.is_active = TRUE
                GROUP BY u.id, u.username
                ORDER BY completed_tasks DESC
            """)

            # Create Treeview for report
            columns = ("username", "total_tasks", "completed_tasks", "overdue_tasks", "completion_rate")
            tree = ttk.Treeview(report_window, columns=columns, show="headings")

            tree.heading("username", text="Username")
            tree.heading("total_tasks", text="Total Tasks")
            tree.heading("completed_tasks", text="Completed")
            tree.heading("overdue_tasks", text="Overdue")
            tree.heading("completion_rate", text="Completion %")

            tree.column("username", width=150)
            tree.column("total_tasks", width=80, anchor="center")
            tree.column("completed_tasks", width=100, anchor="center")
            tree.column("overdue_tasks", width=80, anchor="center")
            tree.column("completion_rate", width=80, anchor="center")

            for row in cursor.fetchall():
                user_id, username, total, completed, overdue = row
                completion_rate = round((completed / total) * 100, 1) if total > 0 else 0
                tree.insert("", "end", values=(username, total, completed, overdue, f"{completion_rate}%"))

            tree.pack(fill="both", expand=True, padx=10, pady=10)

            # Close button
            ttk.Button(report_window, text="Close", command=report_window.destroy).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Error generating report:\\n{str(e)}")
            report_window.destroy()

    def project_status_report(self):
        """Project status report (admin)"""
        report_window = tk.Toplevel(self.root)
        report_window.title("Project Status Report")
        report_window.geometry("800x600")

        try:
            cursor = self.db_connection.cursor()

            # Get project stats
            cursor.execute("""
                SELECT
                    p.id, p.name, u.username,
                    COUNT(t.id) AS total_tasks,
                    SUM(CASE WHEN s.name = 'Completed' THEN 1 ELSE 0 END) AS completed_tasks,
                    MIN(t.due_date) AS earliest_due,
                    MAX(t.due_date) AS latest_due
                FROM projects p
                JOIN users u ON p.owner_id = u.id
                LEFT JOIN tasks t ON p.id = t.project_id
                LEFT JOIN status s ON t.status_id = s.id
                GROUP BY p.id, p.name, u.username
                ORDER BY p.created_at DESC
            """)

            # Create Treeview for report
            columns = ("name", "owner", "total_tasks", "completed_tasks", "completion_rate", "earliest_due", "latest_due")
            tree = ttk.Treeview(report_window, columns=columns, show="headings")

            tree.heading("name", text="Project Name")
            tree.heading("owner", text="Owner")
            tree.heading("total_tasks", text="Total Tasks")
            tree.heading("completed_tasks", text="Completed")
            tree.heading("completion_rate", text="Completion %")
            tree.heading("earliest_due", text="Earliest Due")
            tree.heading("latest_due", text="Latest Due")

            tree.column("name", width=200)
            tree.column("owner", width=100)
            tree.column("total_tasks", width=80, anchor="center")
            tree.column("completed_tasks", width=100, anchor="center")
            tree.column("completion_rate", width=80, anchor="center")
            tree.column("earliest_due", width=100, anchor="center")
            tree.column("latest_due", width=100, anchor="center")

            for row in cursor.fetchall():
                project_id, name, owner, total, completed, earliest, latest = row
                completion_rate = round((completed / total) * 100, 1) if total > 0 else 0
                tree.insert("", "end", values=(
                    name, owner, total, completed, f"{completion_rate}%",
                    earliest.strftime("%Y-%m-%d") if earliest else "-",
                    latest.strftime("%Y-%m-%d") if latest else "-"
                ))

            tree.pack(fill="both", expand=True, padx=10, pady=10)

            # Close button
            ttk.Button(report_window, text="Close", command=report_window.destroy).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Error generating report:\\n{str(e)}")
            report_window.destroy()

    def show_user_summary(self):
        """User summary view"""
        summary_frame = ttk.Frame(self.root, padding="20")
        summary_frame.pack(fill="both", expand=True)

        # Project stats
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM projects WHERE owner_id = %s", (self.current_user,))
            my_projects = cursor.fetchone()[0]

            ttk.Label(summary_frame, text=f"Your Projects: {my_projects}", font=('Tahoma', 12)).pack(anchor="w")
        except Exception as e:
            messagebox.showerror("Error", f"Error getting project stats:\\n{str(e)}")

        # Task stats
        try:
            cursor = self.db_connection.cursor()

            # Personal tasks
            cursor.execute("""
                SELECT COUNT(*)
                FROM tasks
                WHERE user_id = %s AND project_id IS NULL
            """, (self.current_user,))
            personal_tasks = cursor.fetchone()[0]

            # Project tasks
            cursor.execute("""
                SELECT COUNT(*)
                FROM tasks
                WHERE user_id = %s AND project_id IS NOT NULL
            """, (self.current_user,))
            project_tasks = cursor.fetchone()[0]

            # Assigned tasks
            cursor.execute("""
                SELECT COUNT(*)
                FROM tasks t
                JOIN projects p ON t.project_id = p.id
                WHERE t.user_id = %s AND p.owner_id != %s
            """, (self.current_user, self.current_user))
            assigned_tasks = cursor.fetchone()[0]

            ttk.Label(summary_frame, text=f"Personal Tasks: {personal_tasks}", font=('Tahoma', 12)).pack(anchor="w")
            ttk.Label(summary_frame, text=f"Project Tasks: {project_tasks}", font=('Tahoma', 12)).pack(anchor="w")
            ttk.Label(summary_frame, text=f"Assigned Tasks: {assigned_tasks}", font=('Tahoma', 12)).pack(anchor="w")

        except Exception as e:
            messagebox.showerror("Error", f"Error getting task stats:\\n{str(e)}")

    def clear_window(self):
        """Clear all widgets from main window"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Clear menu if exists
        if hasattr(self.root, 'menu'):
            self.root.config(menu=None)

    def logout(self):
        """Logout current user"""
        self.current_user = None
        self.user_role = None
        self.setup_login_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
