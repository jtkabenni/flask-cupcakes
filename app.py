from flask import Flask, render_template, redirect, jsonify, request
from models import Cupcake, db, connect_db


app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "verysecret"
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)

def serialize_cupcake(cupcake):
    """Serialize a dessert SQLAlchemy obj to dictionary."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }


@app.route("/")
def display_cupcakes():
  return render_template("base.html")




@app.route("/api/cupcakes")
def list_all_cupcakes():
  cupcakes = Cupcake.query.all()
  serialized = [ serialize_cupcake(cupcake) for cupcake in cupcakes]

  return jsonify(cupcakes = serialized)

@app.route("/api/cupcakes", methods = ["POST"])
def create_cupcakes():
  # form = AddCupcakeForm()
  cupcake = Cupcake(flavor = request.json["flavor"], size = request.json["size"], rating = request.json["rating"],image = request.json["image"])
  db.session.add(cupcake)
  db.session.commit()
  return (jsonify(cupcake = serialize_cupcake(cupcake)), 201)

@app.route("/api/cupcakes/<int:cupcake_id>")
def list_single_cupcake(cupcake_id):
  cupcake = Cupcake.query.get_or_404(cupcake_id)
  return jsonify(cupcake = serialize_cupcake(cupcake))


@app.route("/api/cupcakes/<int:cupcake_id>", methods = ["PATCH"])
def edit_cupcakes(cupcake_id):
  cupcake = Cupcake.query.get_or_404(cupcake_id)
  cupcake.flavor = request.json["flavor"]
  cupcake.size = request.json["size"]
  cupcake.rating = request.json["rating"]
  cupcake.image=request.json["image"]

  db.session.commit()
  return (jsonify(cupcake = serialize_cupcake(cupcake)))


@app.route("/api/cupcakes/<int:cupcake_id>", methods = ["DELETE"])
def delete_cupcake(cupcake_id):
  cupcake = Cupcake.query.get_or_404(cupcake_id)
  db.session.delete(cupcake)
  db.session.commit()
  return ({"deleted": cupcake_id})


