from groq import Groq
import json
import os
import socket


def verifier_connexion():
  """Vérifie si une connexion Internet est active."""
  try:
    # Tente de se connecter au DNS de Google sur le port 53 (délai de 3 secondes max)
    socket.create_connection(("8.8.8.8", 53), timeout=3)
    return True
  except OSError:
    return False


def charger_memoire(MON_FICHIER):
  if os.path.exists(MON_FICHIER):
    with open(MON_FICHIER, "r", encoding="utf-8") as f:
      return json.load(f)
  else:
    return []


def sauvegarder_memoire(historique, MON_FICHIER):
  with open(MON_FICHIER, "w", encoding="utf-8") as f:
    json.dump(historique, f, ensure_ascii=False, indent=4)


def main():
  MON_FICHIER = "memoire_chat.json"

  # Vérification d'Internet avant de lancer le client ou de boucler
  if not verifier_connexion():
    print(
        "❌ Erreur : Aucune connexion Internet détectée. Veuillez vérifier"
        " votre réseau."
    )
    return

  client = Groq()
  historique = charger_memoire(MON_FICHIER)

  while True:
    vous = input("vous : ")
    if vous.lower() == "exit":
      break
    elif vous.lower() == "clear":
      os.system("clear")
      continue

    historique.append({"role": "user", "content": vous})

    # Vérification du réseau à chaque tour + Bloc de sécurité (try/except)
    if not verifier_connexion():
      print(
          "❌ Connexion perdue ! Impossible d'envoyer le message à Groq."
      )
      # On retire le dernier message utilisateur pour ne pas fausser l'historique
      historique.pop()
      continue

    try:
      # Appel API
      reponse = client.chat.completions.create(
          model="llama-3.3-70b-versatile", messages=historique
      )
      reponse_ia = reponse.choices[0].message.content

      # Affichage et stockage
      print(
          "-------------------------------------------------------------------\n"
      )
      print(f"IA : {reponse_ia}")
      print(
          "-------------------------------------------------------------------\n"
      )
      historique.append({"role": "assistant", "content": reponse_ia})

      # Sauvegarde immédiate
      sauvegarder_memoire(historique, MON_FICHIER)

    except Exception as e:
      print(f"⚠️ Une erreur est survenue avec l'API Groq : {e}")
      # On retire le message pour éviter un décalage dans l'historique
      historique.pop()


if __name__ == "__main__":
  main()
