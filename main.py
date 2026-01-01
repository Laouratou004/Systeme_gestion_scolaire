import tkinter as tk
from tkinter import messagebox
from views.login_view import LoginFrame
from views.admin_view import AdminFrame
from views.teacher_view import TeacherFrame
from views.student_view import StudentFrame
from database import get_connection

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Système de Gestion Scolaire - Groupe 1")
        self.geometry("1400x800")
        self.resizable(True, True)
        
        # Icône de fenêtre (optionnel)
        try:
            self.iconbitmap("icon.ico")
        except:
            pass
        
        self.current_user = None
        self.current_role = None
        self.current_frame = None
        
        # Afficher l'écran de connexion au démarrage
        self.show_login()
    
    def show_login(self):
        """Affiche l'écran de connexion"""
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = LoginFrame(self, self)
        self.current_frame.pack(fill="both", expand=True)
    
    def login_success(self, username, role, user_id):
        """Appelé après une connexion réussie"""
        self.current_user = username
        self.current_role = role
        
        if self.current_frame:
            self.current_frame.destroy()
        
        # Afficher l'interface selon le rôle
        if role == "Admin":
            self.current_frame = AdminFrame(self, self)
        elif role == "Enseignant":
            self.current_frame = TeacherFrame(self, self, user_id)
        elif role == "Étudiant":
            self.current_frame = StudentFrame(self, self, user_id)
        else:
            messagebox.showerror("Erreur", "Rôle non reconnu")
            self.show_login()
            return
        
        self.current_frame.pack(fill="both", expand=True)
    
    def logout(self):
        """Déconnexion de l'utilisateur"""
        self.current_user = None
        self.current_role = None
        self.show_login()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()