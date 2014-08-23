from datetime import datetime
import app
from _hashlib import openssl_md5

db = app.db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  nickname = db.Column(db.String(64), unique = True)
  email = db.Column(db.String(120), unique = True)
  role = db.Column(db.SmallInteger, default = ROLE_USER)
  posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
  about_me = db.Column(db.String(140))
  last_seen = db.Column(db.DateTime)

  def __repr__(self):
    return '<User %r>' % self.nickname

  def is_authenticated(self):
    # Set False if user is not allowed to authenticate.
    return True

  def is_active(self):
    # False for banned
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return unicode(self.id)

  def avatar(self, size):
    return 'http://www.gravatar.com/avatar/' + openssl_md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

  @staticmethod
  def make_unique_nickname(candidate):
    if not User.NicknameExists(candidate):
      return candidate
    for n in range(2, 1000):
      cand = '%s_%d' % (candidate, n)
      if not User.NicknameExists(cand):
        return cand
    return '%s_%s' % datetime.utcnow()

  @staticmethod
  def NicknameExists(nickname):
    return User.query.filter_by(nickname=nickname).count() > 0

class Post(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  body = db.Column(db.String(140))
  timestamp = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return '<Post %r>' % self.body