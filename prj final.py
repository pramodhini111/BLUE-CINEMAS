import os
import mysql.connector
from tkinter import *
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from datetime import datetime, timedelta
import random

DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "2008"
DB_NAME = "blue_cinemas"

BG_IMAGE_PATH = "bg.png"
os.makedirs("tickets", exist_ok=True)
os.makedirs("posters", exist_ok=True)

# For tickets
CINEMA_NAME = "BLUE CINEMA!S"
CINEMA_CONTACT = "contact: bluecinemas@gmail.com | +91 98765 43210"

def get_db_connection():
    """Create and return database connection"""
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

class SeatMap:
    def __init__(self, master, rows=6, cols=8):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.selected_seats = []
        self.seat_buttons = {}
        self.booked_seats = set()
        
        self.create_seat_map()
    
    def create_seat_map(self):
        """Create the seat map interface"""
        # Screen label
        Label(self.master, text="🎬 SCREEN", font=("Arial", 16, "bold"), 
              bg="#000000", fg="white").pack(pady=10)
        
        seat_frame = Frame(self.master, bg="#000000")
        seat_frame.pack(pady=10)
        
        # Create seat buttons
        for row in range(self.rows):
            row_frame = Frame(seat_frame, bg="#000000")
            row_frame.pack()
            
            # Row labels
            Label(row_frame, text=chr(65 + row), font=("Arial", 12, "bold"), 
                  bg="#000000", fg="white", width=3).pack(side=LEFT)
            
            for col in range(1, self.cols + 1):
                seat_num = f"{chr(65 + row)}{col}"
                btn = Button(row_frame, text=seat_num, font=("Arial", 10), 
                           width=4, height=2, bg="lightgreen", relief=RAISED,
                           command=lambda sn=seat_num: self.toggle_seat(sn))
                btn.pack(side=LEFT, padx=2, pady=2)
                self.seat_buttons[seat_num] = btn
    
    def set_booked_seats(self, booked_seats_list):
        """Mark already booked seats as unavailable"""
        self.booked_seats = set(booked_seats_list)
        for seat, btn in self.seat_buttons.items():
            if seat in self.booked_seats:
                btn.config(bg="red", state=DISABLED, relief=SUNKEN)
            else:
                btn.config(bg="lightgreen", state=NORMAL, relief=RAISED)
    
    def toggle_seat(self, seat_num):
        """Toggle seat selection"""
        if seat_num in self.selected_seats:
            self.selected_seats.remove(seat_num)
            self.seat_buttons[seat_num].config(bg="lightgreen", relief=RAISED)
        else:
            self.selected_seats.append(seat_num)
            self.seat_buttons[seat_num].config(bg="orange", relief=SUNKEN)
    
    def get_selected_seats(self):
        """Get comma-separated selected seats"""
        return ",".join(sorted(self.selected_seats))
    
    def clear_selection(self):
        """Clear all seat selections"""
        for seat in self.selected_seats:
            if seat not in self.booked_seats:
                self.seat_buttons[seat].config(bg="lightgreen", relief=RAISED)
        self.selected_seats = []

class BlueCinemasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BLUE CINEMA!S")
        self.root.state("zoomed")
        self.root.resizable(False, False)

        try:
            self.bg_image = Image.open(BG_IMAGE_PATH)
            self.bg_image = self.bg_image.resize(
                (self.root.winfo_screenwidth(), self.root.winfo_screenheight()),
                Image.Resampling.LANCZOS
            )
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        except Exception:
            self.bg_photo = None

        self.canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        if self.bg_photo:
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        else:
            self.canvas.configure(bg="#111111")

        self.current_user = None
        self.show_login_screen()

    # LOGIN SCREEN 
    def show_login_screen(self):
        """Display login screen"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.canvas = Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        if self.bg_photo:
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        else:
            self.canvas.configure(bg="#111111")

        panel_w, panel_h = 520, 420
        panel_x = (self.root.winfo_screenwidth() - panel_w) // 2
        panel_y = (self.root.winfo_screenheight() - panel_h) // 2

        panel = Frame(self.root, bg="#000000", bd=0)
        panel.place(x=panel_x, y=panel_y, width=panel_w, height=panel_h)

        Label(panel, text="BLUE CINEMA!S", font=("Helvetica", 36, "bold"), 
              fg="#ff7f00", bg="#000000").pack(pady=(20, 10))
        
        Label(panel, text="Username:", fg="white", bg="#000000").pack(pady=(10, 0))
        self.entry_username = Entry(panel, font=("Arial", 14))
        self.entry_username.pack(pady=(0, 10))

        Label(panel, text="Password:", fg="white", bg="#000000").pack(pady=(10, 0))
        self.entry_password = Entry(panel, show="*", font=("Arial", 14))
        self.entry_password.pack(pady=(0, 20))

        Button(panel, text="Login", command=self.handle_login, 
               font=("Arial", 14), bg="orange").pack(pady=(5, 10))
        
        Button(panel, text="Don't have an account? Sign up", 
               command=self.show_signup_screen, relief=FLAT, 
               fg="white", bg="#000000").pack()

    # SIGN UP 
    def show_signup_screen(self):
        """Display signup screen"""
        signup = Toplevel(self.root)
        signup.title("Sign Up - BLUE CINEMA!S")
        signup.geometry("420x360")
        signup.resizable(False, False)
        signup.configure(bg="#000000")

        Label(signup, text="Create an Account", font=("Helvetica", 18), 
              fg="orange", bg="#000000").pack(pady=10)
        
        Label(signup, text="Username", fg="white", bg="#000000").pack()
        e_user = Entry(signup, font=("Arial", 12))
        e_user.pack(pady=5)
        
        Label(signup, text="Password", fg="white", bg="#000000").pack()
        e_pass = Entry(signup, show="*", font=("Arial", 12))
        e_pass.pack(pady=5)
        
        Label(signup, text="Email", fg="white", bg="#000000").pack()
        e_email = Entry(signup, font=("Arial", 12))
        e_email.pack(pady=5)

        def do_signup():
            u, p, e = e_user.get().strip(), e_pass.get().strip(), e_email.get().strip()
            if not u or not p:
                messagebox.showerror("Error", "Username and password required.")
                return
            
            if len(p) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters.")
                return
            
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO users (username, password, email, is_admin) VALUES (%s,%s,%s,0)", 
                           (u, p, e))
                conn.commit()
                messagebox.showinfo("Success", "Account created. Please log in.")
                signup.destroy()
            except mysql.connector.IntegrityError:
                messagebox.showerror("Error", "Username already exists.")
            except Exception as e:
                messagebox.showerror("Error", f"Signup failed: {str(e)}")
            finally:
                cur.close()
                conn.close()

        Button(signup, text="Sign Up", command=do_signup, 
               bg="orange", fg="black", font=("Arial", 12)).pack(pady=15)

    # LOGIN HANDLER
    def handle_login(self):
        """Handle user login"""
        u = self.entry_username.get().strip()
        p = self.entry_password.get().strip()
        
        if not u or not p:
            messagebox.showerror("Error", "Enter username and password.")
            return
        
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username=%s", (u,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if not user:
            if messagebox.askyesno("Account not found", "Account doesn't exist. Sign up?"):
                self.show_signup_screen()
            return
        
        if p != user["password"]:
            messagebox.showerror("Error", "Incorrect password.")
            return

        self.current_user = user
        messagebox.showinfo("Welcome", f"Welcome, {user['username']}! 🎬")
        self.show_main_menu()

    # MAIN MENU
    def show_main_menu(self):
        """Display main menu after login"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.canvas = Canvas(self.root, width=self.root.winfo_screenwidth(), 
                           height=self.root.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        
        if self.bg_photo:
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        else:
            self.canvas.configure(bg="#111111")

        # User info frame
        user_frame = Frame(self.root, bg="#000000")
        user_frame.place(x=self.root.winfo_screenwidth() - 320, y=10, width=300, height=60)
        
        Label(user_frame, text=f"User: {self.current_user['username']}", 
              bg="#000000", fg="white", font=("Arial", 12)).pack(anchor="e", padx=10, pady=5)
        
        Button(user_frame, text="Logout", command=self.logout, 
               bg="red", fg="white").pack(anchor="e", padx=10)

        # Main panel
        panel = Frame(self.root, bg="#000000")
        panel.place(x=100, y=140, width=420, height=400)

        Label(panel, text=f"Welcome, {self.current_user['username']}!", 
              font=("Helvetica", 16, "bold"), fg="orange", bg="#000000").pack(pady=(20, 5))
        
        Label(panel, text="What would you like to do?", 
              font=("Helvetica", 12), fg="white", bg="#000000").pack(pady=(0, 15))

        if self.current_user.get("is_admin"):
            # Admin options
            Button(panel, text="🎬 Manage Movies/Shows", width=24, height=2, 
                   command=self.admin_manage_movies, bg="orange", fg="black", 
                   font=("Arial", 12, "bold")).pack(pady=8)
            
            Button(panel, text="📊 View All Bookings", width=24, height=2, 
                   command=self.view_all_bookings, bg="orange", fg="black", 
                   font=("Arial", 12, "bold")).pack(pady=8)
            
            Button(panel, text="💰 Revenue Report", width=24, height=2, 
                   command=self.revenue_report, bg="orange", fg="black", 
                   font=("Arial", 12, "bold")).pack(pady=8)
        else:
            # User options
            Button(panel, text="🎭 Browse & Book", width=24, height=2, 
                   command=self.show_movie_catalog, bg="orange", fg="black", 
                   font=("Arial", 12, "bold")).pack(pady=8)
            
            Button(panel, text="📋 My Bookings", width=24, height=2, 
                   command=self.view_bookings, bg="orange", fg="black", 
                   font=("Arial", 12, "bold")).pack(pady=8)

        Button(panel, text="🚪 Exit", width=24, height=2, command=self.exit_app, 
               bg="red", fg="white", font=("Arial", 12, "bold")).pack(pady=8)

    def logout(self):
        """Logout current user"""
        self.current_user = None
        self.show_login_screen()

    def clear_filters(self, search_var, language_var, genre_var, rating_var, movie_frame):
        """Clear all filters and show all movies"""
        search_var.set("")
        language_var.set("All")
        genre_var.set("All")
        rating_var.set("All")
        self.filter_movies(movie_frame, "", "All", "All", "All")

    def load_movie_poster(self, poster_filename, size=(180, 240)):
        """Load and resize movie poster"""
        try:
            poster_path = os.path.join("posters", poster_filename)
            if os.path.exists(poster_path):
                image = Image.open(poster_path)
                image = image.resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(image)
            else:
                return self.create_default_poster(size)
        except Exception as e:
            print(f"Error loading poster {poster_filename}: {e}")
            return self.create_default_poster(size)

    def create_default_poster(self, size=(180, 240)):
        """Create a default poster when image is missing"""
        image = Image.new('RGB', size, color='#2a2a2a')
        draw = ImageDraw.Draw(image)
        
        center_x, center_y = size[0] // 2, size[1] // 2
        draw.ellipse([center_x-30, center_y-30, center_x+30, center_y+30], 
                    outline='orange', width=3)
        draw.ellipse([center_x-20, center_y-20, center_x+20, center_y+20], 
                    outline='orange', width=2)
        
        try:
            font = ImageFont.load_default()
            draw.text((center_x-25, center_y+40), "NO POSTER", fill='orange', font=font)
        except:
            pass
        
        return ImageTk.PhotoImage(image)

    def filter_movies(self, movie_frame, search_text, language, genre, rating):
        """Filter and display movies based on criteria"""
        for widget in movie_frame.winfo_children():
            widget.destroy()

        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """SELECT id, title, language, genre, duration_minutes, price, 
                          rating, description, poster_filename 
                   FROM movies WHERE 1=1"""
        params = []
        
        if search_text:
            query += " AND (title LIKE %s OR description LIKE %s)"
            params.extend([f"%{search_text}%", f"%{search_text}%"])
        
        if language != "All":
            query += " AND language = %s"
            params.append(language)
        
        if genre != "All":
            query += " AND genre LIKE %s"
            params.append(f"%{genre}%")
        
        if rating != "All":
            query += " AND rating = %s"
            params.append(rating)
        
        query += " ORDER BY title"
        
        cur.execute(query, params)
        movies = cur.fetchall()
        cur.close()
        conn.close()

        if not movies:
            no_results_frame = Frame(movie_frame, bg="#000000")
            no_results_frame.pack(expand=True, fill=BOTH)
            
            Label(no_results_frame, text="🎬 No movies found matching your criteria.", 
                  font=("Arial", 16), fg="white", bg="#000000").pack(expand=True)
            
            Label(no_results_frame, text="Try adjusting your search filters.", 
                  font=("Arial", 12), fg="gray", bg="#000000").pack()
            return

        # Create scrollable canvas
        canvas = Canvas(movie_frame, bg="#000000", highlightthickness=0)
        scrollbar = Scrollbar(movie_frame, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="#000000")

        scrollable_frame.bind("<Configure>", 
                            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.poster_images = []
        
        # Display movies in grid
        for i, movie in enumerate(movies):
            mid, title, lang, movie_genre, duration, price, rating, description, poster_filename = movie
            
            card = Frame(scrollable_frame, bg="#1a1a1a", relief=RAISED, bd=2, 
                        width=320, height=480)
            card.grid(row=i//3, column=i%3, padx=15, pady=15, sticky="nsew")
            card.grid_propagate(False)

            poster_image = self.load_movie_poster(poster_filename)
            self.poster_images.append(poster_image)
            
            poster_label = Label(card, image=poster_image, bg="#1a1a1a")
            poster_label.pack(pady=10)

            title_label = Label(card, text=title, font=("Arial", 14, "bold"), 
                               bg="#1a1a1a", fg="orange", wraplength=280)
            title_label.pack(pady=(0, 5))

            details_frame = Frame(card, bg="#1a1a1a")
            details_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

            info_text = f"🎭 {movie_genre}\n"
            info_text += f"🗣️ {lang} | ⭐ {rating}\n"
            info_text += f"⏱️ {duration} mins\n"
            info_text += f"💰 ₹{price}"
            
            Label(details_frame, text=info_text, font=("Arial", 10), bg="#1a1a1a", 
                  fg="white", justify=LEFT).pack(anchor="w")

            # Truncate description
            desc = description[:80] + "..." if len(description) > 80 else description
            desc_label = Label(details_frame, text=desc, font=("Arial", 9), bg="#1a1a1a", 
                              fg="#cccccc", wraplength=280, justify=LEFT, height=2)
            desc_label.pack(anchor="w", pady=(8, 0))

            Button(card, text="🎟️ Book Tickets", 
                   command=lambda m=mid: self.start_booking_flow(m), 
                   bg="orange", fg="black", font=("Arial", 11, "bold"), 
                   width=20, height=1).pack(pady=10)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

    def start_booking_flow(self, movie_id):
        """Start booking process for selected movie"""
        self.book_tickets_flow(movie_id)

    # MOVIE CATALOG
    def show_movie_catalog(self):
        """Display movie catalog with filtering options"""
        top = Toplevel(self.root)
        top.title("Browse & Book - Movie Catalog")
        top.state('zoomed')
        top.configure(bg="#000000")

        Label(top, text="🎭 Browse & Book Movies", font=("Arial", 24, "bold"), 
              fg="orange", bg="#000000").pack(pady=20)

        # Search and filter frame
        search_frame = Frame(top, bg="#000000")
        search_frame.pack(fill=X, padx=20, pady=10)

        Label(search_frame, text="Search:", font=("Arial", 12, "bold"), 
              fg="white", bg="#000000").pack(side=LEFT, padx=5)
        
        search_var = StringVar()
        search_entry = Entry(search_frame, textvariable=search_var, 
                           font=("Arial", 12), width=25)
        search_entry.pack(side=LEFT, padx=5)
        search_entry.bind('<KeyRelease>', 
                         lambda e: self.filter_movies(movie_frame, search_var.get(), 
                                                     language_var.get(), genre_var.get(), 
                                                     rating_var.get()))

        Label(search_frame, text="Language:", font=("Arial", 12, "bold"), 
              fg="white", bg="#000000").pack(side=LEFT, padx=(20,5))
        
        language_var = StringVar()
        language_combo = ttk.Combobox(search_frame, textvariable=language_var, 
                                    font=("Arial", 10), width=12, state="readonly")
        language_combo['values'] = ('All', 'English', 'Hindi', 'Tamil', 'Telugu', 'Kannada')
        language_combo.set('All')
        language_combo.pack(side=LEFT, padx=5)
        language_combo.bind('<<ComboboxSelected>>', 
                          lambda e: self.filter_movies(movie_frame, search_var.get(), 
                                                      language_var.get(), genre_var.get(), 
                                                      rating_var.get()))

        Label(search_frame, text="Genre:", font=("Arial", 12, "bold"), 
              fg="white", bg="#000000").pack(side=LEFT, padx=(20,5))
        
        genre_var = StringVar()
        genre_combo = ttk.Combobox(search_frame, textvariable=genre_var, 
                                 font=("Arial", 10), width=12, state="readonly")
        genre_combo['values'] = ('All', 'Action', 'Drama', 'Sci-Fi', 'Thriller', 
                                'Comedy', 'Romance', 'Fantasy', 'Adventure')
        genre_combo.set('All')
        genre_combo.pack(side=LEFT, padx=5)
        genre_combo.bind('<<ComboboxSelected>>', 
                       lambda e: self.filter_movies(movie_frame, search_var.get(), 
                                                   language_var.get(), genre_var.get(), 
                                                   rating_var.get()))

        Label(search_frame, text="Rating:", font=("Arial", 12, "bold"), 
              fg="white", bg="#000000").pack(side=LEFT, padx=(20,5))
        
        rating_var = StringVar()
        rating_combo = ttk.Combobox(search_frame, textvariable=rating_var, 
                                  font=("Arial", 10), width=8, state="readonly")
        rating_combo['values'] = ('All', 'U', 'UA', 'A', 'PG-13', 'R')
        rating_combo.set('All')
        rating_combo.pack(side=LEFT, padx=5)
        rating_combo.bind('<<ComboboxSelected>>', 
                        lambda e: self.filter_movies(movie_frame, search_var.get(), 
                                                    language_var.get(), genre_var.get(), 
                                                    rating_var.get()))

        Button(search_frame, text="🔄 Clear Filters", 
               command=lambda: self.clear_filters(search_var, language_var, 
                                                genre_var, rating_var, movie_frame), 
               bg="gray", fg="white", font=("Arial", 10)).pack(side=LEFT, padx=10)

        movie_frame = Frame(top, bg="#000000")
        movie_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        self.filter_movies(movie_frame, "", "All", "All", "All")

    # VIEW BOOKINGS 
    def view_bookings(self):
        """Display user's previous bookings"""
        top = Toplevel(self.root)
        top.title("Your Bookings")
        top.state('zoomed')
        top.configure(bg="#000000")

        Label(top, text="Your Previous Bookings", font=("Arial", 24, "bold"), 
              fg="orange", bg="#000000").pack(pady=20)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """SELECT id, movie_title, show_date, show_time, seats, ntickets, 
                      booking_date, total_price 
             FROM bookings WHERE username=%s ORDER BY booking_date DESC""",
            (self.current_user["username"],)
        )
        bookings = cur.fetchall()
        cur.close()
        conn.close()

        if not bookings:
            Label(top, text="No previous bookings found.", font=("Arial", 18), 
                  fg="white", bg="#000000").pack(pady=40)
            
            Button(top, text="Close", command=top.destroy, bg="gray", 
                   fg="white", font=("Arial", 12), width=15, height=1).pack(pady=10)
            return

        cols = ("Booking ID", "Movie", "Date", "Time", "Seats", "Tickets", "Booked At", "Total (₹)")
        tree = ttk.Treeview(top, columns=cols, show="headings")
        
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=160, anchor="center")
        
        tree.pack(fill="both", expand=True, padx=30, pady=20)

        for b in bookings:
            tree.insert("", "end", values=b)

        Button(top, text="Close", command=top.destroy, bg="gray", 
               fg="white", font=("Arial", 12), width=15, height=1).pack(pady=10)

    # BOOK TICKETS
    def book_tickets_flow(self, pre_selected_movie_id=None):
        """Complete booking flow with seat selection"""
        top = Toplevel(self.root)
        top.title("Book Tickets")
        top.state('zoomed')
        top.configure(bg="#000000")

        Label(top, text="Book Tickets", font=("Arial", 30, "bold"), 
              fg="orange", bg="#000000").pack(pady=20)

        # Main container
        main_container = Frame(top, bg="#000000")
        main_container.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Left frame - movies list
        left_frame = Frame(main_container, bg="#000000")
        left_frame.pack(side=LEFT, fill=Y, padx=10)

        Label(left_frame, text="Select a Movie:", font=("Arial", 16), 
              bg="#000000", fg="white").pack(pady=(0,10))
        
        movie_listbox = Listbox(left_frame, width=40, height=12, font=("Arial", 14))
        movie_listbox.pack()

        # Middle frame - shows list
        middle_frame = Frame(main_container, bg="#000000")
        middle_frame.pack(side=LEFT, fill=Y, padx=10)

        Label(middle_frame, text="Available Shows:", font=("Arial", 16), 
              bg="#000000", fg="white").pack(pady=(0,10))
        
        shows_tree = ttk.Treeview(middle_frame, columns=("id","date","time","available"), 
                                show="headings", height=10)
        shows_tree.heading("id", text="Show ID")
        shows_tree.heading("date", text="Date")
        shows_tree.heading("time", text="Time")
        shows_tree.heading("available", text="Available")
        
        shows_tree.column("id", width=80, anchor="center")
        shows_tree.column("date", width=120, anchor="center")
        shows_tree.column("time", width=120, anchor="center")
        shows_tree.column("available", width=120, anchor="center")
        shows_tree.pack()

        # Right frame - seats and booking controls
        right_frame = Frame(main_container, bg="#000000")
        right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        # Seat map frame
        seat_map_frame = Frame(right_frame, bg="#000000")
        seat_map_frame.pack(fill=BOTH, expand=True)
        
        # Initialize seat map
        self.seat_map = None
        self.current_show_id = None

        # Booking info frame
        info_frame = Frame(right_frame, bg="#000000")
        info_frame.pack(fill=X, pady=10)

        Label(info_frame, text="Selected Seats:", font=("Arial", 14), 
              bg="#000000", fg="white").pack()
        
        self.seats_display = Label(info_frame, text="None", font=("Arial", 14, "bold"), 
                                 bg="#000000", fg="orange")
        self.seats_display.pack()

        Label(info_frame, text="Total Price:", font=("Arial", 14), 
              bg="#000000", fg="white").pack()
        
        self.price_display = Label(info_frame, text="₹0", font=("Arial", 16, "bold"), 
                                 bg="#000000", fg="green")
        self.price_display.pack()

        # Control buttons
        btn_frame = Frame(right_frame, bg="#000000")
        btn_frame.pack(pady=10)

        Button(btn_frame, text="Confirm Booking", font=("Arial", 14, "bold"), 
               bg="orange", fg="black", 
               command=lambda: self.confirm_booking(top)).pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="Clear Selection", font=("Arial", 12), 
               bg="gray", fg="white", 
               command=self.clear_seat_selection).pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="Close", font=("Arial", 12), 
               bg="red", fg="white", command=top.destroy).pack(side=LEFT, padx=5)

        # Load movies from database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title FROM movies ORDER BY title")
        movies = cur.fetchall()
        cur.close()
        conn.close()

        for m in movies:
            movie_listbox.insert(END, f"{m[0]} | {m[1]}")

        # Pre-select movie if provided
        if pre_selected_movie_id:
            for i in range(movie_listbox.size()):
                if movie_listbox.get(i).startswith(f"{pre_selected_movie_id} |"):
                    movie_listbox.selection_set(i)
                    break

        def load_shows(event=None):
            """Load shows for selected movie"""
            # Clear existing seat map
            if self.seat_map:
                self.seat_map.master.pack_forget()
            
            for row in shows_tree.get_children():
                shows_tree.delete(row)

            sel = movie_listbox.curselection()
            if not sel:
                return
            
            idx = sel[0]
            movie_entry = movie_listbox.get(idx)
            movie_id = int(movie_entry.split("|")[0].strip())

            conn2 = get_db_connection()
            cur2 = conn2.cursor()
            
            # Only show future shows (current date and time or later)
            cur2.execute("""SELECT id, show_date, show_time, seats_total, seats_booked 
                          FROM shows 
                          WHERE movie_id=%s AND CONCAT(show_date, ' ', show_time) >= %s
                          ORDER BY show_date, show_time""", 
                        (movie_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            
            shows = cur2.fetchall()
            cur2.close()
            conn2.close()

            if not shows:
                shows_tree.insert("", "end", values=("", "No shows available", "", ""))
                return

            for s in shows:
                sid, sdate, stime, total, booked = s
                available = total - booked
                shows_tree.insert("", "end", values=(sid, str(sdate), str(stime), available))

        def on_show_select(event):
            """Handle show selection"""
            selection = shows_tree.selection()
            if not selection:
                return
            
            show_item = shows_tree.item(selection[0])['values']
            try:
                show_id = int(show_item[0])
                self.current_show_id = show_id
                self.load_seat_map(seat_map_frame, show_id)
            except Exception as e:
                print("Error loading seat map:", e)

        def update_seat_display():
            """Update seat selection display and price"""
            if self.seat_map:
                selected_seats = self.seat_map.get_selected_seats()
                self.seats_display.config(text=selected_seats if selected_seats else "None")
                
                # Calculate price
                if selected_seats:
                    num_tickets = len(self.seat_map.selected_seats)
                    # Get movie price
                    conn = get_db_connection()
                    cur = conn.cursor()
                    try:
                        movie_sel = movie_listbox.curselection()
                        if movie_sel:
                            movie_entry = movie_listbox.get(movie_sel[0])
                            movie_id = int(movie_entry.split("|")[0].strip())
                            cur.execute("SELECT price FROM movies WHERE id=%s", (movie_id,))
                            price = float(cur.fetchone()[0])
                            total = price * num_tickets
                            self.price_display.config(text=f"₹{total:.2f}")
                    except Exception as e:
                        print("Error calculating price:", e)
                    finally:
                        cur.close()
                        conn.close()
                else:
                    self.price_display.config(text="₹0")

        # Bind events
        movie_listbox.bind("<<ListboxSelect>>", load_shows)
        shows_tree.bind("<<TreeviewSelect>>", on_show_select)
        
        # Store update function for seat map to use
        self.update_seat_display = update_seat_display

    def load_seat_map(self, parent_frame, show_id):
        """Load and display the seat map for a given show"""
        # Clear previous seat map
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # Get booked seats for this show
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT seats FROM bookings WHERE show_id=%s", (show_id,))
        booked_seats = []
        for row in cur.fetchall():
            if row[0]:
                booked_seats.extend([s.strip() for s in row[0].split(',')])
        cur.close()
        conn.close()

        # Create new seat map
        self.seat_map = SeatMap(parent_frame)
        self.seat_map.set_booked_seats(booked_seats)
        
        # Override the toggle_seat method to include price update
        original_toggle = self.seat_map.toggle_seat
        
        def new_toggle(seat_num):
            original_toggle(seat_num)
            self.update_seat_display()
        
        self.seat_map.toggle_seat = new_toggle

    def clear_seat_selection(self):
        """Clear all seat selections"""
        if self.seat_map:
            self.seat_map.clear_selection()
            self.update_seat_display()

    def confirm_booking(self, top_window):
        """Confirm and process booking"""
        if not self.seat_map or not self.seat_map.selected_seats:
            messagebox.showerror("Error", "Please select at least one seat.")
            return

        if not self.current_show_id:
            messagebox.showerror("Error", "Please select a show.")
            return

        selected_seats = self.seat_map.get_selected_seats()
        num_tickets = len(self.seat_map.selected_seats)

        # Get movie details
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            # Get show and movie details
            cur.execute("SELECT movie_id, show_date, show_time, seats_booked FROM shows WHERE id=%s", 
                       (self.current_show_id,))
            show_data = cur.fetchone()
            
            if not show_data:
                messagebox.showerror("Error", "Show not found.")
                return

            movie_id, show_date, show_time, seats_booked = show_data
            
            cur.execute("SELECT title, price FROM movies WHERE id=%s", (movie_id,))
            movie_data = cur.fetchone()
            
            if not movie_data:
                messagebox.showerror("Error", "Movie not found.")
                return

            movie_title, price = movie_data
            total_price = price * num_tickets
            booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Update seats_booked and insert booking
            new_booked = seats_booked + num_tickets
            cur.execute("UPDATE shows SET seats_booked=%s WHERE id=%s", 
                       (new_booked, self.current_show_id))
            
            cur.execute(
                """INSERT INTO bookings (username, movie_title, show_date, show_time, 
                          seats, ntickets, booking_date, total_price, show_id) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (self.current_user["username"], movie_title, show_date, str(show_time), 
                 selected_seats, num_tickets, booking_date, total_price, self.current_show_id)
            )
            
            conn.commit()
            booking_id = cur.lastrowid

            # Generate ticket
            self.generate_ticket(booking_id, movie_title, show_date, show_time, 
                               selected_seats, num_tickets, total_price, booking_date)

            messagebox.showinfo("Success", 
                              f"Booking confirmed!\nSeats: {selected_seats}\nTotal: ₹{total_price:.2f}")
            top_window.destroy()

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Booking failed: {str(e)}")
        finally:
            cur.close()
            conn.close()

    def generate_ticket(self, booking_id, movie_title, show_date, show_time, 
                       seats, num_tickets, total_price, booking_date):
        """Generate a ticket file"""
        ticket_filename = f"tickets/ticket_{self.current_user['username']}_{booking_id}.txt"
        
        with open(ticket_filename, "w", encoding="utf-8") as f:
            f.write(f"{CINEMA_NAME}\n")
            f.write(f"{'-'*40}\n")
            f.write(f"Booking ID : {booking_id}\n")
            f.write(f"Username   : {self.current_user['username']}\n")
            f.write(f"Movie      : {movie_title}\n")
            f.write(f"Date       : {show_date}\n")
            f.write(f"Time       : {show_time}\n")
            f.write(f"Seats      : {seats}\n")
            f.write(f"No. Tickets: {num_tickets}\n")
            f.write(f"Total Paid : ₹{total_price:.2f}\n")
            f.write(f"Booked On  : {booking_date}\n")
            f.write(f"{'-'*40}\n")
            f.write(f"{CINEMA_CONTACT}\n")
            f.write("Thank you for choosing Blue Cinema!S\n")

    # ADMIN FEATURES
    def view_all_bookings(self):
        """Admin view of all bookings"""
        top = Toplevel(self.root)
        top.title("All Bookings")
        top.state('zoomed')
        top.configure(bg="#000000")

        Label(top, text="All Bookings", font=("Arial", 24, "bold"), 
              fg="orange", bg="#000000").pack(pady=20)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """SELECT id, username, movie_title, show_date, show_time, seats, 
                      ntickets, booking_date, total_price 
             FROM bookings ORDER BY booking_date DESC"""
        )
        bookings = cur.fetchall()
        cur.close()
        conn.close()

        if not bookings:
            Label(top, text="No bookings found.", font=("Arial", 18), 
                  fg="white", bg="#000000").pack(pady=40)
        else:
            cols = ("ID", "User", "Movie", "Date", "Time", "Seats", "Tickets", "Booked At", "Total (₹)")
            tree = ttk.Treeview(top, columns=cols, show="headings")
            
            for c in cols:
                tree.heading(c, text=c)
                tree.column(c, width=140, anchor="center")
            
            tree.pack(fill="both", expand=True, padx=30, pady=20)

            for b in bookings:
                tree.insert("", "end", values=b)

        Button(top, text="Close", command=top.destroy, bg="gray", 
               fg="white", font=("Arial", 12), width=15, height=1).pack(pady=10)

    def revenue_report(self):
        """Admin revenue report"""
        top = Toplevel(self.root)
        top.title("Revenue Report")
        top.geometry("600x400")
        top.configure(bg="#000000")

        Label(top, text="Revenue Report", font=("Arial", 24, "bold"), 
              fg="orange", bg="#000000").pack(pady=20)

        conn = get_db_connection()
        cur = conn.cursor()
        
        # Total revenue
        cur.execute("SELECT SUM(total_price) FROM bookings")
        total_revenue = cur.fetchone()[0] or 0
        
        # Revenue by movie
        cur.execute("""SELECT movie_title, SUM(total_price) 
                     FROM bookings GROUP BY movie_title 
                     ORDER BY SUM(total_price) DESC""")
        movie_revenue = cur.fetchall()
        
        # Recent bookings count
        cur.execute("""SELECT COUNT(*) FROM bookings 
                     WHERE booking_date >= CURDATE() - INTERVAL 7 DAY""")
        recent_bookings = cur.fetchone()[0]
        
        cur.close()
        conn.close()

        report_frame = Frame(top, bg="#000000")
        report_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        Label(report_frame, text=f"Total Revenue: ₹{total_revenue:.2f}", 
              font=("Arial", 16, "bold"), fg="green", bg="#000000").pack(pady=10)
        
        Label(report_frame, text=f"Bookings (Last 7 days): {recent_bookings}", 
              font=("Arial", 14), fg="white", bg="#000000").pack(pady=5)

        Label(report_frame, text="Revenue by Movie:", font=("Arial", 14, "bold"), 
              fg="orange", bg="#000000").pack(pady=10)

        for movie, revenue in movie_revenue:
            Label(report_frame, text=f"{movie}: ₹{revenue:.2f}", 
                  font=("Arial", 12), fg="white", bg="#000000").pack()

        Button(top, text="Close", command=top.destroy, bg="gray", fg="white", 
               font=("Arial", 12), width=15, height=1).pack(pady=10)

    def admin_manage_movies(self):
        """Admin panel for managing movies and shows"""
        admin_win = Toplevel(self.root)
        admin_win.title("Admin - Manage Movies & Shows")
        admin_win.geometry("950x550")
        admin_win.configure(bg="#000000")

        # Left frame for movies list
        left = Frame(admin_win, bg="#000000")
        left.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        Label(left, text="Movies", font=("Helvetica", 16, "bold"), 
              fg="orange", bg="#000000").pack(pady=6)
    
        # Treeview for movies
        tree = ttk.Treeview(left, columns=("id", "title", "lang", "dur", "price", "rating"), 
                          show="headings")
        
        for col in ("id", "title", "lang", "dur", "price", "rating"):
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=120)
        
        tree.pack(fill=BOTH, expand=True)

        def load_movies():
            """Load movies into treeview"""
            tree.delete(*tree.get_children())
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, title, language, duration_minutes, price, rating FROM movies")
            
            for r in cur.fetchall():
                tree.insert("", "end", values=r)
            
            cur.close()
            conn.close()

        load_movies()

        def add_movie():
            """Add new movie dialog"""
            mwin = Toplevel(admin_win)
            mwin.title("Add Movie")
            mwin.geometry("420x360")
            mwin.configure(bg="#000000")
        
            Label(mwin, text="Add Movie", font=("Helvetica", 14, "bold"), 
                  fg="orange", bg="#000000").pack(pady=8)
        
            entries = {}
            fields = ["Title", "Language", "Duration (min)", "Price (₹)", "Rating"]
        
            for label in fields:
                Label(mwin, text=label, fg="white", bg="#000000").pack()
                e = Entry(mwin, font=("Arial", 12))
                e.pack(pady=2)
                entries[label] = e

            def do_add():
                """Execute movie addition"""
                try:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("""INSERT INTO movies (title, language, duration_minutes, price, rating) 
                                VALUES (%s,%s,%s,%s,%s)""",
                                (entries["Title"].get(), 
                                 entries["Language"].get(), 
                                 int(entries["Duration (min)"].get()), 
                                 float(entries["Price (₹)"].get()), 
                                 entries["Rating"].get()))
                    conn.commit()
                    cur.close()
                    conn.close()
                    load_movies()
                    mwin.destroy()
                    messagebox.showinfo("Success", "Movie added successfully!")
                except Exception as ex:
                    messagebox.showerror("Error", f"Failed to add movie: {str(ex)}")

            Button(mwin, text="Add Movie", command=do_add, 
                   bg="orange", fg="black", font=("Arial", 12)).pack(pady=12)

        def edit_movie():
            """Edit selected movie"""
            sel = tree.selection()
            if not sel:
                messagebox.showerror("Error", "Please select a movie first.")
                return
        
            item = tree.item(sel[0])
            mid, title, lang, dur, price, rating = item['values']
        
            mwin = Toplevel(admin_win)
            mwin.title("Edit Movie")
            mwin.geometry("420x360")
            mwin.configure(bg="#000000")
        
            Label(mwin, text="Edit Movie", font=("Helvetica", 14, "bold"), 
                  fg="orange", bg="#000000").pack(pady=8)

            # Create entry fields with current values
            Label(mwin, text="Title:", fg="white", bg="#000000").pack()
            e1 = Entry(mwin, font=("Arial", 12))
            e1.insert(0, title)
            e1.pack(pady=2)

            Label(mwin, text="Language:", fg="white", bg="#000000").pack()
            e2 = Entry(mwin, font=("Arial", 12))
            e2.insert(0, lang)
            e2.pack(pady=2)

            Label(mwin, text="Duration (min):", fg="white", bg="#000000").pack()
            e3 = Entry(mwin, font=("Arial", 12))
            e3.insert(0, dur)
            e3.pack(pady=2)

            Label(mwin, text="Price (₹):", fg="white", bg="#000000").pack()
            e4 = Entry(mwin, font=("Arial", 12))
            e4.insert(0, price)
            e4.pack(pady=2)

            Label(mwin, text="Rating:", fg="white", bg="#000000").pack()
            e5 = Entry(mwin, font=("Arial", 12))
            e5.insert(0, rating)
            e5.pack(pady=2)

            def do_edit():
                """Execute movie update"""
                try:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("""UPDATE movies SET title=%s, language=%s, 
                                duration_minutes=%s, price=%s, rating=%s WHERE id=%s""",
                                (e1.get(), e2.get(), int(e3.get()), float(e4.get()), e5.get(), mid))
                    conn.commit()
                    cur.close()
                    conn.close()
                    load_movies()
                    mwin.destroy()
                    messagebox.showinfo("Success", "Movie updated successfully!")
                except Exception as ex:
                    messagebox.showerror("Error", f"Failed to update movie: {str(ex)}")

            Button(mwin, text="Save Changes", command=do_edit, 
                   bg="orange", fg="black", font=("Arial", 12)).pack(pady=10)

        def delete_movie():
            """Delete selected movie"""
            sel = tree.selection()
            if not sel:
                messagebox.showerror("Error", "Please select a movie first.")
                return
        
            mid = tree.item(sel[0])['values'][0]
            movie_title = tree.item(sel[0])['values'][1]
        
            if not messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete '{movie_title}' and all its shows?"):
                return
        
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                # Delete shows first (due to foreign key constraints)
                cur.execute("DELETE FROM shows WHERE movie_id=%s", (mid,))
                # Then delete the movie
                cur.execute("DELETE FROM movies WHERE id=%s", (mid,))
                conn.commit()
                messagebox.showinfo("Success", "Movie and its shows deleted successfully!")
                load_movies()
            except Exception as ex:
                conn.rollback()
                messagebox.showerror("Error", f"Failed to delete movie: {str(ex)}")
            finally:
                cur.close()
                conn.close()

        # Right side: show management
        right = Frame(admin_win, bg="#000000")
        right.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
    
        Label(right, text="Manage Shows", font=("Helvetica", 14, "bold"), 
              fg="orange", bg="#000000").pack(pady=6)
        
        Label(right, text="Select a movie first, then click 'Manage Shows'", 
              font=("Helvetica", 10), fg="white", bg="#000000").pack(pady=2)

        def manage_shows():
            """Manage shows for selected movie"""
            sel = tree.selection()
            if not sel:
                messagebox.showerror("Error", "Please select a movie first.")
                return
        
            mid = tree.item(sel[0])['values'][0]
            title = tree.item(sel[0])['values'][1]
        
            swin = Toplevel(admin_win)
            swin.title(f"Shows for {title}")
            swin.geometry("700x420")
            swin.configure(bg="#000000")
        
            Label(swin, text=f"Shows for: {title}", font=("Helvetica", 16, "bold"), 
                  fg="orange", bg="#000000").pack(pady=10)

            # Treeview for shows
            t = ttk.Treeview(swin, columns=("id","date","time","total","booked"), 
                           show="headings")
            
            for c in ("id","date","time","total","booked"):
                t.heading(c, text=c.capitalize())
                t.column(c, width=120)
            
            t.pack(fill=BOTH, expand=True, padx=10, pady=10)

            def load_shows():
                """Load shows into treeview"""
                t.delete(*t.get_children())
                conn = get_db_connection()
                cur = conn.cursor()
                
                # Only show future shows
                cur.execute("""SELECT id, show_date, show_time, seats_total, seats_booked 
                            FROM shows 
                            WHERE movie_id=%s AND CONCAT(show_date, ' ', show_time) >= %s
                            ORDER BY show_date, show_time""", 
                          (mid, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                
                for r in cur.fetchall():
                    t.insert("", "end", values=r)
                
                cur.close()
                conn.close()

            load_shows()

            def add_show():
                """Add new show dialog"""
                win = Toplevel(swin)
                win.title("Add Show")
                win.geometry("320x260")
                win.configure(bg="#000000")
            
                Label(win, text="Add New Show", font=("Helvetica", 12, "bold"), 
                      fg="orange", bg="#000000").pack(pady=8)
            
                Label(win, text="Date (YYYY-MM-DD)", fg="white", bg="#000000").pack()
                e1 = Entry(win, font=("Arial", 12))
                e1.pack(pady=2)
            
                Label(win, text="Time (HH:MM:SS)", fg="white", bg="#000000").pack()
                e2 = Entry(win, font=("Arial", 12))
                e2.pack(pady=2)
            
                Label(win, text="Total Seats", fg="white", bg="#000000").pack()
                e3 = Entry(win, font=("Arial", 12))
                e3.insert(0, "100")  # Default value
                e3.pack(pady=2)

                def do_add_show():
                    """Execute show addition"""
                    try:
                        conn = get_db_connection()
                        cur = conn.cursor()
                        cur.execute("""INSERT INTO shows (movie_id, show_date, show_time, 
                                    seats_total, seats_booked) VALUES (%s,%s,%s,%s,0)""",
                                    (mid, e1.get(), e2.get(), int(e3.get())))
                        conn.commit()
                        cur.close()
                        conn.close()
                        load_shows()
                        win.destroy()
                        messagebox.showinfo("Success", "Show added successfully!")
                    except Exception as ex:
                        messagebox.showerror("Error", f"Failed to add show: {str(ex)}")

                Button(win, text="Add Show", command=do_add_show, 
                       bg="orange", fg="black").pack(pady=10)

            def delete_show():
                """Delete selected show"""
                sel = t.selection()
                if not sel:
                    messagebox.showerror("Error", "Please select a show first.")
                    return
            
                sid = t.item(sel[0])['values'][0]
                show_date = t.item(sel[0])['values'][1]
                show_time = t.item(sel[0])['values'][2]
            
                if not messagebox.askyesno("Confirm Delete", 
                                         f"Delete show on {show_date} at {show_time}?"):
                    return
            
                conn = get_db_connection()
                cur = conn.cursor()
                try:
                    cur.execute("DELETE FROM shows WHERE id=%s", (sid,))
                    conn.commit()
                    load_shows()
                    messagebox.showinfo("Success", "Show deleted successfully!")
                except Exception as ex:
                    conn.rollback()
                    messagebox.showerror("Error", f"Failed to delete show: {str(ex)}")
                finally:
                    cur.close()
                    conn.close()

            # Buttons for show management
            btn_frame = Frame(swin, bg="#000000")
            btn_frame.pack(pady=10)
        
            Button(btn_frame, text="Add Show", command=add_show, 
                   bg="orange", fg="black").pack(side=LEFT, padx=8)
            
            Button(btn_frame, text="Delete Show", command=delete_show, 
                   bg="red", fg="white").pack(side=LEFT, padx=8)

        # Admin controls
        btn_frame = Frame(admin_win, bg="#000000")
        btn_frame.pack(side=BOTTOM, fill=X, padx=8, pady=8)
    
        Button(btn_frame, text="Add Movie", command=add_movie, 
               bg="orange", fg="black").pack(side=LEFT, padx=6)
        
        Button(btn_frame, text="Edit Movie", command=edit_movie, 
               bg="orange", fg="black").pack(side=LEFT, padx=6)
        
        Button(btn_frame, text="Delete Movie", command=delete_movie, 
               bg="red", fg="white").pack(side=LEFT, padx=6)
        
        Button(btn_frame, text="Manage Shows", command=manage_shows, 
               bg="orange", fg="black").pack(side=LEFT, padx=6)
        
        Button(btn_frame, text="Refresh", command=load_movies, 
               bg="gray", fg="white").pack(side=LEFT, padx=6)

    def exit_app(self):
        """Exit the application"""
        self.root.destroy()

if __name__ == "__main__":
    try:
        # Test database connection
        conn = get_db_connection()
        conn.close()
        print("Database connection successful!")
    except Exception as e:
        print("Database connection failed:", e)
        messagebox.showerror("Database Error", 
                           "Cannot connect to database. Please check your MySQL server.")
        raise SystemExit

    root = Tk()
    app = BlueCinemasApp(root)
root.mainloop()
