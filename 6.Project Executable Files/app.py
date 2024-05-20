import pickle as pkl

from flask import Flask, request, render_template

app = Flask(__name__)

model_loaded = pkl.load(open('model (2).pkl', 'rb'))

@app.route('/')

def indput():
    return render_template('portfolio-details.html', prediction_result=None)

month_names_to_int = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}
company_names_to_int = {
    'AMD': 1,
    'ASUS': 2,
    'INTEL': 3,
    'MSI':4,
    'NVIDIA':5
    # Add more company mappings as needed
}

@app.route("/predict", methods=['POST', 'GET'])

def predict():
    if request.method == 'POST':
        low = float(request.form["Low"])
        high = float(request.form["High"])
        volume = float(request.form["Volume"])
        open_val = float(request.form["Open"])
        year = int(request.form["Year"])
        month_name = request.form["Month"]
        month=month_names_to_int.get(month_name)
        if month is None:
            return "Invalid month name"

        day = int(request.form["Day"])
        # company = request.form["Company"]
        company_name = request.form["Company"]
        company = company_names_to_int.get(company_name)
        if company is None:
            return "Invalid company name"


        xx = model_loaded.predict([[open_val, high, low, volume, year, month, day, company]])
        out = xx[0]
        print("Forecasted closing price on {}/{}/{} is $ {}".format(day, month, year, out))

        return render_template("portfolio-details.html",prediction_result="Forecasted closing price on {}/{}/{} is $ {}".format(day, month, year, out))
    else:
        return render_template("portfolio-details.html", prediction_result=None)

if __name__ == '__main__':
    app.run (debug=True ,port=8000)
