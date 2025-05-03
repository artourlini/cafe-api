from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

app = Flask(__name__)


class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/", methods=['GET'])
def home():
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars()
    cafe_list = []

    for cafe in cafes:
        cafe_list.append(
            {
                "id": cafe.id,
                "name": cafe.name,
                "map_url": cafe.map_url,
                "img_url": cafe.img_url,
                "location": cafe.location,
                "seats": cafe.seats,
                "has_toilet": cafe.has_toilet,
                "has_wifi": cafe.has_toilet,
                "has_sockets": cafe.has_sockets,
                "can_take_calls": cafe.can_take_calls,
                "coffee_price": cafe.coffee_price
            }
        )

    return render_template("index.html", cafes=cafe_list)

@app.route("/random", methods=['GET'])
def random():
    #will display all info of one random cafe
    random_cafe = db.session.execute(db.select(Cafe).order_by(db.sql.func.random()).limit(1)).scalar()

    return jsonify(
        cafe={
            "id": random_cafe.id,
            "name": random_cafe.name,
            "map_url": random_cafe.map_url,
            "img_url": random_cafe.img_url,
            "location": random_cafe.location,
            "seats": random_cafe.seats,
            "has_toilet": random_cafe.has_toilet,
            "has_wifi": random_cafe.has_toilet,
            "has_sockets": random_cafe.has_sockets,
            "can_take_calls": random_cafe.can_take_calls,
            "coffee_price": random_cafe.coffee_price
        }
    )

@app.route("/all", methods=['GET'])
def all():
    #displays the cafe api
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.id)).scalars()
    cafe_list = []

    for cafe in cafes:
        cafe_list.append(
            {
                "id": cafe.id,
                "name": cafe.name,
                "map_url": cafe.map_url,
                "img_url": cafe.img_url,
                "location": cafe.location,
                "seats": cafe.seats,
                "has_toilet": cafe.has_toilet,
                "has_wifi": cafe.has_toilet,
                "has_sockets": cafe.has_sockets,
                "can_take_calls": cafe.can_take_calls,
                "coffee_price": cafe.coffee_price
            }
        )

    return jsonify(cafe=cafe_list)

@app.route("/search", methods=['GET'])
def search():
    #search the api for cafes in the same location ex. http://127.0.0.1:5000/search?loc=Peckham
    cafes_loc =request.args.get("loc")
    cafe_list = []

    if cafes_loc:
        cafes = db.session.execute(db.select(Cafe).where(Cafe.location == cafes_loc.title())).scalars()

        for cafe in cafes:
            cafe_list.append(
                {
                    "id": cafe.id,
                    "name": cafe.name,
                    "map_url": cafe.map_url,
                    "img_url": cafe.img_url,
                    "location": cafe.location,
                    "seats": cafe.seats,
                    "has_toilet": cafe.has_toilet,
                    "has_wifi": cafe.has_toilet,
                    "has_sockets": cafe.has_sockets,
                    "can_take_calls": cafe.can_take_calls,
                    "coffee_price": cafe.coffee_price
                }
            )

        return jsonify(cafe=cafe_list)

    else:
        return jsonify(error={"Not Found": "We don't have that cafe in that location"})

if __name__ == '__main__':
    app.run()
