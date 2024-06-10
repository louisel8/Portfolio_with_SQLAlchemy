from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
db = SQLAlchemy(app)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    date = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    github_link = db.Column(db.String(255), nullable=False)


class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired()])
    date = DateField('Completion Date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    skills = TextAreaField('Skills', validators=[DataRequired()])
    github_link = StringField('GitHub Link', validators=[DataRequired(), URL()])

    def __repr__(self):
        return f'''<Project (Project ID: {self.id}
                            Title: {self.title}
                            Completion Date: {self.strftime('%Y-%m-%d')}
                            Description: {self.description}
                            Skills: {self.skills}
                            Github link: {self.github_link}
'''
