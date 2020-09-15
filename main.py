from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# SQLite'ı qoşuruq
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Study(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)  # nullable odur ki intro yeri mecbur dolmalidir
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)  # datetime library ile default olaraq indiki zamani gosterecek


    def __repr__(self):
        return '<Study %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")



@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    meqaleler = Study.query.order_by(Study.date.desc()).all() #desc metodu postlari siraliyir
    return render_template("posts.html", meqaleler=meqaleler) #meqaleler=meqaleler yazısını ona görə yazdımki, template'də db-ə məqaleler adınnan müraciət edim


#Meqaleleri id ile siraliyiriq ki her meqalenin oz id si olsun
@app.route('/posts/<int:id>')
def post_detail(id):
    meqale = Study.query.get(id)
    return render_template("post_detail.html", meqale=meqale)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    meqale = Study.query.get_or_404(id)

    try:
        db.session.delete(meqale)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Qeydi silərkən xəta baş verdi"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    #dbden melumatlari götürürük çünki yeni bir məqalə yazmaga ehtiyac yoxdur, olanı dəyişməliyik
        meqale = Study.query.get(id)
        if request.method == 'POST':
            meqale.title = request.form['title']
            meqale.intro = request.form['intro']
            meqale.text = request.form['text']

            # db-nin qoşulub qoşulmadığını yoxlayırıq
            try:

                db.session.commit()  # melumatlari yadda saxlayiriq
                return redirect('/posts')
            except:
                return "Qeyddə dəyişiklik edərkən xəta baş verdi"

        else:
            return render_template("post_update.html", meqale=meqale)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        study = Study(title=title, intro=intro, text=text)

        # db nin qoşulub qoşulmadığını yoxlayırıq
        try:
            db.session.add(study)  # add xususi metoddur ve bizim melumatlari db e elave edir
            db.session.commit()  # melumatlari yadda saxlayiriq
            return redirect('/posts')
        except:
            return "Meqale elave ederken sehvlik yarandi"

    else:
        return render_template("create-article.html")



if __name__ == '__main__':
    app.run(debug=True)
