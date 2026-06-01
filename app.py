from flask import Flask, render_template, request, redirect, url_for
from models import db, Expense
from datetime import datetime

app = Flask(__name__)

#MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sameer@localhost/expense_tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# DASHBOARD
@app.route('/')
def dashboard():

    expenses = Expense.query.order_by(Expense.date.desc()).all()

    total_income = sum(e.amount for e in expenses if e.category == 'Income')
    total_expense = sum(e.amount for e in expenses if e.category == 'Expense')
    remaining = total_income - total_expense

    return render_template(
        'dashboard.html',
        total_income=total_income,
        total_expense=total_expense,
        remaining=remaining
    )


#ADD PAGE
@app.route('/addExpense')
def add_page():
    return render_template('add_expense.html')


#ADD SAVE
@app.route('/add', methods=['POST'])
def add():

    new_expense = Expense(
        title=request.form['title'],
        amount=float(request.form['amount']),
        category=request.form['category'],
        date=datetime.utcnow()
    )

    db.session.add(new_expense)
    db.session.commit()

    return redirect(url_for('history'))


#HISTORY
@app.route('/history')
def history():

    expenses = Expense.query.order_by(Expense.date.desc()).all()

    return render_template('expense_history.html', expenses=expenses)


#EDIT
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    expense = Expense.query.get_or_404(id)

    if request.method == 'POST':

        expense.title = request.form['title']
        expense.amount = float(request.form['amount'])
        expense.category = request.form['category']

        db.session.commit()

        return redirect(url_for('history'))

    return render_template('edit.html', expense=expense)


#DELETE
@app.route('/delete/<int:id>')
def delete(id):

    expense = Expense.query.get_or_404(id)

    db.session.delete(expense)
    db.session.commit()

    return redirect(url_for('history'))


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)