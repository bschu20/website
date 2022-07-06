
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


#helps Flask find files in our directory
app=Flask(__name__)


#Old db>>
#add a database (SQLite)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///students.db'



#initialize the db; create a variable
db=SQLAlchemy(app) #this is the "Flask(__name__)" from above

#creat model for database
class Students(db.Model):
    #need to specify the datatype
    #primary_key will automatically be assigned since value =True
    id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(200),nullable=False)
    last_name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False, unique=True)
    date_added=db.Column(db.DateTime,default=datetime.utcnow)

#create a string
def __repr__(self):
    return '<first_name %r>' % self.name

app.config['SECRET_KEY']="I'm an old man"


@app.route('/delete/<int:id>')
def delete(id):
    first_name=None
    last_name=None
    form=StudentForm()
    student_to_del=Students.query.get_or_404(id)
    try:
        db.session.delete(student_to_del)
        db.session.commit()
        flash("Student Deleted")
        
        our_students=Students.query.order_by(Students.date_added)
        return render_template('add_student.html', form=form,first_name=first_name, last_name=last_name,our_students=our_students)
    except:
        flash("This didn't work")
        return render_template('add_student.html', form=form,first_name=first_name, last_name=last_name,our_students=our_students)
class ShuForm(FlaskForm): #this will inherit FlaskForm
    #if you don't fill out form, this little validator will throw an error 
    name=StringField("Full Name", validators=[DataRequired()])
    email=StringField("Email Address")
    submit=SubmitField('Submit')# a submit button


#create another form, but this time your form is for the student db
class StudentForm(FlaskForm):
    first_name=StringField("First Name", validators=[DataRequired()])
    last_name=StringField("Last Name", validators=[DataRequired()])
    email=StringField("Email", validators=[DataRequired()])
    submit=SubmitField('Submit')# a submit button

#need a new route and function for our student db
@app.route('/student/add',methods=['GET','POST'])
def add_student():
    first_name=None
    last_name=None
    form=StudentForm()
    if form.validate_on_submit():
        student=Students.query.filter_by(email=form.email.data).first()
        if student is None:
            student=Students(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
            db.session.add(student)
            db.session.commit()
        first_name=form.first_name.data
        last_name=form.last_name.data
        form.first_name.data=''
        form.last_name.data=''
        form.email.data=''
        flash('Submitted')
    our_students=Students.query.order_by(Students.date_added)
    return render_template('add_student.html', form=form,first_name=first_name, last_name=last_name,our_students=our_students)#now we need to create this new html page

@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_error(error):
    return render_template('404.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/student', methods=['GET','POST'])
def student():#takes input from URL and assigns it to 'student_name', which is used inside Jinja2 of student.html
    name=None #this defaults to "none" before anybody passes in a name
    
    form=ShuForm()#this is the form we are passing in 
    if form.validate_on_submit():#if someone submits form, then assign it to "name" variable
        name=form.name.data #assigns input to variable 'name'
        form.name.data='' #this resets the form
        
        flash('Form submitted successfully!')
    return render_template('student.html',name=name,form=form)

