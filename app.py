from flask import Flask, render_template, request, url_for, redirect, flash
import mysql.connector as connector
import uuid
from flask_mail import Message, Mail
from itsdangerous import URLSafeSerializer, SignatureExpired
from validate import *
import os

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'earvinbaraka@gmail.com'
app.config['MAIL_PASSWORD'] = 'Commandprompt.1'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.secret_key = 'super secret key'
s = URLSafeSerializer('secretthistime!')

db = connector.connect(host="localhost", user="root", passwd="root", database="dairy")

# app = Flask(__name__)
app.config['SECRET_KEY'] = 'jxbxjxdjdjdjddj'


@app.route('/')
def home():
    return redirect(url_for('order'))


@app.route('/ok', methods=['GET', 'POST'])
def order():
    form = UserOrderForm()
    form.validate_on_submit()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        product = request.form["product"]
        quantity = request.form["quantity"]
        location = request.form['location']

        print(name, email, phone, product, quantity, location)
        cursor = db.cursor()
        sql = "INSERT INTO `gachagua`(`name`, `email`, `phone`, `product`, `quantity`, `location`, `id`) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (name, email, phone, quantity, product, location)
        cursor.execute(sql, val)
        db.commit()
        flash("saved in database")
        if sql:
            email = request.form['email']
            msg = Message(subject='Order received', sender='earvinbaraka@gmail.com',
                          recipients=[request.form['email']])
            # link = url_for('conf_email', token=token, page=page, _external=True)
            msg.body = render_template('result.html', result=result)
            mail.send(msg)
        return redirect(url_for('order'))
    return render_template('students.html', form=form)


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        page = render_template('result.html', result=result)
        msg = Message(subject='Order received', html=page, sender='earvinbaraka@gmail.com',
                      recipients=[request.form['email']])
        mail.send(msg)
    return render_template("result.html", result=result)


if __name__ == '__main__':
    app.run()
