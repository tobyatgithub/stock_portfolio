from flask import render_template, redirect, url_for, abort, request
from .forms import CompanySearchForm
from .models import Company, db
import requests as req
from . import app # we can do this bcz we define all those lines in the __init__.py
import json

@app.route('/')
def home():
    """
    """
    return render_template('home.html')


@app.route('/search', methods = ['GET','POST'])
def company_search():
    """
    """
    form = CompanySearchForm()

    # check 1. whehter the method is post and 2.whether data is valid
    # so that we don't need if request.method == POST:
    # if form.validate_on_submit():
    if request.method == 'POST':
        # everything here are about POST

        res = req.get(f'https://api.iextrading.com/1.0/stock/{ form.data["symbol"] }/company')
        try:
            data = json.loads(res.text)
            company = {
                'symbol' : data['symbol'],
                'companyName' : data['companyName'],
                'exchange': data['exchange'],
                'industry': data['industry'],
                'website' : data['website'],
                'description' : data['description'],
                'CEO' : data['CEO'],
                'issueType' : data['issueType'],
                'sector' : data['sector'],
            }
            new_company = Company(**company)

            db.session.add(new_company)
            db.session.commit()

            return redirect(url_for('.portfolio_detail'))

        except json.JSONDecodeError: # will be when the json.loads got empty
            abort(404)


    # here we handle GET
    return render_template('portfolio/search.html', form = form)


@app.route('/portfolio')
def portfolio_detail():
    """
    """
    return render_template('portfolio/portfolio.html')
