from flask import render_template, redirect, url_for, abort, request, flash, session
from sqlalchemy.exc import DBAPIError, IntegrityError
from .forms import CompanySearchForm, CompanyAddForm
from .models import Company, db
from . import app # we can do this bcz we define all those lines in the __init__.py
import requests as req
import json
import os

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
    if form.validate_on_submit():
    # if request.method == 'POST':
        # everything here are about POST
        symbol = form.data['symbol']
        res = req.get(f'https://api.iextrading.com/1.0/stock/{ form.data["symbol"] }/company')

        # try:
        #     data = json.loads(res.text)
        #     company = {
        #         'symbol' : data['symbol'],
        #         'companyName' : data['companyName'],
        #         'exchange': data['exchange'],
        #         'industry': data['industry'],
        #         'website' : data['website'],
        #         'description' : data['description'],
        #         'CEO' : data['CEO'],
        #         'issueType' : data['issueType'],
        #         'sector' : data['sector'],
        #     }
        #     new_company = Company(**company)
            # db.session.add(new_company)
            # db.session.commit()
        data = json.loads(res.text)
        session['context'] = data
        session['symbol'] = symbol

        return redirect(url_for('.portfolio_detail'))

        # except json.JSONDecodeError: # will be when the json.loads got empty
        #     abort(404)


    # here we handle GET
    return render_template('portfolio/search.html', form = form)

@app.route('/preview', methods = ['GET','POST'])
def preview_stock():
    """
    """
    form_context = {
        'name': session['context']['name'],
        'symbol':session['symbol'],
    }
    form = CompanyAddForm(**form_context)

    if form.validate_on_submit():
        try:
            company = Company(name = form.data['name'], symbol = form.data['symbol'])
            db.session.add(company)
            db.session.commit()
        except (DBAPIError, IntegrityError):
            flash("Opps...something went wrong!")
            return render_template('portfolio/search.html', form=form)

        return redirect(url_for('.portfolio_detail'))

    return render_template(
        'portfolio/preview.html',
        form=form,
        symbol = form_context['symbol'],
        stock_data = session['context'],
    )

@app.route('/portfolio')
def portfolio_detail():
    """
    """
    companies = Company.query.all()  #somehow this line not really working...
    return render_template('portfolio/portfolio.html', companies = companies)
