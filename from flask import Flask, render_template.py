from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import AccountingForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounting.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Model (defined in models.py)
from models import AccountingEntry

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    form = AccountingForm()
    if form.validate_on_submit():
        entry = AccountingEntry(
            description=form.description.data,
            amount=form.amount.data,
            entry_type=form.entry_type.data
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('tally'))
    return render_template('index.html', form=form)

# Tally route
@app.route('/tally')
def tally():
    income = db.session.query(db.func.sum(AccountingEntry.amount)).filter_by(entry_type='Income').scalar() or 0
    expenses = db.session.query(db.func.sum(AccountingEntry.amount)).filter_by(entry_type='Expense').scalar() or 0
    balance = income - expenses
    return render_template('tally.html', income=income, expenses=expenses, balance=balance)

if __name__ == '__main__':
    app.run(debug=True)
