# Flaski qowuruq, 2ci import bizim html kodlarimizi bura qowur
from flask import Flask, render_template, url_for, request, redirect
# SQL lite i import edirik
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# burada sag terefde hansi sql ile ve table in adini yaziriq
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Study(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id reqem ile yazilir ve primary key i var
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)  # nullable odur ki intro yeri mecbur dolmalidir
    text = db.Column(db.Text, nullable=False)  # text geniw cumleler ucun istifade olunur
    date = db.Column(db.DateTime, default=datetime.utcnow)  # datetime library ile default olaraq indiki zamani gosterecek

    # Bu yazi ile biz onu edirikki, biz obyekti cixiwa verende onun id si ile cixiwa vereceyik
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
    # bu yazi bizim db mizdeki 1ci meqaleni 'meqaleye' elave edir - all yazsaq hamsi elave olunacaq
    meqaleler = Study.query.order_by(Study.date.desc()).all() #desc metodu postlari siraliyir
    return render_template("posts.html", meqaleler=meqaleler) #biz burda meqalemizi meqaleye menimsetdikki htmlde meqale adi ile muraciet edek


#Meqaleleri id ile siraliyiriq ki her meqalenin oz id si olsun
@app.route('/posts/<int:id>')
def post_detail(id):
    meqale = Study.query.get(id)
    return render_template("post_detail.html", meqale=meqale)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    meqale = Study.query.get_or_404(id) #bu ona gore lazimdiki dbde meqale tapilmasa 404 vursun

    try:
        db.session.delete(meqale)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Meqaleni silerken xeta bash verdi"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])  # alinan melumatlari get yadaki post yolu ile qowdugumuzu yoxlayiriq
def post_update(id):
    #dbden melumatlari gotururk cunki yeni bir meqale yazmaga ehtiyac yoxdu olani deyiwmeliyik
        meqale = Study.query.get(id)
        if request.method == 'POST':
            meqale.title = request.form['title']  # create-articledaki titleni bura qowuruq
            meqale.intro = request.form['intro']
            meqale.text = request.form['text']

            # db nin qowulub qowulmadigini yoxlayiriq
            try:

                db.session.commit()  # melumatlari yadda saxlayiriq
                return redirect('/posts')
            except:
                return "Meqale deyiwikliyi edende sehvlik yarandi"

        else:
            return render_template("post_update.html", meqale=meqale)


@app.route('/create-article', methods=['POST', 'GET'])  # alinan melumatlari get yadaki post yolu ile qowdugumuzu yoxlayiriq
def create_article():
    if request.method == 'POST':
        title = request.form['title']  # create-artocledaki titleni bura qowuruq
        intro = request.form['intro']
        text = request.form['text']

        study = Study(title=title, intro=intro, text=text)

        # db nin qowulub qowulmadigini yoxlayiriq
        try:
            db.session.add(study)  # add xususi metoddur ve bizim melumatlari db e elave edir
            db.session.commit()  # melumatlari yadda saxlayiriq
            return redirect('/posts')
        except:
            return "Meqale elave ederken sehvlik yarandi"

    else:
        return render_template("create-article.html")


# bu scriptnen gosteririkki esas yer buradi
if __name__ == '__main__':
    app.run(debug=True)
