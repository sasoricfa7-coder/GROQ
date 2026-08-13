from groq import Groq
import json
import os

def charger_memoire(MON_FICHIER) :
    if os.path.exists(MON_FICHIER) :
        with open(MON_FICHIER, "r", encoding="utf-8") as f :
            return json.load(f)

    else :
        return []

def sauvegarder_memoire(historique, MON_FICHIER) :
    with open(MON_FICHIER, "w", encoding="utf-8") as f :
        json.dump(historique, f, ensure_ascii=False, indent=4)

def main():
    MON_FICHIER = "memoire_chat.json"
    client = Groq() # N'oublie pas l'import au début du fichier !
    historique = charger_memoire(MON_FICHIER)

    while True:
        vous = input("vous : ")
        if vous.lower() == "exit": break # Petit bonus pour quitter proprement

        historique.append({"role": "user", "content": vous})

        # Appel API
        reponse = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=historique)
        reponse_ia = reponse.choices[0].message.content

        # Affichage et stockage
        print("-------------------------------------------------------------------\n")
        print(f"IA : {reponse_ia}")
        print("-------------------------------------------------------------------\n")
        historique.append({"role": "assistant", "content": reponse_ia})
        
        # Sauvegarde immédiate
        sauvegarder_memoire(historique, MON_FICHIER)

if __name__ == "__main__" :
    main()
