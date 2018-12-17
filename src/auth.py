from flask import render_template, flash, redirect, url_for, session, g, flash
from .models import User, db
from .forms import AuthForm
from . import app
import functools


# Decorator:
def login_required(view):
    """
    Here, view is a function. This decorator wrap up this function
    and require
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # you can choose to redirect or abort
            # abort(404)
            flash("Please login first.")
            return redirect(url_for('.login'))

        # import pdb; pdb.set_trace()
        return view(**kwargs)

    # notice that we return uncalled wrapped_view function
    return wrapped_view


# hum...
@app.before_request
def load_logged_in_user():
    """
    Go get the user id from session if exist
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    """
    form = AuthForm()

    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']
        error = None

        if not email or not password:
            error = 'Invalid emial or password.'
        if User.query.filter_by(email=email).first() is not None:
            error = f'{ email } has already been registered.'
        if error is None:
            # username and password pair is good, allow register
            user = User(email=email, password=password)
            db.session.add(user)
            db.session.commit()

            flash('Registration compelte. Please Log in.')
            return redirect(url_for('.login'))
        flash(error)

    return render_template('auth/register.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    """
    """
    form = AuthForm()
    # import pdb; pdb.set_trace()

    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']
        error = None

        # we need to look up user and pw from database,
        # be caucious about malicious intent
        user = User.query.filter_by(email=email).first()

        if user is None or not User.check_password_hash(user, password):
            error = 'Invalid emial or password.'

        if error is None:
            # just be safe
            session.clear()

            # pass on user id info
            session['user_id'] = user.id
            return redirect(url_for('.portfolio_detail'))

        flash(error)

    return render_template('auth/login.html', form=form)


@app.route('/logout', methods=['GET','POST'])
def logout():
    """
    """
    # similar to local storage.clear()
    session.clear()
    flash('Logged out!')
    return redirect(url_for('.login'))
