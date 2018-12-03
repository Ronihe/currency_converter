from flask import (Flask, request, render_template, jsonify, session)
from flask_debugtoolbar import DebugToolbarExtension
import currency

app = Flask(__name__)
app.config['SECRET_KEY'] = "a secret"
debug = DebugToolbarExtension(app)

# Key name will be used to store all the calculations we made in the sessions;
# put here as constants, so it will be consistent

CALCULATED_KEY = "calculated"


def format_currency(amt, curr):
    """ format amt and curr to a better format"""

    return f"{currency.symbol(curr)} {currency.rounding(amt, curr)}"


@app.route("/")
def show_convert_form():
    """Show convert currency form."""

    # Check if session data exists
    # If CALCULATED_KEY EXISTS IN SESSION KEY, KEEP, OTHERWISE SET KEY TO EMPTY LIST
    if session.get(CALCULATED_KEY):
        print(session[CALCULATED_KEY])
    else:
        session[CALCULATED_KEY] = []

    return render_template("index.html", calculations=session[CALCULATED_KEY])


@app.route("/calc_nums")
def show_converted_curr():
    """"show the converted currency"""

    convert_from = request.args.get("convert_from").upper()
    convert_to = request.args.get("convert_to").upper()
    amount = float(request.args.get("amount"))

    try:
        converted_amt = currency.convert(convert_from, convert_to, amount)
    except currency.exceptions.CurrencyException:
        convert_result = f"Conver From {convert_from} or Convert To{convert_to} is not valid currency, Please put in valid currencies"
        return jsonify(
            result=convert_result, calculated=session[CALCULATED_KEY])

    formattet_convert_from = format_currency(amount, convert_from)
    formattet_convert_to = format_currency(converted_amt, convert_to)

    convert_result = f"{formattet_convert_from} is converted to {formattet_convert_to}"

    # save the calculated result to session
    calculated = session[CALCULATED_KEY]
    calculated.append(convert_result)
    session[CALCULATED_KEY] = calculated

    return jsonify(result=convert_result, calculated=session[CALCULATED_KEY])
