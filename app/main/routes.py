from flask import session, render_template, url_for, redirect

from app.main.forms import JoinForm
from . import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    form = JoinForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('room.room', title=session.get('room', '')))
    return render_template('index.html', form=form)

