from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
db = SQLAlchemy(app)

# Replace [PASSWORD] with the root password for your mysql container
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{getenv("MYSQL_ROOT_PASSWORD")}@mysql:3306/trio_db'

class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(30), nullable=False)
	last_name = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(150), nullable=False, unique=True)
	def __repr__(self):
		return ''.join(['User ID: ', str(self.id), '\r\n', 'Email: ', self.email, ' Name: ', self.first_name, ' ', self.last_name, '\n'])


@app.route('/')
def hello():
  data1 = Users.query.all()
  return render_template('home.html', data1=data1)

@app.route('/new/<fname>-<lname>-<email>')
def add(fname, lname, email):
	user = Users(first_name=fname, last_name=lname, email=email)
	db.session.add(user)
	db.session.commit()
	return redirect(url_for('hello'))

if __name__=='__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)