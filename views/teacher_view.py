import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from PIL import Image, ImageTk
import os

class TeacherFrame(tk.Frame):
    def __init__(self, parent, controller, user_id):
        super().__init__(parent)
        self.controller = controller
        self.user_id = user_id
        self.configure(bg="#f8fafc")
        
        self.current_subject_id = None
        self.current_class_name = None
        self.current_student_id = None
        
        self.load_teacher_info()
        self.create_header()
        
        main_container = tk.Frame(self, bg="#f8fafc")
        main_container.pack(fill="both", expand=True, padx=40, pady=20)
        
        self.create_form_section(main_container)
        self.create_dashboard_section(main_container)
        
        self.load_subjects()
    
    def load_teacher_info(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT first_name, last_name, specialty FROM Teachers WHERE id = ?", (self.user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            self.first_name, self.last_name = result[0], result[1]
            self.specialty = result[2] if result[2] else "Non définie"
        else:
            self.first_name, self.last_name, self.specialty = "Enseignant", "Inconnu", "Non définie"
    
    def create_header(self):
        header = tk.Frame(self, bg="white", height=140)
        header.pack(fill="x", padx=40, pady=(20, 0))
        header.pack_propagate(False)
        
        content = tk.Frame(header, bg="white")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Logo
        logo_box = tk.Frame(content, bg="white")
        logo_box.pack(side="left", padx=(0, 20))
        
        try:
            logo_path = None
            for name in ["logo groupe 1.png", "logo groupe 1.jpg", "logo_groupe_1.png"]:
                if os.path.exists(name):
                    logo_path = name
                    break
            
            if logo_path:
                img = Image.open(logo_path)
                img = img.resize((80, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                logo_label = tk.Label(logo_box, image=photo, bg="white")
                logo_label.image = photo
                logo_label.pack()
            else:
                tk.Label(logo_box, text="G1", bg="#0ea5e9", fg="white",
                        font=("Arial", 28, "bold"), width=2, height=1).pack()
        except:
            tk.Label(logo_box, text="G1", bg="#0ea5e9", fg="white",
                    font=("Arial", 28, "bold"), width=2, height=1).pack()
        
        # Informations
        info = tk.Frame(content, bg="white")
        info.pack(side="left", fill="both", expand=True)
        
        tk.Label(info, text=f"👋 Bienvenue, {self.first_name} {self.last_name}",
                bg="white", fg="#1e293b", font=("Arial", 20, "bold")).pack(anchor="w")
        
        specialty_frame = tk.Frame(info, bg="#e0f2fe", bd=0)
        specialty_frame.pack(anchor="w", pady=(8, 0))
        
        tk.Label(specialty_frame, text=f"🎯 {self.specialty}", bg="#e0f2fe", fg="#0284c7",
                font=("Arial", 11, "bold")).pack(padx=12, pady=5)
        
        # Bouton déconnexion
        tk.Button(content, text="🚪 Déconnexion", bg="#22c55e", fg="white",
                 font=("Arial", 10, "bold"), padx=20, pady=10, bd=0,
                 cursor="hand2", relief="flat",
                 activebackground="#16a34a",
                 command=self.controller.logout).pack(side="right")
    
    def create_form_section(self, parent):
        form_frame = tk.Frame(parent, bg="white", bd=0)
        form_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Header
        header = tk.Frame(form_frame, bg="#0ea5e9", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="📝 Formulaire de Notation",
                bg="#0ea5e9", fg="white", font=("Arial", 15, "bold")).pack(pady=18)
        
        # Corps du formulaire avec scrollbar
        canvas_container = tk.Frame(form_frame, bg="white")
        canvas_container.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(canvas_container, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        
        fields = tk.Frame(canvas, bg="white", padx=30, pady=20)
        
        canvas.create_window((0, 0), window=fields, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        fields.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # ÉTAPE 1
        tk.Label(fields, text="ÉTAPE 1 : Sélection de la matière", 
                bg="white", fg="#0284c7",
                font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 8))
        
        subject_border = tk.Frame(fields, bg="#0ea5e9", bd=0)
        subject_border.pack(fill="x")
        
        self.subject_combo = ttk.Combobox(subject_border, font=("Arial", 11), state="readonly")
        self.subject_combo.pack(fill="x", padx=2, pady=2, ipady=6)
        self.subject_combo.bind("<<ComboboxSelected>>", self.on_subject_change)
        
        # ÉTAPE 2
        tk.Label(fields, text="ÉTAPE 2 : Classe (Auto-complétée)", 
                bg="white", fg="#0284c7",
                font=("Arial", 10, "bold")).pack(anchor="w", pady=(20, 8))
        
        self.class_entry = tk.Entry(fields, font=("Arial", 11), state="readonly",
                                    bg="#f1f5f9", fg="#64748b", bd=0, relief="flat")
        self.class_entry.pack(fill="x", pady=2, ipady=8)
        
        # ÉTAPE 3
        tk.Label(fields, text="ÉTAPE 3 : Sélection de l'étudiant", 
                bg="white", fg="#0284c7",
                font=("Arial", 10, "bold")).pack(anchor="w", pady=(20, 8))
        
        student_border = tk.Frame(fields, bg="#0ea5e9", bd=0)
        student_border.pack(fill="x")
        
        self.student_combo = ttk.Combobox(student_border, font=("Arial", 11), state="readonly")
        self.student_combo.pack(fill="x", padx=2, pady=2, ipady=6)
        self.student_combo.bind("<<ComboboxSelected>>", self.on_student_change)
        
        # ÉTAPE 4
        tk.Label(fields, text="ÉTAPE 4 : Saisie de la note (0-20)", 
                bg="white", fg="#0284c7",
                font=("Arial", 10, "bold")).pack(anchor="w", pady=(20, 8))
        
        note_border = tk.Frame(fields, bg="#0ea5e9", bd=0)
        note_border.pack(fill="x")
        
        note_inner = tk.Frame(note_border, bg="white")
        note_inner.pack(fill="x", padx=2, pady=2)
        
        self.grade_entry = tk.Entry(note_inner, font=("Arial", 48, "bold"),
                                    justify="center", bg="white", fg="#1e293b",
                                    bd=0, insertbackground="#0ea5e9")
        self.grade_entry.pack(fill="x", pady=15)
        self.grade_entry.bind("<Return>", lambda e: self.save_grade())
        
        # Info
        self.info_label = tk.Label(fields, text="💡 Sélectionnez une matière pour commencer",
                                   bg="white", fg="#64748b", font=("Arial", 10, "italic"))
        self.info_label.pack(pady=15)
        
        # Bouton ENREGISTRER - TRÈS VISIBLE
        save_button = tk.Button(fields, text="💾 ENREGISTRER LA NOTE",
                               bg="#22c55e", fg="white", font=("Arial", 14, "bold"),
                               pady=18, bd=0, cursor="hand2", relief="flat",
                               activebackground="#16a34a",
                               command=self.save_grade)
        save_button.pack(fill="x", pady=(15, 30), ipady=5)
        
        # Effet hover
        save_button.bind("<Enter>", lambda e: save_button.config(bg="#16a34a"))
        save_button.bind("<Leave>", lambda e: save_button.config(bg="#22c55e"))
    
    def create_dashboard_section(self, parent):
        dashboard = tk.Frame(parent, bg="#f8fafc")
        dashboard.pack(side="right", fill="both", expand=True)
        
        tk.Label(dashboard, text="📊 Tableau de Bord",
                bg="#f8fafc", fg="#1e293b", font=("Arial", 15, "bold")).pack(pady=(0, 15))
        
        # Compteurs
        counters = tk.Frame(dashboard, bg="#f8fafc")
        counters.pack(fill="x", pady=(0, 15))
        
        # Carte verte
        green = tk.Frame(counters, bg="#22c55e", bd=0)
        green.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(green, text="✅ Effectif noté", bg="#22c55e", fg="white",
                font=("Arial", 10, "bold")).pack(pady=(12, 5))
        self.graded_label = tk.Label(green, text="0 / 0", bg="#22c55e", fg="white",
                                     font=("Arial", 28, "bold"))
        self.graded_label.pack(pady=(0, 12))
        
        # Carte rouge
        red = tk.Frame(counters, bg="#ef4444", bd=0)
        red.pack(side="right", fill="both", expand=True)
        
        tk.Label(red, text="⏳ En attente", bg="#ef4444", fg="white",
                font=("Arial", 10, "bold")).pack(pady=(12, 5))
        self.pending_label = tk.Label(red, text="0", bg="#ef4444", fg="white",
                                      font=("Arial", 28, "bold"))
        self.pending_label.pack(pady=(0, 12))
        
        # Liste succès
        success = tk.Frame(dashboard, bg="white", bd=0)
        success.pack(fill="both", expand=True, pady=(0, 10))
        
        success_header = tk.Frame(success, bg="#e0f2fe", height=40)
        success_header.pack(fill="x")
        success_header.pack_propagate(False)
        
        tk.Label(success_header, text="✨ Élèves évalués", bg="#e0f2fe", fg="#0284c7",
                font=("Arial", 11, "bold")).pack(pady=10)
        
        table_container = tk.Frame(success, bg="white")
        table_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        style = ttk.Style()
        style.configure("Success.Treeview", background="white", foreground="#1e293b",
                       fieldbackground="white", borderwidth=0, font=("Arial", 10))
        style.configure("Success.Treeview.Heading", background="#0ea5e9", foreground="white",
                       font=("Arial", 10, "bold"))
        style.map("Success.Treeview", background=[("selected", "#86efac")],
                 foreground=[("selected", "#1e293b")])
        
        scrollbar = tk.Scrollbar(table_container)
        scrollbar.pack(side="right", fill="y")
        
        self.graded_tree = ttk.Treeview(table_container, columns=("Étudiant", "Note"),
                                       show="headings", height=8,
                                       yscrollcommand=scrollbar.set,
                                       style="Success.Treeview")
        scrollbar.config(command=self.graded_tree.yview)
        
        self.graded_tree.heading("Étudiant", text="ÉTUDIANT")
        self.graded_tree.heading("Note", text="NOTE /20")
        self.graded_tree.column("Étudiant", width=200)
        self.graded_tree.column("Note", width=80, anchor="center")
        self.graded_tree.pack(fill="both", expand=True)
        
        # Liste alerte
        alert = tk.Frame(dashboard, bg="white", bd=0)
        alert.pack(fill="both", expand=True)
        
        alert_header = tk.Frame(alert, bg="#fee2e2", height=40)
        alert_header.pack(fill="x")
        alert_header.pack_propagate(False)
        
        tk.Label(alert_header, text="⚠️ Élèves non évalués", bg="#fee2e2", fg="#dc2626",
                font=("Arial", 11, "bold")).pack(pady=10)
        
        alert_scroll = tk.Frame(alert, bg="white")
        alert_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        alert_canvas = tk.Canvas(alert_scroll, bg="white", highlightthickness=0)
        alert_scrollbar = tk.Scrollbar(alert_scroll, command=alert_canvas.yview)
        self.alert_content = tk.Frame(alert_canvas, bg="white")
        
        alert_canvas.create_window((0, 0), window=self.alert_content, anchor="nw")
        alert_canvas.configure(yscrollcommand=alert_scrollbar.set)
        
        alert_scrollbar.pack(side="right", fill="y")
        alert_canvas.pack(side="left", fill="both", expand=True)
        
        self.alert_content.bind("<Configure>", 
                               lambda e: alert_canvas.configure(scrollregion=alert_canvas.bbox("all")))
    
    def load_subjects(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, class_name FROM Subjects WHERE teacher_id = ? ORDER BY name",
                      (self.user_id,))
        subjects = cursor.fetchall()
        conn.close()
        
        if subjects:
            self.subjects_data = {f"{s[1]} - {s[2]}": (s[0], s[2]) for s in subjects}
            self.subject_combo['values'] = list(self.subjects_data.keys())
        else:
            self.subjects_data = {}
            self.subject_combo['values'] = []
            messagebox.showwarning("⚠️ Attention", "Aucune matière assignée.\nContactez l'administrateur.")
    
    def on_subject_change(self, event):
        selected = self.subject_combo.get()
        if not selected:
            return
        
        self.current_subject_id, self.current_class_name = self.subjects_data[selected]
        
        self.class_entry.config(state="normal")
        self.class_entry.delete(0, tk.END)
        self.class_entry.insert(0, self.current_class_name)
        self.class_entry.config(state="readonly")
        
        self.load_students()
        self.grade_entry.delete(0, tk.END)
        self.current_student_id = None
        self.info_label.config(text="💡 Sélectionnez un étudiant", fg="#64748b")
        self.update_dashboard()
    
    def load_students(self):
        if not self.current_class_name:
            return
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_name, last_name FROM Students WHERE class_name = ? ORDER BY last_name, first_name",
                      (self.current_class_name,))
        students = cursor.fetchall()
        conn.close()
        
        if students:
            self.students_data = {f"{s[2]} {s[1]}": s[0] for s in students}
            self.student_combo['values'] = list(self.students_data.keys())
        else:
            self.students_data = {}
            self.student_combo['values'] = []
            self.info_label.config(text="⚠️ Aucun étudiant dans cette classe", fg="#ef4444")
    
    def on_student_change(self, event):
        selected = self.student_combo.get()
        if not selected:
            return
        
        self.current_student_id = self.students_data[selected]
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT grade FROM Grades WHERE student_id = ? AND subject_id = ?",
                      (self.current_student_id, self.current_subject_id))
        result = cursor.fetchone()
        conn.close()
        
        self.grade_entry.delete(0, tk.END)
        if result:
            self.grade_entry.insert(0, str(result[0]))
            self.info_label.config(text="✏️ Note existante - Modification possible", fg="#f59e0b")
        else:
            self.info_label.config(text="✅ Prêt à noter cet étudiant", fg="#22c55e")
        
        self.grade_entry.focus()
    
    def save_grade(self):
        if not self.current_subject_id:
            messagebox.showerror("❌ Erreur", "Sélectionnez une matière")
            return
        
        if not self.current_student_id:
            messagebox.showerror("❌ Erreur", "Sélectionnez un étudiant")
            return
        
        grade_str = self.grade_entry.get().strip()
        if not grade_str:
            messagebox.showerror("❌ Erreur", "Saisissez une note")
            return
        
        try:
            grade = float(grade_str.replace(',', '.'))
            if grade < 0 or grade > 20:
                messagebox.showerror("❌ Erreur", "Note entre 0 et 20")
                return
        except ValueError:
            messagebox.showerror("❌ Erreur", "Note invalide (ex: 15.5)")
            return
        
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id FROM Grades WHERE student_id = ? AND subject_id = ?",
                         (self.current_student_id, self.current_subject_id))
            existing = cursor.fetchone()
            
            if existing:
                cursor.execute("UPDATE Grades SET grade = ?, date = datetime('now') WHERE student_id = ? AND subject_id = ?",
                             (grade, self.current_student_id, self.current_subject_id))
                message = "✅ Note mise à jour !"
            else:
                cursor.execute("INSERT INTO Grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, datetime('now'))",
                             (self.current_student_id, self.current_subject_id, grade))
                message = "✅ Note enregistrée !"
            
            conn.commit()
            messagebox.showinfo("Succès", message)
            
            self.student_combo.set('')
            self.grade_entry.delete(0, tk.END)
            self.current_student_id = None
            self.info_label.config(text="💡 Sélectionnez un autre étudiant", fg="#64748b")
            self.update_dashboard()
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur: {str(e)}")
        finally:
            conn.close()
    
    def update_dashboard(self):
        if not self.current_subject_id or not self.current_class_name:
            return
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, first_name, last_name FROM Students WHERE class_name = ?",
                      (self.current_class_name,))
        all_students = cursor.fetchall()
        total_students = len(all_students)
        
        cursor.execute("""SELECT s.first_name, s.last_name, g.grade FROM Grades g
                         JOIN Students s ON g.student_id = s.id
                         WHERE g.subject_id = ? AND s.class_name = ?
                         ORDER BY s.last_name, s.first_name""",
                      (self.current_subject_id, self.current_class_name))
        graded_students = cursor.fetchall()
        conn.close()
        
        graded_count = len(graded_students)
        pending_count = total_students - graded_count
        
        self.graded_label.config(text=f"{graded_count} / {total_students}")
        self.pending_label.config(text=str(pending_count))
        
        for item in self.graded_tree.get_children():
            self.graded_tree.delete(item)
        
        for student in graded_students:
            self.graded_tree.insert("", "end", values=(f"{student[1]} {student[0]}", f"{student[2]:.2f}"))
        
        for widget in self.alert_content.winfo_children():
            widget.destroy()
        
        row, col = 0, 0
        for student in all_students:
            has_grade = any(g[0] == student[1] and g[1] == student[2] for g in graded_students)
            
            if not has_grade:
                badge = tk.Label(self.alert_content, text=f"{student[2]} {student[1]}",
                               bg="#fee2e2", fg="#dc2626", font=("Arial", 9, "bold"),
                               padx=10, pady=6, relief="solid", bd=1, borderwidth=1)
                badge.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
                
                col += 1
                if col > 1:
                    col = 0
                    row += 1
        
        for i in range(2):
            self.alert_content.columnconfigure(i, weight=1)