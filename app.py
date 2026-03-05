from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# 🔥 Charger le modèle et les colonnes
model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        age = float(request.form["Age"])
        height = float(request.form["Height"])
        weight = float(request.form["Weight"])
        fcvc = float(request.form["FCVC"])
        ncp = float(request.form["NCP"])
        ch2o = float(request.form["CH2O"])
        faf = float(request.form["FAF"])
        tue = float(request.form["TUE"])

        # 🔥 Calcul IMC
        bmi = round(weight / (height ** 2), 2)

        # Préparer le DataFrame pour le modèle
        data = {
            "Age": age,
            "Height": height,
            "Weight": weight,
            "FCVC": fcvc,
            "NCP": ncp,
            "CH2O": ch2o,
            "FAF": faf,
            "TUE": tue
        }

        df = pd.DataFrame([data])
        df = pd.get_dummies(df)
        df = df.reindex(columns=columns, fill_value=0)

        prediction = model.predict(df)[0]

        # 🩺 État IMC et conseil
        if bmi < 18.5:
            bmi_status = "Insuffisance pondérale"
            advice = "Augmenter légèrement l'apport calorique et consulter un spécialiste."
        elif bmi < 25:
            bmi_status = "Poids normal"
            advice = "Continuez vos bonnes habitudes !"
        elif bmi < 30:
            bmi_status = "Surpoids"
            advice = "Augmenter l'activité physique et surveiller l'alimentation."
        else:
            bmi_status = "Obésité"
            advice = "Consulter un professionnel de santé et adopter un mode de vie actif."

        # 🔥 Score santé simple basé sur habitudes
        score = round((fcvc + ch2o + faf) * 10)
        score = min(score, 100)

        return render_template("index.html",
                               prediction=prediction,
                               bmi=bmi,
                               bmi_status=bmi_status,
                               advice=advice,
                               score=score)

    except Exception as e:
        return render_template("index.html", prediction="Erreur : Veuillez vérifier vos entrées.")

if __name__ == "__main__":
    app.run(debug=True)