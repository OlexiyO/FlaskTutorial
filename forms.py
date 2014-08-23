from app.models import User
from flask.ext.wtf import Form
from wtforms import BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
  openid = StringField('openid', validators = [DataRequired()])
  remember_me = BooleanField('remember_me', default = False)


class EditForm(Form):
  nickname = StringField('nickname', validators = [DataRequired()])
  about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])

  def __init__(self, my_nickname, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
    self._my_nickname = my_nickname

  def validate(self):
    if not Form.validate(self):
      return False
    if self._my_nickname == self.nickname.data:
      return True
    if User.NicknameExists(self.nickname.data):
      self.nickname.errors.append(
          'Name %s is already used! How about %s?' %
          (self.nickname.data, User.make_unique_nickname(self.nickname.data)))
      return False
    return True
