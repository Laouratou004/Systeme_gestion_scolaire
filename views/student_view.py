import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from datetime import datetime
from PIL import Image, ImageTk
import os

class StudentFrame(tk.Frame):
    def __init__(self, parent, controller, user_id):
        super().__init__(parent)
        self.controller = controller
        self.user_id = user_id
        self.configure(bg="#f8fafc")
        
        self.load_student_info()
        self.create_header()
        self.create_main_content()
        self.load_grades()
    
    def load_student_info(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT first_name, last_name, class_name, birth_date
            FROM Students 
            WHERE id = ?
        """, (self.user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            self.first_name = result[0]
            self.last_name = result[1]
            self.class_name = result[2] if result[2] else "Non assigné"
            self.birth_date = result[3] if result[3] else "N/A"
        else:
            self.first_name = "Étudiant"
            self.last_name = "Inconnu"
            self.class_name = "Non assigné"
            self.birth_date = "N/A"
    
    def create_header(self):
        header = tk.Frame(self, bg="white", height=180)
        header.pack(fill="x", padx=40, pady=(20, 0))
        header.pack_propagate(False)
        
        content = tk.Frame(header, bg="white")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Partie gauche : Logo + Identité
        left_section = tk.Frame(content, bg="white")
        left_section.pack(side="left", fill="both", expand=True)
        
        # Logo à côté du nom
        logo_name_frame = tk.Frame(left_section, bg="white")
        logo_name_frame.pack(anchor="w")
        
        # Logo
        logo_box = tk.Frame(logo_name_frame, bg="white")
        logo_box.pack(side="left", padx=(0, 15))
        
        try:
            logo_path = None
            for name in ["logo groupe 1.png", "logo groupe 1.jpg", "logo_groupe_1.png"]:
                if os.path.exists(name):
                    logo_path = name
                    break
            
            if logo_path:
                img = Image.open(logo_path)
                img = img.resize((60, 60), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                logo_label = tk.Label(logo_box, image=photo, bg="white")
                logo_label.image = photo
                logo_label.pack()
            else:
                tk.Label(logo_box, text="G1", bg="#0ea5e9", fg="white",
                        font=("Arial", 20, "bold"), width=2, height=1).pack()
        except:
            tk.Label(logo_box, text="G1", bg="#0ea5e9", fg="white",
                    font=("Arial", 20, "bold"), width=2, height=1).pack()
        
        # Nom et info
        name_info = tk.Frame(logo_name_frame, bg="white")
        name_info.pack(side="left", fill="both", expand=True)
        
        tk.Label(name_info, text=f"{self.first_name} {self.last_name}",
                bg="white", fg="#1e293b", font=("Arial", 24, "bold")).pack(anchor="w")
        
        # Badge classe et matricule
        badges_frame = tk.Frame(left_section, bg="white")
        badges_frame.pack(anchor="w", pady=(10, 0))
        
        class_badge = tk.Frame(badges_frame, bg="#0ea5e9", bd=0)
        class_badge.pack(side="left", padx=(0, 10))
        tk.Label(class_badge, text=f"🎓 {self.class_name}",
                bg="#0ea5e9", fg="white",
                font=("Arial", 10, "bold")).pack(padx=12, pady=5)
        
        matricule_frame = tk.Frame(badges_frame, bg="#e0f2fe", bd=0)
        matricule_frame.pack(side="left")
        tk.Label(matricule_frame, text=f"🆔 Matricule : {self.user_id:04d}",
                bg="#e0f2fe", fg="#0284c7",
                font=("Arial", 9, "bold")).pack(padx=10, pady=5)
        
        # Partie droite : Moyenne + Boutons
        right_section = tk.Frame(content, bg="white")
        right_section.pack(side="right", padx=(20, 0))
        
        # Carte moyenne
        moyenne_card = tk.Frame(right_section, bg="#0ea5e9", bd=0, width=200, height=100)
        moyenne_card.pack()
        moyenne_card.pack_propagate(False)
        
        tk.Label(moyenne_card, text="📊 Moyenne Générale",
                bg="#0ea5e9", fg="white",
                font=("Arial", 10, "bold")).pack(pady=(12, 3))
        
        self.moyenne_label = tk.Label(moyenne_card, text="--/20",
                                      bg="#0ea5e9", fg="white",
                                      font=("Arial", 32, "bold"))
        self.moyenne_label.pack(pady=(0, 12))
        
        # 🆕 SECTION BOUTONS D'EXPORT
        buttons_container = tk.Frame(right_section, bg="white")
        buttons_container.pack(pady=(12, 0))
        
        # Bouton Voir mon Bulletin
        btn_bulletin = tk.Button(buttons_container, 
                               text="📋 Voir mon Bulletin",
                               bg="#8b5cf6", fg="white",
                               font=("Arial", 10, "bold"),
                               padx=18, pady=10, bd=0,
                               cursor="hand2", relief="flat",
                               activebackground="#7c3aed",
                               command=self.open_bulletin_preview)
        btn_bulletin.pack(fill="x", pady=(0, 5))
        
        btn_bulletin.bind("<Enter>", lambda e: btn_bulletin.config(bg="#7c3aed"))
        btn_bulletin.bind("<Leave>", lambda e: btn_bulletin.config(bg="#8b5cf6"))
        
        # Message info
        tk.Label(buttons_container,
                text="💡 Cliquez pour voir\net télécharger",
                bg="white", fg="#64748b",
                font=("Arial", 8),
                justify="center").pack()
        
        # Bouton déconnexion (en haut à droite)
        tk.Button(content, text="🚪 Déconnexion",
                 bg="#22c55e", fg="white",
                 font=("Arial", 9, "bold"),
                 padx=15, pady=8, bd=0,
                 cursor="hand2", relief="flat",
                 activebackground="#16a34a",
                 command=self.controller.logout).pack(side="right", anchor="ne")
    
    def create_main_content(self):
        main = tk.Frame(self, bg="#f8fafc")
        main.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Header du tableau
        table_header = tk.Frame(main, bg="#0ea5e9", height=60)
        table_header.pack(fill="x")
        table_header.pack_propagate(False)
        
        header_content = tk.Frame(table_header, bg="#0ea5e9")
        header_content.pack(fill="both", expand=True, padx=25, pady=12)
        
        tk.Label(header_content, text="📋 Relevé de Notes Officiel",
                bg="#0ea5e9", fg="white",
                font=("Arial", 16, "bold")).pack(anchor="w")
        
        tk.Label(header_content, text="Vos résultats académiques en temps réel",
                bg="#0ea5e9", fg="white",
                font=("Arial", 9)).pack(anchor="w")
        
        # Container du tableau
        table_container = tk.Frame(main, bg="white", bd=0)
        table_container.pack(fill="both", expand=True, pady=(0, 15))
        
        # Style du Treeview
        style = ttk.Style()
        style.configure("Student.Treeview",
                       background="white",
                       foreground="#1e293b",
                       fieldbackground="white",
                       borderwidth=0,
                       rowheight=40,
                       font=("Arial", 10))
        style.configure("Student.Treeview.Heading",
                       background="#0ea5e9",
                       foreground="white",
                       borderwidth=0,
                       font=("Arial", 10, "bold"))
        style.map("Student.Treeview",
                 background=[("selected", "#86efac")],
                 foreground=[("selected", "#1e293b")])
        
        # Scrollbar
        scrollbar = tk.Scrollbar(table_container)
        scrollbar.pack(side="right", fill="y")
        
        # Vérifier si coefficient existe
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(Subjects)")
            columns_info = cursor.fetchall()
            conn.close()
            
            has_coefficient = any(col[1] == 'coefficient' for col in columns_info)
        except:
            has_coefficient = False
        
        if has_coefficient:
            columns = ("Matière", "Note", "Coefficient", "Mention", "Date")
        else:
            columns = ("Matière", "Note", "Mention", "Date")
        
        self.grades_tree = ttk.Treeview(table_container,
                                       columns=columns,
                                       show="headings",
                                       yscrollcommand=scrollbar.set,
                                       style="Student.Treeview")
        scrollbar.config(command=self.grades_tree.yview)
        
        # Configuration des colonnes
        self.grades_tree.heading("Matière", text="📚 MATIÈRE")
        self.grades_tree.heading("Note", text="📊 NOTE /20")
        
        if has_coefficient:
            self.grades_tree.heading("Coefficient", text="⚖️ COEF")
            self.grades_tree.column("Matière", width=250, anchor="w")
            self.grades_tree.column("Note", width=100, anchor="center")
            self.grades_tree.column("Coefficient", width=80, anchor="center")
            self.grades_tree.column("Mention", width=120, anchor="center")
            self.grades_tree.column("Date", width=120, anchor="center")
        else:
            self.grades_tree.column("Matière", width=300, anchor="w")
            self.grades_tree.column("Note", width=120, anchor="center")
            self.grades_tree.column("Mention", width=150, anchor="center")
            self.grades_tree.column("Date", width=150, anchor="center")
        
        self.grades_tree.heading("Mention", text="🏆 MENTION")
        self.grades_tree.heading("Date", text="📅 DATE")
        
        self.grades_tree.pack(fill="both", expand=True)
        
        # Footer avec légende
        footer = tk.Frame(main, bg="white", bd=0)
        footer.pack(fill="x", pady=15)
        
        tk.Frame(footer, height=1, bg="#e2e8f0").pack(fill="x", padx=20, pady=(0, 15))
        
        legend_frame = tk.Frame(footer, bg="white")
        legend_frame.pack()
        
        tk.Label(legend_frame, text="📖 Système de mentions : ",
                bg="white", fg="#1e293b",
                font=("Arial", 9, "bold")).pack(side="left", padx=(0, 15))
        
        # EXCELLENT
        excellent_frame = tk.Frame(legend_frame, bg="#0ea5e9", bd=0)
        excellent_frame.pack(side="left", padx=5)
        tk.Label(excellent_frame, text="Excellent (≥16)",
                bg="#0ea5e9", fg="white",
                font=("Arial", 8, "bold")).pack(padx=8, pady=3)
        
        # ADMIS
        admis_frame = tk.Frame(legend_frame, bg="#22c55e", bd=0)
        admis_frame.pack(side="left", padx=5)
        tk.Label(admis_frame, text="Admis (10-15.99)",
                bg="#22c55e", fg="white",
                font=("Arial", 8, "bold")).pack(padx=8, pady=3)
        
        # ÉCHEC
        echec_frame = tk.Frame(legend_frame, bg="#ef4444", bd=0)
        echec_frame.pack(side="left", padx=5)
        tk.Label(echec_frame, text="Échec (<10)",
                bg="#ef4444", fg="white",
                font=("Arial", 8, "bold")).pack(padx=8, pady=3)
        
        # Info footer
        tk.Label(footer, text="ℹ️ Vos notes sont mises à jour en temps réel par vos enseignants",
                bg="white", fg="#64748b",
                font=("Arial", 8, "italic")).pack(pady=(8, 0))
    
    def get_mention(self, note):
        if note >= 16:
            return ("Excellent", "#0ea5e9")
        elif note >= 10:
            return ("Admis", "#22c55e")
        else:
            return ("Échec", "#ef4444")
    
    def load_grades(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Vérifier si coefficient existe
        try:
            cursor.execute("PRAGMA table_info(Subjects)")
            columns_info = cursor.fetchall()
            has_coefficient = any(col[1] == 'coefficient' for col in columns_info)
        except:
            has_coefficient = False
        
        # Requête selon si coefficient existe ou non
        if has_coefficient:
            cursor.execute("""
                SELECT s.name, g.grade, g.date, COALESCE(s.coefficient, 1.0)
                FROM Grades g
                JOIN Subjects s ON g.subject_id = s.id
                WHERE g.student_id = ?
                ORDER BY s.name
            """, (self.user_id,))
        else:
            cursor.execute("""
                SELECT s.name, g.grade, g.date, 1.0
                FROM Grades g
                JOIN Subjects s ON g.subject_id = s.id
                WHERE g.student_id = ?
                ORDER BY s.name
            """, (self.user_id,))
        
        grades = cursor.fetchall()
        conn.close()
        
        # Vider le tableau
        for item in self.grades_tree.get_children():
            self.grades_tree.delete(item)
        
        if not grades:
            self.moyenne_label.config(text="--/20")
            return
        
        # Calculer la moyenne pondérée
        total_points = 0
        total_coef = 0
        
        for grade in grades:
            note = grade[1]
            coef = grade[3]
            total_points += note * coef
            total_coef += coef
        
        moyenne = total_points / total_coef if total_coef > 0 else 0
        self.moyenne_label.config(text=f"{moyenne:.2f}/20")
        
        # Ajouter les notes au tableau
        for grade in grades:
            matiere = grade[0]
            note = grade[1]
            date_str = grade[2]
            coef = grade[3]
            
            # Formater la date
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                date_formatted = date_obj.strftime("%d/%m/%Y")
            except:
                date_formatted = date_str.split()[0] if date_str else "N/A"
            
            # Déterminer la mention
            mention_text, mention_color = self.get_mention(note)
            
            # Insérer dans le tableau
            try:
                cursor.execute("PRAGMA table_info(Subjects)")
                columns_info = cursor.fetchall()
                has_coefficient = any(col[1] == 'coefficient' for col in columns_info)
            except:
                has_coefficient = False
            
            if has_coefficient:
                self.grades_tree.insert("", "end",
                                       values=(f"  {matiere}",
                                              f"{note:.2f}",
                                              f"{coef:.1f}",
                                              mention_text,
                                              date_formatted))
            else:
                self.grades_tree.insert("", "end",
                                       values=(f"  {matiere}",
                                              f"{note:.2f}",
                                              mention_text,
                                              date_formatted))
    
    def open_bulletin_preview(self):
        """Ouvre la fenêtre de prévisualisation du bulletin"""
        
        try:
            from views.bulletin_preview import BulletinPreviewWindow
        except ImportError as e:
            messagebox.showerror(
                "❌ Erreur",
                f"Le module de prévisualisation n'est pas disponible.\n\n"
                f"Erreur: {str(e)}\n\n"
                f"Vérifiez que le fichier views/bulletin_preview.py existe."
            )
            return
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Vérifier si coefficient existe
            try:
                cursor.execute("""
                    SELECT s.name, g.grade, COALESCE(s.coefficient, 1.0), 
                           t.first_name, t.last_name
                    FROM Grades g
                    JOIN Subjects s ON g.subject_id = s.id
                    LEFT JOIN Teachers t ON s.teacher_id = t.id
                    WHERE g.student_id = ?
                    ORDER BY s.name
                """, (self.user_id,))
            except:
                cursor.execute("""
                    SELECT s.name, g.grade, 1.0, 
                           t.first_name, t.last_name
                    FROM Grades g
                    JOIN Subjects s ON g.subject_id = s.id
                    LEFT JOIN Teachers t ON s.teacher_id = t.id
                    WHERE g.student_id = ?
                    ORDER BY s.name
                """, (self.user_id,))
            
            grades_raw = cursor.fetchall()
            conn.close()
            
            if not grades_raw:
                messagebox.showwarning(
                    "⚠️ Attention", 
                    "Aucune note disponible.\n\n"
                    "Vous devez avoir au moins une note\n"
                    "pour voir votre bulletin."
                )
                return
            
            # Préparer les données pour la fenêtre
            grades_data = []
            for grade in grades_raw:
                teacher_name = f"{grade[3]} {grade[4]}" if grade[3] and grade[4] else "Non assigné"
                grades_data.append({
                    'subject': grade[0],
                    'grade': grade[1],
                    'coefficient': grade[2],
                    'teacher': teacher_name
                })
            
            student_info = {
                'username': f"ETU{self.user_id:04d}",
                'name': f"{self.first_name} {self.last_name}",
                'class_name': self.class_name
            }
            
            # Ouvrir la fenêtre de prévisualisation
            BulletinPreviewWindow(self, student_info, grades_data)
            
        except Exception as e:
            messagebox.showerror(
                "❌ Erreur", 
                f"Impossible d'ouvrir le bulletin.\n\n"
                f"Erreur : {str(e)}"
            )
            print(f"❌ Erreur détaillée: {e}")
            import traceback
            traceback.print_exc()