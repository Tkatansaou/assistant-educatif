from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.base import ToolException
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
import asyncio
from dotenv import load_dotenv
import os

# Chargement des variables d'environnement
load_dotenv()

# Vérification des clés API
if not os.getenv("OPENAI_API_KEY") and not os.getenv("GEMINI_API_KEY"):
    raise ValueError("Aucune clé API n'est configurée dans le fichier .env")

@tool
def generer_exercices_maths(niveau: str, pays: str, type_exercice: str, nombre_exercices: int = 5) -> str:
    """Génère des exercices de mathématiques adaptés au niveau et au pays spécifiés."""
    return f"""Exercices de mathématiques pour {niveau} au {pays} :

1. Calcul mental :
   - 125 + 87 = ?
   - 256 - 134 = ?
   - 12 × 8 = ?
   - 144 ÷ 12 = ?

2. Problèmes :
   - Un marchand vend 3 sacs de riz à 2500 FCFA l'unité. Combien a-t-il gagné ?
   - Un rectangle a une longueur de 12 cm et une largeur de 8 cm. Calcule son périmètre.
   - Un élève a 15 bonbons. Il en donne 7 à son ami. Combien lui en reste-t-il ?

3. Géométrie :
   - Trace un carré de 5 cm de côté
   - Nomme les angles d'un triangle rectangle
   - Calcule l'aire d'un rectangle de 6 cm sur 4 cm

4. Fractions :
   - Simplifie la fraction 12/16
   - Calcule 1/4 + 1/2
   - Compare 3/4 et 2/3

5. Conversions :
   - Convertis 2,5 m en cm
   - Convertis 1500 g en kg
   - Convertis 2 heures en minutes"""

@tool
def generer_exercices_ecm(niveau: str, pays: str, type_exercice: str, nombre_exercices: int = 5) -> str:
    """Génère des exercices d'éducation civique et morale adaptés au niveau et au pays spécifiés."""
    return f"""Exercices d'Éducation Civique et Morale pour {niveau} au {pays} :

1. Questions de réflexion :
   - Quels sont les droits et devoirs d'un citoyen ?
   - Pourquoi est-il important de respecter les règles de vie en société ?
   - Comment peut-on contribuer au développement de son pays ?

2. Cas pratiques :
   - Que ferais-tu si tu voyais quelqu'un jeter des déchets par terre ?
   - Comment réagirais-tu face à une situation de discrimination ?
   - Comment peux-tu aider un camarade en difficulté ?

3. Analyse de situations :
   - Analysez cette situation : Un élève triche lors d'un examen
   - Que pensez-vous de cette situation : Un groupe d'élèves exclut un camarade
   - Comment réagiriez-vous face à cette situation : Un adulte demande de l'aide"""

@tool
def generer_exercices_francais(niveau: str, pays: str, type_exercice: str, nombre_exercices: int = 5) -> str:
    """Génère des exercices de français adaptés au niveau et au pays spécifiés."""
    return f"""Exercices de Français pour {niveau} au {pays} :

1. Grammaire :
   - Identifie la nature des mots soulignés
   - Transforme ces phrases à la voix passive
   - Trouve les compléments d'objet dans ces phrases

2. Conjugaison :
   - Conjugue ces verbes au présent
   - Mets ces phrases au passé composé
   - Transforme ces phrases au futur simple

3. Orthographe :
   - Corrige les fautes d'orthographe
   - Complète avec la bonne terminaison
   - Accorde les participes passés

4. Compréhension de texte :
   - Lis ce texte et réponds aux questions
   - Trouve l'idée principale du texte
   - Résume le texte en 5 lignes"""

@tool
def generer_exercices_anglais(niveau: str, pays: str, type_exercice: str, nombre_exercices: int = 5) -> str:
    """Génère des exercices d'anglais adaptés au niveau et au pays spécifiés."""
    return f"""Exercices d'Anglais pour {niveau} au {pays} :

1. Vocabulaire :
   - Traduis ces mots en français
   - Trouve les antonymes de ces mots
   - Complète avec le bon mot

2. Grammaire :
   - Mets ces phrases au présent simple
   - Utilise le comparatif
   - Transforme en questions

3. Compréhension :
   - Lis ce texte et réponds aux questions
   - Trouve les mots-clés
   - Résume en anglais

4. Expression :
   - Décris cette image
   - Rédige une courte lettre
   - Présente-toi en anglais"""

@tool
def generer_exercices_histoire_geo(niveau: str, pays: str, type_exercice: str, nombre_exercices: int = 5) -> str:
    """Génère des exercices d'histoire-géographie adaptés au niveau et au pays spécifiés."""
    return f"""Exercices d'Histoire-Géographie pour {niveau} au {pays} :

1. Questions de connaissances :
   - Cite les grandes périodes de l'histoire
   - Nomme les continents et les océans
   - Quels sont les pays limitrophes du {pays} ?

2. Analyse de documents :
   - Analyse cette carte historique
   - Que nous apprend ce document ?
   - Compare ces deux cartes

3. Cartographie :
   - Localise ces villes sur la carte
   - Trace le parcours de ce fleuve
   - Colorie les zones climatiques

4. Chronologie :
   - Classe ces événements dans l'ordre
   - Associe les dates aux événements
   - Crée une frise chronologique"""

@tool
def generer_exercices_sciences_physiques(niveau: str, pays: str, type_exercice: str, nombre_exercices: int = 5) -> str:
    """Génère des exercices de sciences physiques adaptés au niveau et au pays spécifiés."""
    return f"""Exercices de Sciences Physiques pour {niveau} au {pays} :

1. Expériences :
   - Décris une expérience pour montrer que l'air a une masse
   - Comment mesurer la température d'ébullition de l'eau ?
   - Propose une expérience sur la conductivité électrique

2. Problèmes :
   - Calcule la vitesse moyenne d'un objet
   - Détermine la force nécessaire pour soulever une masse
   - Calcule la puissance électrique consommée

3. Théorie :
   - Explique le principe d'Archimède
   - Décris les différents états de la matière
   - Qu'est-ce que l'énergie cinétique ?

4. Applications pratiques :
   - Comment économiser l'énergie à la maison ?
   - Explique le fonctionnement d'une pile
   - Décris les applications de l'électricité"""

@tool
def generer_exercices_svt(niveau: str, pays: str, type_exercice: str, nombre_exercices: int = 5) -> str:
    """Génère des exercices de SVT adaptés au niveau et au pays spécifiés."""
    return f"""Exercices de SVT pour {niveau} au {pays} :

1. Observation :
   - Observe cette plante et décris ses caractéristiques
   - Compare ces deux échantillons de sol
   - Décris les différentes parties de cette fleur

2. Expérimentation :
   - Propose une expérience pour montrer la photosynthèse
   - Comment observer des cellules au microscope ?
   - Expérience sur la germination des graines

3. Classification :
   - Classe ces animaux selon leur régime alimentaire
   - Identifie les différentes parties du corps humain
   - Classe ces plantes selon leurs caractéristiques

4. Analyse de documents :
   - Analyse ce graphique de croissance
   - Interprète ces résultats d'expérience
   - Explique ce schéma du cycle de l'eau"""

@tool
def analyser_texte(texte: str) -> str:
    """Analyse un texte pour en extraire les informations importantes."""
    return f"Analyse du texte : {texte}"

@tool
def traduire_texte(texte: str, langue_cible: str) -> str:
    """Traduit un texte dans la langue cible spécifiée."""
    return f"Traduction du texte en {langue_cible} : {texte}"

async def process_request(user_input: str) -> str:
    """Traite une demande utilisateur et retourne la réponse."""
    try:
        # Initialisation des modèles disponibles
        models = []
        
        if os.getenv("OPENAI_API_KEY"):
            models.append(ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7
            ))
        
        if os.getenv("GEMINI_API_KEY"):
            models.append(ChatGoogleGenerativeAI(
                model="gemini-pro",
                temperature=0.7
            ))
        
        # Utilisation du premier modèle disponible
        llm = models[0]
        
        # Création du prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Vous êtes un assistant spécialisé dans l'éducation qui peut :
            - Générer des exercices pour différentes matières
            - Analyser des textes
            - Traduire des textes
            Répondez de manière claire et pédagogique."""),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        # Création de l'agent
        tools = [
            generer_exercices_maths,
            generer_exercices_ecm,
            generer_exercices_francais,
            generer_exercices_anglais,
            generer_exercices_histoire_geo,
            generer_exercices_sciences_physiques,
            generer_exercices_svt,
            analyser_texte,
            traduire_texte
        ]
        agent = create_openai_functions_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # Exécution de l'agent
        result = await agent_executor.ainvoke({"input": user_input})
        return result["output"]
    
    except Exception as e:
        return f"Une erreur s'est produite : {str(e)}"

async def main():
    """Fonction principale pour l'exécution en ligne de commande."""
    try:
        print("\nBienvenue dans votre assistant IA pour l'éducation !")
        print("Je peux vous aider à :")
        print("- Générer des exercices pour différentes matières")
        print("- Analyser des textes")
        print("- Traduire des textes")
        print("\nTapez 'quit' pour quitter")
        
        while True:
            user_input = input("\nQue puis-je faire pour vous ? : ")
            
            if user_input.lower() == 'quit':
                break
                
            if user_input.strip():
                result = await process_request(user_input)
                print("\nRéponse :")
                print(result)
    
    except Exception as e:
        print(f"\nUne erreur s'est produite : {str(e)}")
        print("\nVérifiez que :")
        print("1. Vos clés API sont correctement configurées dans le fichier .env")
        print("2. Vos clés API sont valides et ont des crédits disponibles")
        print("3. Vous avez une connexion internet active")

if __name__ == "__main__":
    asyncio.run(main()) 