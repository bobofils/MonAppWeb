import os

fichier = "taches.txt"

# Charger les tâches si le fichier existe
if os.path.exists(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        taches = [ligne.strip() for ligne in f.readlines()]
else:
    taches = []

while True:
    print("\n--- Gestionnaire de tâches ---")
    print("1. Ajouter une tâche")
    print("2. Voir les tâches")
    print("3. Supprimer une tâche")
    print("4. Quitter")

    choix = input("Choisissez une option : ")

    if choix == "1":
        tache = input("Entrez la tâche : ")
        taches.append(tache)
        print("Tâche ajoutée !")

    elif choix == "2":
        if len(taches) == 0:
            print("Aucune tâche.")
        else:
            for i, t in enumerate(taches):
                print(f"{i + 1}. {t}")

    elif choix == "3":
        numero = int(input("Numéro de la tâche à supprimer : "))
        if 0 < numero <= len(taches):
            taches.pop(numero - 1)
            print("Tâche supprimée.")
        else:
            print("Numéro invalide.")

    elif choix == "4":
        # Sauvegarder les tâches avant de quitter
        with open(fichier, "w", encoding="utf-8") as f:
            for t in taches:
                f.write(t + "\n")
        print("Tâches sauvegardées. Au revoir !")
        break

    else:
        print("Option invalide.")