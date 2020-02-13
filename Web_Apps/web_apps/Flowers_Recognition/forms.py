#Flask forms & validators
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import  SubmitField


class uploadRecogIm(FlaskForm):
    file = FileField("Upload a FLower Image")
    submit = SubmitField("Run the recognition")




