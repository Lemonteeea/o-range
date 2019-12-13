from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('E-mail', validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    password2 = PasswordField(
            'Repeat Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Regist')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Username is already used')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('This E-mail is already used')

class MusicselectForm(FlaskForm):
    music_list=[("kblk","开不了口"),("ljf","龙卷风"),("ah","暗号"),('caihong','彩虹'),('feng','枫'),('jda','简单爱'),('ylxb','一路向北'),('azxyq','爱在西元前'),('qlx','七里香'),('gq','搁浅'),('hdgq','回到过去'),('xq','星晴'),('jk','借口')]
    music = SelectField('选择歌曲',choices=music_list)
    submit = SubmitField('就听这首吧')
