import streamlit as st
from agent_script import process_request
import asyncio
from dotenv import load_dotenv
import os

# Configuration de la page
st.set_page_config(
    page_title="Assistant Éducatif IA",
    page_icon="📚",
    layout="wide"
)

# Chargement des variables d'environnement
load_dotenv()

# Vérification des clés API
if not os.getenv("OPENAI_API_KEY") and not os.getenv("GEMINI_API_KEY"):
    st.error("Erreur : Aucune clé API n'est configurée dans le fichier .env")
    st.info("Veuillez configurer au moins une clé API (OpenAI ou Gemini)")
    st.stop()

# Titre de l'application
st.title("Assistant Éducatif IA")
st.subheader("Générateur d'exercices et de ressources pédagogiques")

# Sélection du niveau
niveau = st.selectbox(
    "Niveau scolaire",
    ["6ème", "5ème", "4ème", "3ème"]
)

# Sélection du pays
pays = st.selectbox(
    "Pays",
    ["Togo", "Bénin", "Côte d'Ivoire", "Sénégal"]
)

# Sélection de la matière
matiere = st.selectbox(
    "Matière",
    [
        "Mathématiques",
        "Éducation Civique et Morale",
        "Français",
        "Anglais",
        "Histoire-Géographie",
        "Sciences Physiques",
        "Sciences de la Vie et de la Terre"
    ]
)

# Zone de texte pour la demande
user_input = st.text_area(
    "Votre demande",
    placeholder=f"Exemple : Génère des exercices de {matiere} pour la {niveau} au {pays}"
)

# Type d'exercice selon la matière
if matiere == "Mathématiques":
    type_exercice = st.selectbox(
        "Type d'exercice",
        ["Calcul mental", "Problèmes", "Géométrie", "Fractions", "Conversions"]
    )
elif matiere == "Éducation Civique et Morale":
    type_exercice = st.selectbox(
        "Type d'exercice",
        ["Questions de réflexion", "Cas pratiques", "Analyse de situations", "Débats"]
    )
elif matiere == "Français":
    type_exercice = st.selectbox(
        "Type d'exercice",
        ["Grammaire", "Conjugaison", "Orthographe", "Compréhension de texte", "Rédaction"]
    )
elif matiere == "Anglais":
    type_exercice = st.selectbox(
        "Type d'exercice",
        ["Vocabulaire", "Grammaire", "Compréhension", "Expression écrite", "Expression orale"]
    )
elif matiere == "Histoire-Géographie":
    type_exercice = st.selectbox(
        "Type d'exercice",
        ["Questions de connaissances", "Analyse de documents", "Cartographie", "Chronologie"]
    )
elif matiere == "Sciences Physiques":
    type_exercice = st.selectbox(
        "Type d'exercice",
        ["Expériences", "Problèmes", "Théorie", "Applications pratiques"]
    )
elif matiere == "Sciences de la Vie et de la Terre":
    type_exercice = st.selectbox(
        "Type d'exercice",
        ["Observation", "Expérimentation", "Classification", "Analyse de documents"]
    )

# Bouton pour soumettre
if st.button("Générer"):
    if user_input:
        with st.spinner("Génération en cours..."):
            try:
                # Exécution de l'agent
                result = asyncio.run(process_request(user_input))
                
                # Affichage du résultat
                st.success("Exercices générés avec succès !")
                st.write(result)
            except Exception as e:
                st.error(f"Une erreur s'est produite : {str(e)}")
    else:
        st.warning("Veuillez entrer une demande")

# Pied de page
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Assistant Éducatif IA - Version 1.0</p>
    </div>
""", unsafe_allow_html=True) 