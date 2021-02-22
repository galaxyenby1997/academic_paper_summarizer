from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class InputData(FlaskForm):
	url_link = StringField('HTML page', validators=[DataRequired()])
	word_count = IntegerField('Word Count', validators=[DataRequired()])
	#keyword_percentage = IntegerField('Keyword %', validators=[DataRequired()])

	submit = SubmitField('Summarize')