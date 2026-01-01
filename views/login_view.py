import tkinter as tk
from tkinter import messagebox
from auth_manager import verify_login
from PIL import Image, ImageTk
import os

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.bg_photo = None
        
        # 1. Configuration du fond d'écran
        self.setup_background()

        # 2. Création de l'interface (directement sur le frame principal)
        self.create_widgets()

    def setup_background(self):
        """Charge l'image de fond en plein écran."""
        self.bg_path = "pg.png" 
        
        if os.path.exists(self.bg_path):
            try:
                self.original_image = Image.open(self.bg_path)
                self.bg_label = tk.Label(self)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                self.bind("<Configure>", self._on_resize)
            except Exception as e:
                print(f"Erreur image : {e}")
                self.configure(bg="#1e293b")
        else:
            self.configure(bg="#1e293b")

    def _on_resize(self, event):
        """Redimensionne et ajuste la luminosité."""
        width = event.width
        height = event.height
        if width > 0 and height > 0:
            resized_img = self.original_image.resize((width, height), Image.Resampling.LANCZOS)
            # On assombrit légèrement (0.5) pour que le texte blanc soit lisible partout
            dark_img = resized_img.point(lambda p: p * 0.5)
            self.bg_photo = ImageTk.PhotoImage(dark_img)
            self.bg_label.config(image=self.bg_photo)

    def create_widgets(self):
        """Place les widgets directement sur le fond, sans cadre."""
        
        # Calcul des positions relatives pour centrer l'ensemble
        # On utilise un Frame invisible pour grouper les éléments au centre
        self.ui_group = tk.Frame(self, bg="#000000") # Ce frame ne sera pas visible car on va configurer ses enfants
        # Pour rendre le groupe transparent en Tkinter, on doit mettre le BG des enfants 
        # identique à la couleur du label de fond, mais Tkinter ne gère pas la vraie transparence.
        # ASTUCE : On utilise 'place' directement sur 'self' pour chaque élément.

        # --- LOGO ---
        self.logo_label = tk.Label(self, bg="#1a1a1a", bd=0) # Fond sombre assorti à l'image assombrie
        try:
            logo_path = "logo groupe 1.png"
            if os.path.exists(logo_path):
                img = Image.open(logo_path).resize((120, 120), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(img)
                self.logo_label.config(image=self.logo_photo)
        except:
            self.logo_label.config(text="G1", fg="white", font=("Arial", 40, "bold"))
        
        self.logo_label.place(relx=0.5, rely=0.2, anchor="center")

        # --- TITRE ---
        tk.Label(self, text="GROUPE 1", bg="#1a1a1a", fg="white", 
                 font=("Arial", 28, "bold")).place(relx=0.5, rely=0.35, anchor="center")
        
        tk.Label(self, text="P O R T A I L  É D U C A T I F", bg="#1a1a1a", fg="#38bdf8", 
                 font=("Arial", 10, "bold")).place(relx=0.5, rely=0.40, anchor="center")

        # --- CHAMPS DE SAISIE ---
        # Utilisateur
        tk.Label(self, text="NOM D'UTILISATEUR", bg="#1a1a1a", fg="#94a3b8", 
                 font=("Arial", 8, "bold")).place(relx=0.5, rely=0.50, anchor="center", width=300)
        self.entry_user = tk.Entry(self, font=("Arial", 12), bg="#ffffff", fg="#1e293b", 
                                   bd=0, insertbackground="#1e293b")
        self.entry_user.place(relx=0.5, rely=0.55, anchor="center", width=300, height=40)

        # Mot de passe
        tk.Label(self, text="MOT DE PASSE", bg="#1a1a1a", fg="#94a3b8", 
                 font=("Arial", 8, "bold")).place(relx=0.5, rely=0.62, anchor="center", width=300)
        self.entry_pass = tk.Entry(self, font=("Arial", 12), bg="#ffffff", fg="#1e293b", 
                                   bd=0, show="●", insertbackground="#1e293b")
        self.entry_pass.place(relx=0.5, rely=0.67, anchor="center", width=300, height=40)

        # --- BOUTON ---
        self.login_btn = tk.Button(self, text="SE CONNECTER", bg="#0ea5e9", fg="white", 
                                   font=("Arial", 11, "bold"), bd=0, cursor="hand2",
                                   activebackground="#0284c7", command=self.handle_login)
        self.login_btn.place(relx=0.5, rely=0.78, anchor="center", width=300, height=50)

        # Binds
        self.entry_user.bind("<Return>", lambda e: self.entry_pass.focus())
        self.entry_pass.bind("<Return>", lambda e: self.handle_login())
        self.entry_user.focus()

    def handle_login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get()
        if not username or not password:
            messagebox.showwarning("Erreur", "Veuillez remplir les champs.")
            return

        result = verify_login(username, password)
        if result:
            self.controller.login_success(username, result[1], result[0])
        else:
            messagebox.showerror("Accès refusé", "Identifiants invalides.")