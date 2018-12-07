# here we want to deal with exceptions (largely) from user input
from . import app
from flask import render_template

@app.errorhandler(404)
def not_found(error):
    """
    """
    return render_template('404_notfound.html', error = error), 404