from flask import request, Flask, render_template, abort, redirect, \
url_for, session, g, make_response

from .form import StockSearchForm
import requests as req


app = Flask(__name__)

def fetch_stock_info(stock):
    return req.get(f"{os.getenv('API_URL')}{stock}"+"/company")


@app.route('/')
def home():
    """
    Render and send the base home page to user.
    """
    return render_template('home_page.html'), 200


@app.route('/portfolio')
def portfolio():
    """
    The page for portfolio which shall be under construction right now.
    """
    return render_template('portfolio.html'), 200


@app.route('/search', methods = ['GET','POST'])
def stock_search():
    """
    """
    form = StockSearchForm()
    # import pdb; pdb.set_trace()
    if form.validate_on_submit():
        stock = form.data['stock_name']
        res = fetch_stock(stock)

        try:
            # not sure what we do here...
            session['companyName'] = res.text
            return redirect(url_for('.city_detail'))

        except:
            abort(404)

    # if request.method == 'GET':
    #     return render_template('portfolio.html'), 200

    if request.method == 'POST':
        return redirect("./portfolio", code=201)
#     # form =
#     pass



# @app.route('/search', method = 'POST')
