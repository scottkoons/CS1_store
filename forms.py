from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, HiddenField, SelectField, DecimalField, FileField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError, email_validator
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import configure_uploads, IMAGES, UploadSet, UploadNotAllowed, patch_request_class


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[
                           InputRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     InputRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
                           InputRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login Now')


class AddProduct(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    price = DecimalField('Price')
    stock = IntegerField('Stock')
    description = TextAreaField('Description')
    image = FileField('Image', validators=[
                      FileAllowed(IMAGES, 'Only images are accepted.')])

    submit = SubmitField('Save Product')


class UpdateProduct(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    price = DecimalField('Price')
    stock = IntegerField('Stock')
    description = TextAreaField('Description')
    image = FileField('Image', validators=[
                      FileAllowed(IMAGES, 'Only images are accepted.')])

    submit = SubmitField('Update Product')


class Checkout(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone_number = StringField('Number')
    email = StringField('Email')
    address = StringField('Address')
    city = StringField('City')
    state = SelectField('State',
                        choices=[('CO', 'Colorado'), ('CA', 'California'), ('WA', 'Washington')
                                 ])
    country = SelectField('Country',
                          choices=[('US', 'United States'),
                                   ('UK', 'United Kingdom'),
                                   ('AQ', 'Antarctica')])
    payment_type = SelectField('Payment Type',
                               choices=[('VS', 'Visa'),
                                        ('MC', 'Mastercard'),
                                        ('AM', 'American Express')])


class AddToCart(FlaskForm):
    quantity = IntegerField('Quantity')
    id = HiddenField('ID')
