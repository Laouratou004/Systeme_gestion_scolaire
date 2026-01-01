# views/bulletin_preview.py
"""
Fenêtre de prévisualisation du bulletin avant export
"""

import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import os

# Import du module Excel avec débogage
try:
    from views.components.export_excel import export_bulletin_excel
    EXCEL_AVAILABLE = True
    print("✅ Module export_excel chargé avec succès")
except ImportError as e:
    EXCEL_AVAILABLE = False
    print(f"❌ Erreur import: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    EXCEL_AVAILABLE = False
    print(f"❌ Erreur inattendue: {e}")
    import traceback
    traceback.print_exc()


class BulletinPreviewWindow(tk.Toplevel):
    """Fenêtre de prévisualisation du bulletin"""
    
    def __init__(self, parent, student_info, grades_data):
        super().__init__(parent)
        
        self.student_info = student_info
        self.grades_data = grades_data
        
        # Configuration de la fenêtre
        self.title("📋 Mon Bulletin de Notes")
        self.geometry("900x700")
        self.configure(bg="#f8fafc")
        
        # Centrer la fenêtre
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.winfo_screenheight() // 2) - (700 // 2)
        self.geometry(f"900x700+{x}+{y}")
        
        # Créer l'interface
        self.create_header()
        self.create_bulletin_content()
        self.create_footer()
        
        # Rendre la fenêtre modale
        self.transient(parent)
        self.grab_set()
    
    def create_header(self):
        """En-tête du bulletin"""
        header = tk.Frame(self, bg="#0ea5e9", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        content = tk.Frame(header, bg="#0ea5e9")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Titre
        tk.Label(content, text="📋 BULLETIN DE NOTES",
                bg="#0ea5e9", fg="black",
                font=("Arial", 22, "bold")).pack()
        
        tk.Label(content, text="Aperçu avant téléchargement",
                bg="#0ea5e9", fg="white",
                font=("Arial", 11)).pack(pady=(5, 0))
    
    def create_bulletin_content(self):
        """Contenu principal du bulletin"""
        
        # Container scrollable
        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Canvas pour le scroll
        canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        content_frame = tk.Frame(canvas, bg="white")
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        content_frame.bind("<Configure>", 
                          lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # === INFORMATIONS ÉTUDIANT ===
        info_section = tk.Frame(content_frame, bg="#f8fafc", bd=0)
        info_section.pack(fill="x", padx=20, pady=(15, 20))
        
        tk.Label(info_section, text="📌 INFORMATIONS",
                bg="#f8fafc", fg="#1e293b",
                font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 10))
        
        info_grid = tk.Frame(info_section, bg="white", bd=1, relief="solid")
        info_grid.pack(fill="x")
        
        info_data = [
            ("Nom complet", self.student_info['name']),
            ("Matricule", self.student_info['username']),
            ("Classe", self.student_info['class_name']),
            ("Période", "Semestre 1"),
            ("Année scolaire", "2024-2025")
        ]
        
        for i, (label, value) in enumerate(info_data):
            row_frame = tk.Frame(info_grid, bg="white" if i % 2 == 0 else "#f8fafc")
            row_frame.pack(fill="x")
            
            tk.Label(row_frame, text=label + " :",
                    bg=row_frame['bg'], fg="#64748b",
                    font=("Arial", 10, "bold"),
                    width=20, anchor="w").pack(side="left", padx=15, pady=10)
            
            tk.Label(row_frame, text=value,
                    bg=row_frame['bg'], fg="#1e293b",
                    font=("Arial", 10),
                    anchor="w").pack(side="left", padx=10)
        
        # === TABLEAU DES NOTES ===
        notes_section = tk.Frame(content_frame, bg="white", bd=0)
        notes_section.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        tk.Label(notes_section, text="📊 DÉTAIL DES NOTES",
                bg="white", fg="#1e293b",
                font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 10))
        
        # Style du tableau
        style = ttk.Style()
        style.configure("Bulletin.Treeview",
                       background="white",
                       foreground="#1e293b",
                       fieldbackground="white",
                       borderwidth=1,
                       rowheight=35,
                       font=("Arial", 10))
        style.configure("Bulletin.Treeview.Heading",
                       background="#0ea5e9",
                       foreground="white",
                       font=("Arial", 10, "bold"))
        
        # Créer le tableau
        columns = ("Matière", "Note", "Coef", "Note × Coef", "Enseignant")
        tree = ttk.Treeview(notes_section, columns=columns, show="headings",
                           height=10, style="Bulletin.Treeview")
        
        tree.heading("Matière", text="MATIÈRE")
        tree.heading("Note", text="NOTE /20")
        tree.heading("Coef", text="COEF")
        tree.heading("Note × Coef", text="NOTE × COEF")
        tree.heading("Enseignant", text="ENSEIGNANT")
        
        tree.column("Matière", width=200, anchor="w")
        tree.column("Note", width=80, anchor="center")
        tree.column("Coef", width=60, anchor="center")
        tree.column("Note × Coef", width=100, anchor="center")
        tree.column("Enseignant", width=180, anchor="w")
        
        tree.pack(fill="both", expand=True)
        
        # Remplir le tableau
        total_points = 0
        total_coef = 0
        
        for grade in self.grades_data:
            subject = grade['subject']
            note = grade['grade']
            coef = grade['coefficient']
            teacher = grade['teacher']
            
            weighted = note * coef
            total_points += weighted
            total_coef += coef
            
            tree.insert("", "end", values=(
                f"  {subject}",
                f"{note:.2f}",
                f"{coef:.1f}",
                f"{weighted:.2f}",
                teacher
            ))
        
        # Ligne de moyenne
        moyenne = total_points / total_coef if total_coef > 0 else 0
        tree.insert("", "end", values=(
            "  MOYENNE GÉNÉRALE",
            f"{moyenne:.2f}",
            f"{total_coef:.1f}",
            f"{total_points:.2f}",
            ""
        ), tags=('moyenne',))
        
        tree.tag_configure('moyenne', background='#fef3c7', font=("Arial", 10, "bold"))
        
        # === MENTION ===
        mention_section = tk.Frame(content_frame, bg="white")
        mention_section.pack(fill="x", padx=20, pady=(10, 20))
        
        mention_text, mention_color = self.get_mention(moyenne)
        
        mention_frame = tk.Frame(mention_section, bg=mention_color, bd=0)
        mention_frame.pack()
        
        tk.Label(mention_frame, text=f"🏆 Mention : {mention_text}",
                bg=mention_color, fg="white",
                font=("Arial", 16, "bold")).pack(padx=40, pady=15)
    
    def create_footer(self):
        """Pied de page avec boutons d'export"""
        footer = tk.Frame(self, bg="white", height=80)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        
        tk.Frame(footer, height=1, bg="#e2e8f0").pack(fill="x")
        
        buttons_frame = tk.Frame(footer, bg="white")
        buttons_frame.pack(expand=True)
        
        # Bouton Excel uniquement
        if EXCEL_AVAILABLE:
            btn_excel = tk.Button(buttons_frame,
                                 text="📊 Télécharger en Excel",
                                 bg="#10b981", fg="white",
                                 font=("Arial", 12, "bold"),
                                 padx=40, pady=15, bd=0,
                                 cursor="hand2", relief="flat",
                                 activebackground="#059669",
                                 command=self.export_excel)
            btn_excel.pack(side="left", padx=10)
            
            # Effet hover
            btn_excel.bind("<Enter>", lambda e: btn_excel.config(bg="#059669"))
            btn_excel.bind("<Leave>", lambda e: btn_excel.config(bg="#10b981"))
        else:
            tk.Label(buttons_frame,
                    text="⚠️ Export Excel non disponible\nInstallez: pip install pandas openpyxl",
                    bg="#fee2e2", fg="#dc2626",
                    font=("Arial", 10, "bold"),
                    justify="center",
                    padx=20, pady=12).pack(side="left", padx=10)
        
        # Bouton Fermer
        btn_close = tk.Button(buttons_frame,
                             text="❌ Fermer",
                             bg="#64748b", fg="white",
                             font=("Arial", 12, "bold"),
                             padx=30, pady=15, bd=0,
                             cursor="hand2", relief="flat",
                             activebackground="#475569",
                             command=self.destroy)
        btn_close.pack(side="left", padx=10)
        
        # Effet hover
        btn_close.bind("<Enter>", lambda e: btn_close.config(bg="#475569"))
        btn_close.bind("<Leave>", lambda e: btn_close.config(bg="#64748b"))
    
    def get_mention(self, moyenne):
        """Retourne la mention et la couleur"""
        if moyenne >= 16:
            return "Très Bien", "#22c55e"
        elif moyenne >= 14:
            return "Bien", "#3b82f6"
        elif moyenne >= 12:
            return "Assez Bien", "#f59e0b"
        elif moyenne >= 10:
            return "Passable", "#64748b"
        else:
            return "Insuffisant", "#ef4444"
    
    def export_excel(self):
        """Exporter en Excel"""
        try:
            class SimpleStudent:
                def __init__(self, username, name, class_name):
                    self.username = username
                    self.name = name
                    self.class_name = class_name
            
            student = SimpleStudent(
                username=self.student_info['username'],
                name=self.student_info['name'],
                class_name=self.student_info['class_name']
            )
            
            excel_path = export_bulletin_excel(
                student=student,
                grades_data=self.grades_data,
                semester="Semestre 1",
                year="2024-2025"
            )
            
            messagebox.showinfo(
                " Excel Généré",
                f"Bulletin exporté avec succès !\n\n"
                f"📂 {os.path.basename(excel_path)}\n\n"
                f"Le fichier va s'ouvrir."
            )
            
            webbrowser.open(excel_path)
            
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur Excel : {str(e)}")
            print(f"Erreur détaillée: {e}")
            import traceback
            traceback.print_exc()