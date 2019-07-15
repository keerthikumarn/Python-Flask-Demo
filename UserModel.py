from settings import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return str({
            'username': self.username,
            'password': self.password
        })

    def creds_match(uname, pwd):
        user = User.query.filter_by(username=uname).filter_by(password=pwd).first()
        if user is None:
            return False
        else:
            return True

    def create_user(username, password):
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
