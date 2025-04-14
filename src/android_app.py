from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.dialog import MDDialog
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import asyncio
from agent_script import process_request

class AssistantEducatifApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Light"
        
        # Configuration de la fenêtre
        Window.size = (360, 640)  # Taille standard pour mobile
        
        # Création de l'écran principal
        screen = MDScreen()
        
        # Layout principal
        layout = MDBoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )
        
        # Titre
        title = MDLabel(
            text="Assistant Éducatif IA",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height=50
        )
        layout.add_widget(title)
        
        # Sélection du niveau
        self.niveau = MDTextField(
            hint_text="Niveau scolaire (6ème, 5ème, 4ème, 3ème)",
            mode="rectangle"
        )
        layout.add_widget(self.niveau)
        
        # Sélection du pays
        self.pays = MDTextField(
            hint_text="Pays (Togo, Bénin, Côte d'Ivoire, Sénégal)",
            mode="rectangle"
        )
        layout.add_widget(self.pays)
        
        # Sélection de la matière
        self.matiere = MDTextField(
            hint_text="Matière",
            mode="rectangle"
        )
        layout.add_widget(self.matiere)
        
        # Type d'exercice
        self.type_exercice = MDTextField(
            hint_text="Type d'exercice",
            mode="rectangle"
        )
        layout.add_widget(self.type_exercice)
        
        # Zone de texte pour la demande
        self.demande = MDTextField(
            hint_text="Votre demande",
            mode="rectangle",
            multiline=True
        )
        layout.add_widget(self.demande)
        
        # Bouton de génération
        self.btn_generer = MDRaisedButton(
            text="Générer",
            on_release=self.generer_exercices
        )
        layout.add_widget(self.btn_generer)
        
        # Zone de résultat
        self.resultat = MDLabel(
            text="",
            halign="left",
            valign="top",
            size_hint_y=None,
            markup=True
        )
        
        # ScrollView pour le résultat
        scroll = ScrollView()
        scroll.add_widget(self.resultat)
        layout.add_widget(scroll)
        
        screen.add_widget(layout)
        return screen
    
    def generer_exercices(self, *args):
        # Désactiver le bouton pendant la génération
        self.btn_generer.disabled = True
        
        # Afficher un spinner
        self.spinner = MDSpinner()
        self.root.add_widget(self.spinner)
        
        # Préparer la demande
        demande = f"Génère des exercices de {self.matiere.text} pour la {self.niveau.text} au {self.pays.text}. Type d'exercice : {self.type_exercice.text}"
        
        # Exécuter la génération dans un thread séparé
        def run_generation():
            try:
                result = asyncio.run(process_request(demande))
                self.update_ui(result)
            except Exception as e:
                self.show_error(str(e))
            finally:
                self.btn_generer.disabled = False
                self.root.remove_widget(self.spinner)
        
        import threading
        threading.Thread(target=run_generation).start()
    
    def update_ui(self, result):
        self.resultat.text = result
        self.resultat.text_size = (Window.width - 20, None)
        self.resultat.height = self.resultat.texture_size[1]
    
    def show_error(self, message):
        dialog = MDDialog(
            title="Erreur",
            text=message,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

if __name__ == "__main__":
    AssistantEducatifApp().run() 