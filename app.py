from flask import Flask,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #IMP
db = SQLAlchemy(app) 

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id
    

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'] # Form input Name tag
        new_task = Todo(content = task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/") 
        except:
            return "Error creating new task."
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks = tasks) # IMP


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) # IMP 
# When you use Todo.query, it creates a query object for the Todo model, 
# which allows you to perform queries on the todos table.
    
    try:
        db.session.delete(task_to_delete)
        # db is an instance of SQLAlchemy, which is used to manage the connection and interaction with 
        # the database. However, to perform queries on the Todo model, 
        # we need to use the query method of the Todo model.
        db.session.commit()
        return redirect("/")
    except:
        return "Error Deleting Task"

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Error Updating Task"
        
    else:
        return render_template('update.html',task = task)
    


if __name__ ==  '__main__':
    app.run(debug=True)
    
# From Shell
# from app import db,app
# app.app_context().push()
# db_create_all()    


