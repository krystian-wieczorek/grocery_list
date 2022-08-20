from flask import Flask, render_template, url_for,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable = False)
    count = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_changed = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Count %r>' % self.id



@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        item_content = request.form['content']
        new_item = Basket(content=item_content)
     
        try:
            if(item_content == ""):
                return "Can't add an empty item"
            else:
                db.session.add(new_item)
                db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"

    else:
        items = Basket.query.order_by(Basket.date_created).all()
        return render_template('index.html', items=items)

@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Basket.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There Was a problem deleting this record'


@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    item = Basket.query.get_or_404(id)
    if request.method == 'POST':
        item.content = request.form['content']
        

        try:
            item.last_changed = datetime.utcnow()
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the record'

    else:
        return render_template('update.html', item=item)


@app.route('/increment/<int:id>', methods=['GET','POST'])
def increment(id):
    item_to_increment = Basket.query.get_or_404(id)
    
    try:
        item_to_increment.count = item_to_increment.count + 1
        item_to_increment.last_changed = datetime.utcnow()
        db.session.commit()
        return redirect('/')
    except:
        return 'The was problem incremanting your item'

@app.route('/decrement/<int:id>', methods=['GET','POST'])
def decrement(id):
    item_to_decrement = Basket.query.get_or_404(id)
    
    try:
        if item_to_decrement.count == 0:
            pass
        else:
            item_to_decrement.count = item_to_decrement.count - 1
        item_to_decrement.last_changed = datetime.utcnow()
        db.session.commit()
        return redirect('/')
    except:
        return 'The was problem incremanting your item'

if __name__ == "__main__":
    app.run(debug=True)