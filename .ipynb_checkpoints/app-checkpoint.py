from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

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
         
    # Après calcul bmi

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

    return render_template("index.html",
                       prediction=prediction,
                       bmi=bmi,
                       bmi_status=bmi_status,
                       advice=advice)

if __name__ == "__main__":
    app.run(debug=True)