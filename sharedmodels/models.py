from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db


facesetface = db.Table('faceset_face',
                       db.Column('faceset_id', db.Integer,
                                 db.ForeignKey('faceset.id')),
                       db.Column('face_id', db.Integer,
                                 db.ForeignKey('face.id')))


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    # Relationship
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    api_keys = db.relationship('APIKey', backref='user', lazy='dynamic')
    facesets = db.relationship('FaceSet', backref='user', lazy='dynamic')
    faces = db.relationship('Face', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class APIKey(db.Model):
    __tablename__ = 'apikey'
    id = db.Column(db.Integer, primary_key=True)
    application = db.Column(db.String(64))
    apikey = db.Column(db.String(64), unique=True)
    # Relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class FaceSet(db.Model):
    __tablename__ = 'faceset'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True)
    display_name = db.Column(db.String(256))
    # Relationship
    # faces = db.relationship('Face', backref='faceset', lazy='dynamic')
    faces = db.relationship('Face',
                            secondary=facesetface,
                            backref=db.backref('facesets', lazy='dynamic'),
                            lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Face(db.Model):
    __tablname__ = 'face'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True)
    encoding = db.Column(db.String(2048))
    # Relationship
    # faceset_id = db.Column(db.Integer, db.ForeignKey('faceset.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
