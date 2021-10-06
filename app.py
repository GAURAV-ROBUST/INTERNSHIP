from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Product(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    product_name = db.Column(db.String(500), nullable=False)
    from_location = db.Column(db.String(500))
    to_location = db.Column(db.String(500), nullable=False)
    location_id = db.Column(db.Integer)
    movement_id = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.product_id} - {self.product_name}"


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        product_id = request.form['product_id']
        product_name = request.form['product_name']
        location = request.form['location']
        location_id = request.form['location_id']

        product = Product(product_id=product_id,product_name=product_name,to_location=location,location_id=location_id)
        db.session.add(product)
        db.session.commit()
        
    allpro = Product.query.all() 
    return render_template('index.html', allpro=allpro)
    
@app.route('/move/<int:sno>', methods=['GET', 'POST'])
def move(sno):
    if request.method=='POST':
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        location_id = request.form['location_id']
        movement_id = request.form['movement_id']
        pro = Product.query.filter_by(sno=sno).first()
        pro.from_location = from_location
        pro.to_location = to_location
        pro.location_id = location_id
        pro.movement_id = movement_id
        db.session.add(pro)
        db.session.commit()
        return redirect("/")
        
    pro = Product.query.filter_by(sno=sno).first()
    return render_template('move.html', pro=pro)

@app.route('/delete/<int:sno>')
def delete(sno):
    pro = Product.query.filter_by(sno=sno).first()
    db.session.delete(pro)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5000)