from flask import request, Flask, render_template, abort, redirect, url_for, session, g, make_response

app = Flask(__name__)

@app.route('/')
def home():
    """
    """
    return render_template('home_page.html'), 200


@app.route('/search', method = ['GET','POST'])
def stock_search():
    """
    """
    if request.method == 'POST':

#     # form =
#     pass



# @app.route('/search', method = 'POST')
