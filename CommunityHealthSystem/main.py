import customtkinter as ctk
from tkinter import messagebox, Toplevel
import random
import time

# ================= THEME =================
NAVY = "#0B1F3B"
CARD = "#132A46"
ACCENT = "#18C6C9"

ctk.set_appearance_mode("Dark")

# ================= 30 PATIENTS WITH AGE & PHONE =================
names = [
    "Aisha Conteh", "Ibrahim Kamara", "Fatmata Koroma", "Musa Bangura", "Hawa Jalloh",
    "Saidu Turay", "Mariama Kargbo", "Abdul Sesay", "Zainab Kamara", "Foday Conteh",
    "Isatu Bangura", "Alhaji Koroma", "Bintu Jalloh", "Komba Turay", "Salamatu Kamara",
    "Isha Sesay", "Mohamed Kargbo", "Aminata Conteh", "Brima Bangura", "Hassan Jalloh",
    "Omaru Koroma", "Fatu Kamara", "Sulaiman Sesay", "Adama Turay", "Ibrahim Kargbo",
    "Nancy Conteh", "Joseph Kamara", "Sarah Bangura", "David Sesay", "Linda Turay"
]

patients = []
statuses = ["Active", "Critical", "Pending", "Under Review"]
phone_prefixes = ["076", "077", "078", "030", "088", "025"]

for i in range(30):
    rand_phone = f"{random.choice(phone_prefixes)}-{random.randint(100000, 999999)}"
    patients.append({
        "id": f"P-{1000 + i}",
        "name": names[i],
        "age": random.randint(18, 70),
        "phone": rand_phone,
        "status": random.choice(statuses)
    })

audit_log = []
appointments = []


# ================= APP =================
class CHERS(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CHERS Hospital OS v2.5")
        self.geometry("1280x720")
        self.configure(fg_color=NAVY)

        self.user = "Guest"
        self.role = "Admin"

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.login_screen()

    # ================= UTIL =================
    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    def log(self, text):
        audit_log.append(f"{time.strftime('%H:%M:%S')} | {text}")

    def add_top_bar(self):
        top_bar = ctk.CTkFrame(self.container, height=50, fg_color="#081a2f", corner_radius=0)
        top_bar.pack(side="top", fill="x")

        back_btn = ctk.CTkButton(
            top_bar,
            text="← Back to Dashboard",
            fg_color="transparent",
            hover_color=CARD,
            text_color=ACCENT,
            command=self.dashboard,
            width=150
        )
        back_btn.pack(side="left", padx=10, pady=10)

    # ================= LOGIN =================
    def login_screen(self):
        self.clear()

        box = ctk.CTkFrame(self.container, fg_color=CARD, corner_radius=20)
        box.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(box, text="CHERS LOGIN", font=("Arial", 26, "bold")).pack(pady=10)

        u = ctk.CTkEntry(box, placeholder_text="Username", width=200)
        u.pack(pady=5)

        p = ctk.CTkEntry(box, placeholder_text="Password", show="*", width=200)
        p.pack(pady=5)

        def forgot_window():
            win = Toplevel(self)
            win.title("Forgot Password")
            win.geometry("350x250")
            win.configure(bg=NAVY)

            name_ent = ctk.CTkEntry(win, placeholder_text="Full Name")
            name_ent.pack(pady=10)

            role_ent = ctk.CTkEntry(win, placeholder_text="Role (Admin/Doctor/Nurse)")
            role_ent.pack(pady=10)

            pid_ent = ctk.CTkEntry(win, placeholder_text="User ID")
            pid_ent.pack(pady=10)

            def submit():
                self.log(
                    f"Password reset request: {name_ent.get()} | {role_ent.get()} | {pid_ent.get()} | UNDER REVIEW")
                messagebox.showinfo("Submitted", "Request sent for review")
                win.destroy()

            ctk.CTkButton(win, text="Submit", command=submit, fg_color=ACCENT).pack(pady=10)

        ctk.CTkButton(box, text="Forgot Password?", fg_color="transparent", text_color="gray",
                      command=forgot_window).pack()

        def login():
            self.user = u.get() or "Guest"
            self.log(f"{self.user} logged in")
            self.dashboard()

        ctk.CTkButton(box, text="LOGIN", fg_color=ACCENT, text_color="black", font=("Arial", 14, "bold"),
                      command=login).pack(pady=10)

    # ================= DASHBOARD =================
    def dashboard(self):
        self.clear()

        side = ctk.CTkFrame(self.container, width=220, fg_color="#081a2f", corner_radius=0)
        side.pack(side="left", fill="y")

        main = ctk.CTkFrame(self.container, fg_color="transparent")
        main.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(side, text="CHERS Navigation", font=("Arial", 16, "bold"), text_color="white").pack(pady=15)
        ctk.CTkButton(side, text="Dashboard", fg_color=CARD, command=self.dashboard).pack(fill="x", pady=2, padx=5)
        ctk.CTkButton(side, text="Patients Records", command=self.patients_page).pack(fill="x", pady=2, padx=5)
        ctk.CTkButton(side, text="Appointments", command=self.appointment_page).pack(fill="x", pady=2, padx=5)
        ctk.CTkButton(side, text="Audit Log", command=self.audit_page).pack(fill="x", pady=2, padx=5)

        ctk.CTkButton(side, text="🚨 Emergency Alert", fg_color="#C0392B", hover_color="#962D22",
                      command=self.emergency).pack(side="bottom", fill="x", pady=10, padx=5)

        ctk.CTkLabel(main, text=f"Welcome back, {self.user}", font=("Arial", 24, "bold"), text_color="white").pack(
            anchor="w", pady=(0, 10))
        ctk.CTkLabel(main, text=f"Total Dynamic Patients Registered: {len(patients)}", font=("Arial", 14)).pack(
            anchor="w")

        chart = ctk.CTkFrame(main, fg_color=CARD, corner_radius=12)
        chart.pack(fill="x", pady=20, ipady=10)

        ctk.CTkLabel(chart, text="Patient Status Case Volume Distribution", font=("Arial", 14, "bold"),
                     text_color=ACCENT).pack(anchor="w", padx=15, pady=10)

        def bar(label, value, color):
            row = ctk.CTkFrame(chart, fg_color="transparent")
            row.pack(fill="x", pady=5, padx=15)
            ctk.CTkLabel(row, text=label, width=100, anchor="w").pack(side="left")

            progress_val = value / len(patients) if patients else 0
            bar_line = ctk.CTkProgressBar(row, progress_color=color)
            bar_line.set(progress_val)
            bar_line.pack(side="left", fill="x", expand=True, padx=10)

            ctk.CTkLabel(row, text=str(value), font=("Arial", 12, "bold")).pack(side="right")

        active = sum(1 for p in patients if p["status"] == "Active")
        critical = sum(1 for p in patients if p["status"] == "Critical")
        pending = sum(1 for p in patients if p["status"] == "Pending")
        review = sum(1 for p in patients if p["status"] == "Under Review")

        bar("Active", active, "#2ECC71")
        bar("Critical", critical, "#E74C3C")
        bar("Pending", pending, "#F1C40F")
        bar("Under Review", review, "#3498DB")

    # ================= PATIENTS (WITH LIVE SEARCH) =================
    def patients_page(self):
        self.clear()
        self.add_top_bar()

        # Header Frame for Title and Search Bar
        header_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)

        title_lbl = ctk.CTkLabel(header_frame, text="Patient Directory Management", font=("Arial", 20, "bold"),
                                 text_color="white")
        title_lbl.pack(side="left")

        # Live Search Field Entry
        search_var = ctk.StringVar()
        search_bar = ctk.CTkEntry(header_frame, placeholder_text="🔍 Search by Name or ID...", width=300,
                                  textvariable=search_var)
        search_bar.pack(side="right", padx=10)

        # Scrollable area where row elements live
        scroll_box = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll_box.pack(fill="both", expand=True, padx=20, pady=5)

        def render_patient_rows(filter_text=""):
            """Clears current view rows and updates dynamically based on matched search queries."""
            for widget in scroll_box.winfo_children():
                widget.destroy()

            query = filter_text.lower()
            for p in patients:
                # Logic condition match: Checks if typed text matches the dictionary ID or Name values
                if query in p["name"].lower() or query in p["id"].lower():
                    row = ctk.CTkFrame(scroll_box, fg_color=CARD, height=50)
                    row.pack(fill="x", pady=4, ipady=4)

                    ctk.CTkLabel(row, text=f"{p['id']}", font=("Arial", 12, "bold"), text_color=ACCENT, width=70).pack(
                        side="left", padx=10)
                    ctk.CTkLabel(row, text=p["name"], font=("Arial", 13, "bold"), width=160, anchor="w").pack(
                        side="left", padx=10)
                    ctk.CTkLabel(row, text=f"Age: {p['age']}", width=60, anchor="w").pack(side="left", padx=10)
                    ctk.CTkLabel(row, text=f"Phone: {p['phone']}", width=150, anchor="w", text_color="gray").pack(
                        side="left", padx=10)

                    status = ctk.CTkComboBox(row, values=statuses, width=130)
                    status.set(p["status"])
                    status.pack(side="right", padx=15)

                    def update(target_p=p, current_s=status):
                        target_p["status"] = current_s.get()
                        self.log(f"{target_p['id']} status updated to → {target_p['status']}")

                    status.configure(command=lambda _, u=update: u())

        # Initialize list container with full un-filtered datasets
        render_patient_rows()

        # Event-Listener Callback: Fires the filter whenever any keyboard action happens inside the box
        search_bar.bind("<KeyRelease>", lambda event: render_patient_rows(search_bar.get()))

    # ================= APPOINTMENTS =================
    def appointment_page(self):
        self.clear()
        self.add_top_bar()

        box = ctk.CTkFrame(self.container, fg_color=CARD, corner_radius=15)
        box.pack(pady=40, ipady=15, ipadx=15)

        ctk.CTkLabel(box, text="Schedule New Appointment", font=("Arial", 18, "bold"), text_color=ACCENT).pack(pady=10)

        name = ctk.CTkEntry(box, placeholder_text="Patient Full Name", width=260)
        name.pack(pady=5)

        s1 = ctk.CTkEntry(box, placeholder_text="Primary Symptom", width=260)
        s1.pack(pady=5)

        s2 = ctk.CTkEntry(box, placeholder_text="Secondary Symptom", width=260)
        s2.pack(pady=5)

        time_box = ctk.CTkEntry(box, placeholder_text="Preferred Time (e.g., 14:30)", width=260)
        time_box.pack(pady=5)

        def book():
            if not name.get() or not time_box.get():
                messagebox.showerror("Error", "Missing required fields.")
                return
            appt = f"{name.get()} | Symptoms: {s1.get()}, {s2.get()} | Scheduled: {time_box.get()}"
            appointments.append(appt)
            self.log(f"Appointment booked: {appt}")
            messagebox.showinfo("Booked", "Appointment saved successfully!")
            self.dashboard()

        ctk.CTkButton(box, text="BOOK APPOINTMENT", fg_color=ACCENT, text_color="black", font=("Arial", 12, "bold"),
                      command=book).pack(pady=15)

    # ================= AUDIT =================
    def audit_page(self):
        self.clear()
        self.add_top_bar()

        title_lbl = ctk.CTkLabel(self.container, text="System Audit Trails", font=("Arial", 20, "bold"),
                                 text_color="white")
        title_lbl.pack(pady=10, anchor="w", padx=20)

        box = ctk.CTkScrollableFrame(self.container, fg_color=CARD, corner_radius=12)
        box.pack(fill="both", expand=True, padx=20, pady=10)

        if not audit_log:
            ctk.CTkLabel(box, text="No events logged in this session.", text_color="gray").pack(pady=20)
        else:
            for log_entry in audit_log:
                ctk.CTkLabel(box, text=log_entry, font=("Courier New", 12), text_color="#AEC6CF").pack(anchor="w",
                                                                                                       padx=10, pady=2)

    # ================= EMERGENCY =================
    def emergency(self):
        messagebox.showwarning("EMERGENCY", "CRITICAL SYSTEM-WIDE ALERT ACTIVATED")
        self.log("🚨 Emergency mode triggered by user")


# ================= RUN =================
if __name__ == "__main__":
    app = CHERS()
    app.mainloop()