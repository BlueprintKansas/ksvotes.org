from app.main import main
from flask import render_template, g, current_app
from app.main.helpers import guess_locale

@main.errorhandler(404)
def page_not_found(_e):
    g.locale = guess_locale()
    return render_template('404.html'), 404

@main.errorhandler(500)
def page_exception(_e):
    g.locale = guess_locale()
    return render_template('500.html'), 500

@main.errorhandler(Exception)
def unhandled_exception(e):
    current_app.logger.error('Unhandled Exception: %s', (e))
    return page_exception(e)

@main.route('/throw-error', methods=['GET'])
def throw_error():
    raise Exception('Oops')

# catch any route that does not match a known route
# see https://github.com/pallets/flask/issues/1498
@main.route("/<path:invalid_path>")
def handle_unmatchable(*args, **kwargs):
    return page_not_found(None)
