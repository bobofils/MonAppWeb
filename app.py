from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
fichier = "taches.txt"

# Charger les tâches
if os.path.exists(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        taches = [ligne.strip() for ligne in f.readlines()]
else:
    taches = []

# Page principale
@app.route("/", methods=["GET", "POST"])
def index():
    global taches
    if request.method == "POST":
        # Ajouter une tâche
        nouvelle_tache = request.form.get("tache")
        if nouvelle_tache:
            taches.append(nouvelle_tache)
            with open(fichier, "w", encoding="utf-8") as f:
                for t in taches:
                    f.write(t + "\n")
        return redirect(url_for("index"))
    return render_template("index.html", taches=taches)

# Supprimer une tâche
@app.route("/supprimer/<int:index>")
def supprimer(index):
    global taches
    if 0 <= index < len(taches):
        taches.pop(index)
        with open(fichier, "w", encoding="utf-8") as f:
            for t in taches:
                f.write(t + "\n")
    return redirect(url_for("index"))

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render fournit le port, sinon 5000 pour tests locaux
    app.run(host="0.0.0.0", port=port, debug=True)