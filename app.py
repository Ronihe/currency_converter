from flask import (Flask, request, render_template, jsonify, session, flash)
from flask_debugtoolbar import DebugToolbarExtension
import currency

app = Flask(__name__)
app.config['SECRET_KEY'] = "a secret"
debug = DebugToolbarExtension(app)

# Key name will be used to store all the calculations we made in the sessions;
# put here as constants, so it will be consistent

CALCULATED_KEY = "calculated"


@app.route("/")
def show_convert_form():
    """Show convert currency form."""

    session[CALCULATED_KEY] = []
    return render_template("index.html")


@app.route("/calc_nums")
def show_converted_curr():
    """"show the converted currency"""

    convert_from = request.args.get("convert_from").upper()
    convert_to = request.args.get("convert_to").upper()
    amount = float(request.args.get("amount"))

    try:
        converted_amt = currency.convert(convert_from, convert_to, amount)
    except currency.exceptions.CurrencyException:
        convert_result = f"{convert_from} or {convert_to} is not valid currency, Please put in valid currency"
        return jsonify(result=convert_result)

    converted_amt_rounded = currency.rounding(converted_amt, convert_to)
    convert_from_rounded = currency.rounding(amount, convert_from)
    convert_to_currency_symbol = currency.symbol(convert_to)
    convert_result = f"{convert_from_rounded} {convert_from} is converted to {convert_to_currency_symbol} {converted_amt_rounded}"

    # save the calculated result to session
    calculated = session[CALCULATED_KEY]
    calculated.append(convert_result)
    session[CALCULATED_KEY] = calculated
    print(session[CALCULATED_KEY])

    return jsonify(
        result=convert_result, calculated=session[CALCULATED_KEY][-1])


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
