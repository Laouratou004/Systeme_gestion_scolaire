import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from auth_manager import hash_password
from PIL import Image, ImageTk
import os

class AdminFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f8fafc")

        self.show_form = False
        self.editing_id = None
        self.current_module = "users"
        
        # Variables pour la recherche et les filtres
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        self.filter_var = tk.StringVar(value="Tous")
        self.filter_var.trace('w', self.on_filter_change)
        self.all_data = []

        # --- SIDEBAR ---
        self.sidebar = tk.Frame(self, bg="white", width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(self.sidebar, bg="white", pady=30)
        logo_frame.pack(fill="x")
        
        try:
            logo_path = None
            possible_names = ["logo groupe 1.png", "logo groupe 1.jpg", "logo_groupe_1.png"]
            for name in possible_names:
                if os.path.exists(name):
                    logo_path = name
                    break
            
            if logo_path:
                img = Image.open(logo_path)
                img = img.resize((80, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                logo_label = tk.Label(logo_frame, image=photo, bg="white")
                logo_label.image = photo
                logo_label.pack()
            else:
                tk.Label(logo_frame, text="G1", bg="#0ea5e9", fg="white",
                        font=("Arial", 32, "bold"), width=2, height=1).pack()
        except Exception as e:
            tk.Label(logo_frame, text="G1", bg="#0ea5e9", fg="white",
                    font=("Arial", 32, "bold"), width=2, height=1).pack()
        
        tk.Label(logo_frame, text="GROUPE 1", fg="#1e293b", bg="white", 
                font=("Arial", 16, "bold")).pack(pady=(10, 2))
        tk.Label(logo_frame, text="Administration", fg="#64748b", bg="white", 
                font=("Arial", 10)).pack()
        
        tk.Frame(self.sidebar, height=1, bg="#e2e8f0").pack(fill="x", padx=20, pady=20)

        # Menu
        self.nav_btns = {}
        menu_items = [
            ("👤 Utilisateurs", "users"),
            ("🎓 Étudiants", "students"),
            ("👨‍🏫 Enseignants", "teachers"),
            ("📚 Matières", "subjects")
        ]
        
        for text, mod in menu_items:
            btn = tk.Button(self.sidebar, text=text, bg="white", fg="#64748b", 
                          bd=0, padx=25, pady=15, anchor="w", 
                          font=("Arial", 11),
                          activebackground="#f1f5f9", activeforeground="#0ea5e9",
                          relief="flat",
                          command=lambda m=mod: self.switch_module(m))
            btn.pack(fill="x", padx=20, pady=2)
            self.nav_btns[mod] = btn

        # Footer
        footer = tk.Frame(self.sidebar, bg="white")
        footer.pack(side="bottom", fill="x", pady=20)
        tk.Frame(footer, height=1, bg="#e2e8f0").pack(fill="x", padx=20, pady=(0, 15))
        
        tk.Button(footer, text="Déconnexion", bg="#22c55e", fg="black", 
                 font=("Arial", 11, "bold"), command=self.controller.logout, 
                 bd=0, pady=12, cursor="hand2", relief="flat",
                 activebackground="#16a34a").pack(fill="x", padx=20)

        # --- ZONE PRINCIPALE ---
        self.main_area = tk.Frame(self, bg="#f8fafc")
        self.main_area.pack(side="right", fill="both", expand=True)

        # Header
        self.header = tk.Frame(self.main_area, bg="#0ea5e9", height=100)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        
        header_content = tk.Frame(self.header, bg="#0ea5e9")
        header_content.pack(fill="both", expand=True, padx=40, pady=25)
        
        title_box = tk.Frame(header_content, bg="#0ea5e9")
        title_box.pack(side="left")
        
        self.lbl_title = tk.Label(title_box, text="", font=("Arial", 26, "bold"), bg="#0ea5e9", fg="white")
        self.lbl_title.pack(anchor="w")
        
        self.lbl_subtitle = tk.Label(title_box, text="Gestion du système", font=("Arial", 11), bg="#0ea5e9", fg="white")
        self.lbl_subtitle.pack(anchor="w")
        
        self.btn_toggle_form = tk.Button(header_content, text="➕ Nouveau", bg="white", fg="#0ea5e9", 
                                       font=("Arial", 11, "bold"), padx=25, pady=12, bd=0, cursor="hand2",
                                       command=self.toggle_form)
        self.btn_toggle_form.pack(side="right")

        # Contenu
        content = tk.Frame(self.main_area, bg="#f8fafc", padx=40, pady=30)
        content.pack(fill="both", expand=True)

        # Barre Recherche
        self.search_filter_frame = tk.Frame(content, bg="white")
        self.search_filter_frame.pack(fill="x", pady=(0, 15))
        
        search_container = tk.Frame(self.search_filter_frame, bg="white", padx=20, pady=15)
        search_container.pack(fill="x")
        
        search_row = tk.Frame(search_container, bg="white")
        search_row.pack(fill="x", pady=(0, 10))
        
        tk.Label(search_row, text="🔍 Recherche:", bg="white", font=("Arial", 10, "bold")).pack(side="left", padx=(0, 10))
        tk.Entry(search_row, textvariable=self.search_var, font=("Arial", 11), bg="#f8fafc").pack(side="left", fill="x", expand=True, ipady=8)
        
        tk.Label(search_row, text="🎯 Filtre:", bg="white", font=("Arial", 10, "bold")).pack(side="left", padx=(10, 10))
        self.filter_combo = ttk.Combobox(search_row, textvariable=self.filter_var, state="readonly", font=("Arial", 11), width=15)
        self.filter_combo.pack(side="left", ipady=6)

        stats_row = tk.Frame(search_container, bg="white")
        stats_row.pack(fill="x")
        self.stats_label = tk.Label(stats_row, text="📊 Chargement...", bg="white", fg="#64748b", font=("Arial", 9, "italic"))
        self.stats_label.pack(side="left")
        
        tk.Button(stats_row, text="🧹 Réinitialiser", bg="#f1f5f9", font=("Arial", 9), command=self.reset_filters).pack(side="right")

        self.form_container = tk.Frame(content, bg="white")
        self.table_container = tk.Frame(content, bg="white")
        self.table_container.pack(fill="both", expand=True)

        # Actions
        self.action_bar = tk.Frame(content, bg="#060D13", pady=15)
        self.action_bar.pack(fill="x", side="bottom")

        tk.Button(self.action_bar, text="✏️ Modifier", bg="#0ea5e9", fg="black", font=("Arial", 10, "bold"), 
                 padx=20, pady=10, bd=0, command=self.handle_edit).pack(side="left", padx=(0, 10))
        
        tk.Button(self.action_bar, text="🗑️ Supprimer", bg="#ef4444", fg="black", font=("Arial", 10, "bold"), 
                 padx=20, pady=10, bd=0, command=self.handle_delete).pack(side="left")
        
        tk.Button(self.action_bar, text="📊 Statistiques", bg="#22c55e", fg="black", font=("Arial", 10, "bold"), 
                 padx=20, pady=10, bd=0, command=self.show_stats).pack(side="right")

        self.switch_module("users")

    def switch_module(self, module):
        self.current_module = module
        self.editing_id = None
        self.show_form = False
        self.form_container.pack_forget()
        self.search_var.set("")
        
        titles = {
            "users": ("👤 Utilisateurs", "Comptes système"),
            "students": ("🎓 Étudiants", "Base étudiants"),
            "teachers": ("👨‍🏫 Enseignants", "Corps professoral"),
            "subjects": ("📚 Matières", "Cours")
        }
        t, s = titles.get(module, ("Module", ""))
        self.lbl_title.config(text=t)
        self.lbl_subtitle.config(text=s)
        
        if module in ["students", "teachers"]:
            self.btn_toggle_form.pack_forget()
        else:
            self.btn_toggle_form.pack(side="right")
            self.btn_toggle_form.configure(text="➕ Nouveau", bg="white", fg="#0ea5e9")

        for m, btn in self.nav_btns.items():
            btn.configure(bg="#e0f2fe" if m == module else "white")

        self.configure_filters()
        self.refresh_ui()

    def configure_filters(self):
        opts = ["Tous"]
        if self.current_module == "users":
            opts += ["Admin", "Enseignant", "Étudiant"]
        else:
            opts += self.get_all_classes()
        self.filter_combo['values'] = opts
        self.filter_var.set("Tous")

    def get_all_classes(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT class_name FROM Students WHERE class_name IS NOT NULL")
            return [r[0] for r in cursor.fetchall()]
        except: return []
        finally: conn.close()

    def on_search_change(self, *args): self.apply_filters_and_refresh()
    def on_filter_change(self, *args): self.apply_filters_and_refresh()
    def reset_filters(self): self.search_var.set(""); self.filter_var.set("Tous")

    def apply_filters_and_refresh(self):
        if not hasattr(self, 'tree'): return
        self.tree.delete(*self.tree.get_children())
        
        search = self.search_var.get().lower().strip()
        f_val = self.filter_var.get()
        filtered = []

        for row in self.all_data:
            # Filtre
            if f_val != "Tous":
                idx = 2 if self.current_module == "users" else 4 if self.current_module in ["students", "teachers"] else 2
                if str(row[idx]) != f_val: continue
            # Recherche
            if search and search not in " ".join(map(str, row)).lower(): continue
            filtered.append(row)

        for r in filtered: self.tree.insert("", "end", values=r)
        self.stats_label.config(text=f"📊 {len(filtered)} sur {len(self.all_data)} résultat(s)")

    def toggle_form(self):
        if not self.show_form:
            self.show_form = True
            self.btn_toggle_form.configure(text="❌ Annuler", bg="#ef4444", fg="white")
            self.form_container.pack(before=self.table_container, fill="x", pady=(0, 20))
            self.render_form_content()
        else:
            self.show_form = False
            self.editing_id = None
            self.form_container.pack_forget()
            if self.current_module not in ["students", "teachers"]:
                self.btn_toggle_form.configure(text="➕ Nouveau", bg="white", fg="#0ea5e9")

    def render_form_content(self):
        for w in self.form_container.winfo_children(): w.destroy()
        self.inputs = {}
        f = tk.Frame(self.form_container, bg="white", padx=40, pady=20, bd=1, relief="solid")
        f.pack(fill="x")

        if self.current_module == "users":
            self.create_input(f, "Nom d'utilisateur", "username", 0, 0)
            self.create_input(f, "Mot de passe", "password", 0, 1, show="●")
            self.create_input(f, "Email", "email", 2, 0)
            tk.Label(f, text="Rôle", bg="white").grid(row=2, column=1, sticky="w")
            self.inputs["role"] = ttk.Combobox(f, values=["Admin", "Enseignant", "Étudiant"], state="readonly")
            self.inputs["role"].grid(row=3, column=1, sticky="we", padx=5, pady=5)

        elif self.current_module == "students":
            self.create_input(f, "Prénom", "first_name", 0, 0)
            self.create_input(f, "Nom", "last_name", 0, 1)
            self.create_input(f, "Naissance (YYYY-MM-DD)", "birth_date", 2, 0)
            self.create_input(f, "Classe", "class_name", 2, 1)

        elif self.current_module == "teachers":
            self.create_input(f, "Prénom", "first_name", 0, 0)
            self.create_input(f, "Nom", "last_name", 0, 1)
            self.create_input(f, "Spécialité", "specialty", 2, 0)
            
            # 🆕 CHAMP TEXTE POUR SAISIR LES CLASSES
            tk.Label(f, text="Classes (séparées par des virgules)", bg="white", 
                    font=("Arial", 10, "bold"), fg="#1e293b").grid(row=2, column=1, sticky="w", padx=5, pady=5)
            
            # Frame avec bordure
            border_frame = tk.Frame(f, bg="#0ea5e9", bd=0)
            border_frame.grid(row=3, column=1, sticky="we", padx=5, pady=5)
            
            classes_entry = tk.Entry(border_frame, font=("Arial", 11), bg="white", fg="#1e293b", bd=0, relief="flat")
            classes_entry.pack(fill="both", padx=2, pady=2, ipady=8)
            self.inputs["classes_text"] = classes_entry
            
            # Info bulle
            tk.Label(f, text="💡 Ex: L1, L2, Terminal A", bg="white", fg="#64748b", 
                    font=("Arial", 9, "italic")).grid(row=4, column=1, sticky="w", padx=5)

        elif self.current_module == "subjects":
            self.create_input(f, "Nom de la matière", "name", 0, 0)
            self.create_input(f, "Classe", "class_name", 0, 1)
            tk.Label(f, text="Enseignant", bg="white").grid(row=2, column=0, sticky="w")
            conn = get_connection(); cur = conn.cursor(); cur.execute("SELECT id, first_name, last_name FROM Teachers")
            profs = [f"{r[0]}-{r[1]} {r[2]}" for r in cur.fetchall()]; conn.close()
            self.inputs["teacher_id"] = ttk.Combobox(f, values=profs, state="readonly")
            self.inputs["teacher_id"].grid(row=3, column=0, columnspan=2, sticky="we", padx=5)

        tk.Button(f, text="💾 Enregistrer", bg="#22c55e", fg="white", font=("Arial", 11, "bold"), 
                  command=self.save_logic).grid(row=5, column=0, columnspan=2, pady=20, sticky="we")

    def create_input(self, parent, label, key, r, c, show=None):
        tk.Label(parent, text=label, bg="white", font=("Arial", 10, "bold"), fg="#1e293b").grid(row=r, column=c, sticky="w", padx=5, pady=5)
        
        # Frame avec bordure bleue
        border_frame = tk.Frame(parent, bg="#0ea5e9", bd=0)
        border_frame.grid(row=r+1, column=c, sticky="we", padx=5, pady=5)
        
        ent = tk.Entry(border_frame, show=show, font=("Arial", 11), bg="white", fg="#1e293b", bd=0, relief="flat")
        ent.pack(fill="both", padx=2, pady=2, ipady=8)
        self.inputs[key] = ent
        parent.columnconfigure(c, weight=1)

    def save_logic(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.current_module == "users":
                u, p, r, e = self.inputs["username"].get(), self.inputs["password"].get(), self.inputs["role"].get(), self.inputs["email"].get()
                if self.editing_id:
                    if p: cursor.execute("UPDATE Users SET username=?, password_hash=?, role=?, email=? WHERE id=?", (u, hash_password(p), r, e, self.editing_id))
                    else: cursor.execute("UPDATE Users SET username=?, role=?, email=? WHERE id=?", (u, r, e, self.editing_id))
                else:
                    cursor.execute("INSERT INTO Users (username, password_hash, role, email) VALUES (?,?,?,?)", (u, hash_password(p), r, e))
                    tid = cursor.lastrowid
                    if r == "Étudiant": cursor.execute("INSERT INTO Students (id, first_name, last_name) VALUES (?,?,'')", (tid, u))
                    elif r == "Enseignant": cursor.execute("INSERT INTO Teachers (id, first_name, last_name) VALUES (?,?,'')", (tid, u))

            elif self.current_module == "students":
                cursor.execute("UPDATE Students SET first_name=?, last_name=?, birth_date=?, class_name=? WHERE id=?", 
                             (self.inputs["first_name"].get(), self.inputs["last_name"].get(), self.inputs["birth_date"].get(), self.inputs["class_name"].get(), self.editing_id))

            elif self.current_module == "teachers":
                # 🆕 Récupérer les classes saisies dans le champ texte
                classes_text = self.inputs["classes_text"].get().strip()
                
                cursor.execute("UPDATE Teachers SET first_name=?, last_name=?, specialty=?, class_name=? WHERE id=?", 
                             (self.inputs["first_name"].get(), self.inputs["last_name"].get(), self.inputs["specialty"].get(), classes_text, self.editing_id))

            elif self.current_module == "subjects":
                tid = self.inputs["teacher_id"].get().split('-')[0]
                if self.editing_id: cursor.execute("UPDATE Subjects SET name=?, class_name=?, teacher_id=? WHERE id=?", (self.inputs["name"].get(), self.inputs["class_name"].get(), tid, self.editing_id))
                else: cursor.execute("INSERT INTO Subjects (name, class_name, teacher_id) VALUES (?,?,?)", (self.inputs["name"].get(), self.inputs["class_name"].get(), tid))

            conn.commit()
            messagebox.showinfo("Succès", "Données sauvegardées avec succès!")
            self.toggle_form(); self.refresh_ui()
        except Exception as ex: 
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}")
            print(f"Erreur détaillée: {ex}")
        finally: conn.close()

    def refresh_ui(self):
        for w in self.table_container.winfo_children(): w.destroy()
        conf = {
            "users": ("ID", "Nom d'utilisateur", "Rôle", "Email"),
            "students": ("ID", "Prénom", "Nom", "Naissance", "Classe"),
            "teachers": ("ID", "Prénom", "Nom", "Spécialité", "Classes"),
            "subjects": ("ID", "Nom de la matière", "Classe", "Enseignant")
        }
        cols = conf[self.current_module]
        self.tree = ttk.Treeview(self.table_container, columns=cols, show="headings", height=15)
        for c in cols: self.tree.heading(c, text=c); self.tree.column(c, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

        conn = get_connection(); cursor = conn.cursor()
        try:
            if self.current_module == "users": cursor.execute("SELECT id, username, role, email FROM Users")
            elif self.current_module == "students": cursor.execute("SELECT id, first_name, last_name, birth_date, class_name FROM Students")
            elif self.current_module == "teachers": cursor.execute("SELECT id, first_name, last_name, specialty, class_name FROM Teachers")
            elif self.current_module == "subjects":
                cursor.execute("""SELECT s.id, s.name, s.class_name, COALESCE(t.first_name || ' ' || t.last_name, 'N/A') 
                                FROM Subjects s LEFT JOIN Teachers t ON s.teacher_id = t.id""")
            self.all_data = cursor.fetchall()
            self.apply_filters_and_refresh()
        finally: conn.close()

    def handle_edit(self):
        sel = self.tree.selection()
        if not sel: return messagebox.showwarning("Attention", "Sélectionnez un élément")
        vals = self.tree.item(sel)['values']
        self.editing_id = vals[0]
        if not self.show_form: self.toggle_form()
        else: self.render_form_content()

        if self.current_module == "users":
            self.inputs["username"].insert(0, vals[1])
            self.inputs["role"].set(vals[2])
            self.inputs["email"].insert(0, vals[3] if vals[3] else "")
        elif self.current_module == "students":
            self.inputs["first_name"].insert(0, vals[1])
            self.inputs["last_name"].insert(0, vals[2])
            self.inputs["birth_date"].insert(0, vals[3] if vals[3] else "")
            self.inputs["class_name"].insert(0, vals[4] if vals[4] else "")
        elif self.current_module == "teachers":
            self.inputs["first_name"].insert(0, vals[1])
            self.inputs["last_name"].insert(0, vals[2])
            self.inputs["specialty"].insert(0, vals[3] if vals[3] else "")
            # 🆕 Pré-remplir le champ texte des classes
            self.inputs["classes_text"].insert(0, vals[4] if vals[4] else "")
        elif self.current_module == "subjects":
            self.inputs["name"].insert(0, vals[1])
            self.inputs["class_name"].insert(0, vals[2])

    def handle_delete(self):
        sel = self.tree.selection()
        if not sel: return messagebox.showwarning("Attention", "Sélectionnez un élément")
        iid = self.tree.item(sel)['values'][0]
        if messagebox.askyesno("Confirmation", "Supprimer cet élément ?"):
            conn = get_connection(); cursor = conn.cursor()
            try:
                table = "Subjects" if self.current_module == "subjects" else "Users"
                cursor.execute(f"DELETE FROM {table} WHERE id=?", (iid,))
                conn.commit(); 
                messagebox.showinfo("Succès", "Suppression effectuée")
                self.refresh_ui()
            finally: conn.close()

    def show_stats(self):
        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Users"); u = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM Teachers"); t = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM Students"); s = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM Subjects"); sub = cursor.fetchone()[0]
            msg = f"👤 Utilisateurs: {u}\n👨‍🏫 Enseignants: {t}\n🎓 Étudiants: {s}\n📚 Matières: {sub}"
            messagebox.showinfo("📊 Statistiques Globales", msg)
        finally: conn.close()