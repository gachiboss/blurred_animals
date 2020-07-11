from flask import Flask, render_template, redirect
from PIL import Image, ImageFilter, UnidentifiedImageError
import requests
import config
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
db = SQLAlchemy(app)


class Events(db.Model):
    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    animal_type = db.Column(db.String, nullable=False)
    processed_image = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow().replace(microsecond=0))


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/cat')
def cat():
    response = requests.get(config.cat_url, stream=True).raw
    try:
        img_cat = Image.open(response).filter(ImageFilter.SHARPEN)
    except UnidentifiedImageError:
        return render_template("error.html")
    uuid = uuid4()
    imgname = config.basedir+'\\static\\downloads\\'+str(uuid)+'.jpeg'
    img_cat.save(imgname)
    event = Events(animal_type='Cat', processed_image=str(uuid)+'.jpeg')
    db.session.add(event)
    db.session.commit()
    return render_template("cat.html", uuid=str(uuid)+'.jpeg')


@app.route('/dog')
def dog():
    resp = str(requests.get(config.dog_url, stream=True).content)[4:-3]
    response = requests.get(resp, stream=True).raw
    try:
        img_dog = Image.open(response).filter(ImageFilter.SHARPEN)
    except UnidentifiedImageError:
        return render_template("error.html")
    uuid = uuid4()
    imgname = config.basedir+'\\static\\downloads\\'+str(uuid)+'.jpeg'
    img_dog.save(imgname)
    event = Events(animal_type='Dog', processed_image=str(uuid)+'.jpeg')
    db.session.add(event)
    db.session.commit()
    return render_template("dog.html", uuid=str(uuid)+'.jpeg')


@app.route('/fox')
def fox():
    response = requests.get(config.fox_url, stream=True).raw
    try:
        img_fox = Image.open(response).filter(ImageFilter.SHARPEN)
    except UnidentifiedImageError:
        return render_template("error.html")
    uuid = uuid4()
    imgname = config.basedir+'\\static\\downloads\\'+str(uuid)+'.jpeg'
    img_fox.save(imgname)
    event = Events(animal_type='Fox', processed_image=str(uuid)+'.jpeg')
    db.session.add(event)
    db.session.commit()
    return render_template("fox.html", uuid=str(uuid)+'.jpeg')

@app.route('/history')
def table():
    event = Events.query.order_by(Events.ID).all()
    return render_template("history.html", event=event)

@app.route('/history/static/<uuid>')
def show_img(uuid):
    return render_template('view.html', uuid=str(uuid)+'.jpeg')


def get_cat_url(kitty_url):
    url = str(requests.get(kitty_url, stream=True).content)[11:-3:]
    kitty_url = url.replace('\\', '')
    return kitty_url



if __name__ == "__main__":
    app.run(debug=True)
