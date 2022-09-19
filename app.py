from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    tel = db.Column(db.Integer, nullable=True, unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    url = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<contacts {self.id}>"



@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        name = request.form['name']
        title = request.form['title']
        tel = request.form['tel']
        url = request.form['url']

        contact = Contacts(name=name, title=title, tel=tel, url=url)
        try:
            db.session.add(contact)
            db.session.commit()
            return redirect('/table_contacts')
        except:
            return 'При добавлении контакта произошла ошибка'
    else:
        return render_template('index.html', title="Добавление контакта")


@app.route('/table_contacts')
def table_contacts():
    contacts = Contacts.query.all()
    return render_template('table_contacts.html', contacts=contacts, title="Контакты")

@app.route('/table_contacts/<int:id>')
def contacts_detail(id):
    contact = Contacts.query.get(id)
    return render_template('contacts_detail.html', contact=contact, title=contact.title)

@app.route('/table_contacts/<int:id>/delete')
def contact_delete(id):
    contact = Contacts.query.get_or_404(id)
    try:
        db.session.delete(contact)
        db.session.commit()
        return redirect(url_for('table_contacts'))
    except:
        return "При удалении контакта произошла ошибка"

@app.route('/table_contacts/<int:id>/update', methods=['POST', 'GET'])
def contact_update(id):
    contact = Contacts.query.get(id)
    if request.method == "POST":
        if request.form['name']:
            contact.name = request.form['name']
        if request.form['title']:
            contact.title = request.form['title']
        if request.form['tel']:
            contact.tel = request.form['tel']
        if request.form['url']:
            contact.url = request.form['url']

        try:
            db.session.commit()
            return redirect('/table_contacts')
        except:
            return "При редактировании контакта произошла ошибка"
    else:
        contact = Contacts.query.get(id)
        return render_template('contact_update.html', contact=contact,title="Обновление контакта")


if __name__ == "__main__":
    app.run(debug=True)
