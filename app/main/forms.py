class EditProfileForm(Form):
	name = StringField('Real name', validators=[length(0,64)])
	location = StringField('Location', validators=[length(0,64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')

class EditProfileAdminForm(Form):
	"""docstring for EditProfileAdminForm"""
	email = StringField('Email', validators=[Required(), Length(1,64),Email()])
	username = StringField('Username', validators=[Required(),Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'usernames must have only letters, numbers, dots or underscores')])
	confirm = BooleanField('Confirmed') 
	role = SelectField('Role', coerce=int)
	name = StringField('Real name', validators=[length(0,64)])
	location = StringField('Location', validators=[length(0,64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')

	def __init__(self, user, *arg, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		self.role = choices=[(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_email(self, field):
		if field.data != self.user.email and \
		        User.query.filter_by(email=field.data).first():
		    raise ValidationError('Email already registered.')
			
    def validate_username(self, field):
    	if field.data != self.user.username and \
    	        User.query.filter_by(username=field.data).first():
    	    raise ValidationError('Username already in use.')
		
class PostForm(Form):
	body = TextAreaField("what do you want to say", validators=[Required()])
	submit = SubmitField('submit')
	