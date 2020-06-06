import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

database_location = 'sqlite:///' + os.getenv('DATABASE_LOCATION', '') + 'test.db'
port_number = int(os.getenv('FLASK_PORT_NUMBER','5000'))
host_ip_address = os.getenv('FLASK_HOST_IP_ADDRESS', '0.0.0.0')
debug_mode = os.getenv('FLASK_DEBUG_MODE', 'True') == 'True'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_location
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)        

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']  # content is the id fromt he submit on index.html
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error.'    

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks) 

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting ' % id

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content'] 
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating.'
       
    else: # GET
        return render_template('update.html', task=task)

    
def init_dbase():
    location = os.getenv('DATABASE_LOCATION', '') + 'test.db'
    if not os.path.exists(location):
        db.create_all()
        

if __name__ == "__main__":
    init_dbase()
    app.run(host=host_ip_address, port=port_number, debug=debug_mode)
