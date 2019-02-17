from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DecimalField,
DecimalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo,
Length, NumberRange
from app.models import Counter, Unit, Client, User

class AddUnitForm(FlaskForm):
    sn = StringField('Serial number', validators=[DataRequired()])
    vendor = StringField('Vendor', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    black_counter = DecimalField('Black counter',
                                validators=[NumberRange(min=0)])
    color_counter = DecimalField('Color counter',
                                validators=[NumberRange(min=0)])

    submit = SubmitField('Submit')

    def validate_sn(self, sn):
        serialno = Unit.query.filter_by(sn=sn.data).first()
        if serialno is not None:
            raise ValidationError('Serial number already exists.')

class EditUnitForm(FlaskForm):
    sn = StringField('Serial number', validators=[DataRequired()])
    vendor = StringField('Vendor', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    client_id = DecimalField('Client') # scrollable, dynamic
    black_counter = DecimalField('Black counter',
                                validators=[NumberRange(min=0)])
    color_counter = DecimalField('Color counter',
                                validators=[NumberRange(min=0)])

    submit = SubmitField('Submit')

    def __init__(self, original_sn, *args, **kwargs):
        super(EditUnitForm, self).__init__(*args, **kwargs)
        self.original_sn = orignal_sn

    def validate_sn(self, sn):
        if sn.data != self.orignal_sn:
            sn = Unit.query.filter_by(sn=self.sn.data).first()
            if sn is not None:
                raise ValidationError('Cannot have duplicate serial numbers.')

class AddClientForm(FlaskForm):
    company_name = StringField('Company name', validators=[DataRequired()])
    black_rate = DecimalField('Black rate', validators=[DataRequired(),
                                NumberRange(min=0)])
    color_rate = DecimalField('Color rate', validators=[DataRequired(),
                                NumberRange(min=0)])
    min_monthly_pay = DecimalField('Minimum monthly pay',
                                validators=[DataRequired(), NumberRange(min=0)])
    address = StringField('Address', validators=[Length(max=128)])
    email = StringField('Email address', validators=[Email()])
    phone = StringField('Phone number', validators =[Length(max=64)])
    notes = TextAreaField('Notes', validators=[Length(max=256)])

    submit = SubmitField('Submit')

    def validate_company_name(self, company_name):
        company = Client.query.filter_by(company_name=company_name.data).first()
        if company is not None:
            raise ValidationError(
                                f'Company {company_name.data} already exists.')

class EditClientForm(FlaskForm):
    company_name = StringField('Company name', validators=[DataRequired()])
    black_rate = DecimalField('Black rate', validators=[DataRequired(),
                                NumberRange(min=0)])
    color_rate = DecimalField('Color rate', validators=[DataRequired(),
                                NumberRange(min=0)])
    min_monthly_pay = DecimalField('Minimum monthly pay',
                                validators=[DataRequired(), NumberRange(min=0)])
    address = StringField('Address', validators=[Length(max=128)])
    email = StringField('Email address', validators=[Email()])
    phone = StringField('Phone number', validators =[Length(max=64)])
    notes = TextAreaField('Notes', validators=[Length(max=256)])

    submit = SubmitField('Submit')
