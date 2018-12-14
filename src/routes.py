from flask import render_template, redirect, url_for, abort, request, flash, session, g
from .forms import CompanySearchForm, CompanyAddForm, PortfolioCreateForm
from sqlalchemy.exc import DBAPIError, IntegrityError
from .models import Company, db, Portfolio
from .auth import login_required
from . import app # we can do this bcz we define all those lines in the __init__.py
import requests as req
import json
import os

@app.add_template_global
def get_portfolios():
    """
    """
    return Portfolio.query.all()

@app.route('/')
def home():
    """
    """
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
# protect company_search page:
@login_required
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
        res = req.get(f'https://api.iextrading.com/1.0/stock/{form.data["symbol"]}/company')

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
        # flash('Ok..we got your request!')
        data = json.loads(res.text)
        session['context'] = data
        session['symbol'] = symbol
        return redirect(url_for('.preview_stock'))
        # except json.JSONDecodeError: # will be when the json.loads got empty
        #     abort(404)
    # here we handle GET
    return render_template('portfolio/search.html', form=form)


@app.route('/preview', methods=['GET', 'POST'])
@login_required
def preview_stock():
    """
    """
    # session['context'] example:
    # {'CEO': 'Jeffrey P. Bezos', 'companyName': 'Amazon.com Inc.', 'description':
    # 'Amazon.com Inc is an online retailer. The Company sells its products through
    # the website which provides services, such as advertising services and co-branded
    # credit card agreements. It also offers electronic devices like Kindle e-readers and Fire tablets.',
    # 'exchange': 'Nasdaq Global Select', 'industry': 'Retail - Apparel & Specialty',
    # 'issueType': 'cs', 'sector': 'Consumer Cyclical', 'symbol': 'AMZN', 'tags': ['Consumer Cyclical',
    # 'Specialty Retail', 'Retail - Apparel & Specialty'], 'website': 'http://www.amazon.com'}
    form_context = {
        'name': session['context']['companyName'],
        'symbol': session['symbol'],
        'CEO': session['context']['CEO'],
        # 'description':session['context']['description'],
        # 'exchange':session['context']['exchange'],
        # 'industry':session['context']['industry'],

    }
    form = CompanyAddForm(**form_context)
    # import pdb; pdb.set_trace()
    if form.validate_on_submit():
        try:
            company = Company(
                name=form.data['name'],
                symbol=form.data['symbol'],
                CEO=form.data['CEO'],
                portfolio_id=form.data['portfolios'],
            )
            db.session.add(company)
            db.session.commit()
        except (DBAPIError, IntegrityError):
            flash("Opps...something went wrong!")
            return render_template('portfolio/search.html', form=form)

        return redirect(url_for('.portfolio_detail'))

    return render_template(
        'portfolio/preview.html',
        form=form,
        symbol=form_context['symbol'],
        company_data=session['context'],
    )

@app.route('/portfolio', methods=['GET', 'POST'])
@login_required
def portfolio_detail():
    """
    """
    form = PortfolioCreateForm()

    if form.validate_on_submit():
        # flash('OK we received form.')
        try:
            # db.session.clear()
            portfolio = Portfolio(name=form.data['name'], user_id=g.user.id)
            db.session.add(portfolio)
            db.session.commit()
        except (DBAPIError, IntegrityError):
            flash('Opps, something went bad uhhh.')
            return render_template('portfolio/portfolio.html', form=form)

        return redirect(url_for('.company_search'))

    user_portfolios = Portfolio.query.filter(Portfolio.user_id == g.user.id).all()
    por_ids = [p.id for p in user_portfolios]

    companies = Company.query.filter(Company.portfolio_id.in_(por_ids)).all()
    # companies = Company.query.all()
    # portfolios = Portfolio.query.all()
    # import pdb; pdb.set_trace()
    return render_template(
        'portfolio/portfolio.html',
        companies=companies,
        portfolios=user_portfolios,
        form=form)
