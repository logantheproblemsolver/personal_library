from flask import Blueprint, render_template, request
import mokkari
from personal_library import db
import os

bp = Blueprint('comics', __name__, url_prefix='/comics', static_folder='static', template_folder="../templates/comics/")

@bp.route('/')
def index():
  m = mokkari.api(os.environ.get('MOKKARI_USERNAME'), os.environ.get('MOKKARI_PASSWORD'))
  comics = []
  # Get all Marvel comics for the week of 2021-06-07
  this_week = m.issues_list({"upc": 76194137882400111})
  print(f"{this_week=}")
  print(bool(this_week))
  for i in this_week:
      print(f"{i.id} {i.issue_name}")
      issue = m.issue(i.id)
      print(f"{issue.image=}")
      comics.append({
          "title": issue.series.name,
          "series_place": issue.series.volume,
          "image": issue.image,
          "desc": issue.desc
      })
  print(f"{comics=}")
  return "Comic found!"


@bp.route('/lookup', methods=('GET', 'POST'))
def lookup():
    if request.method == 'POST':
        print(f"{request.form['isbn']}")
        isbn = request.form['isbn']
        m = mokkari.api('mrloganellis', 'Vf3#Ay*khN$Rhtk6')
        comics = []
        this_week = m.issues_list({"upc": isbn})
        print(f"{this_week=}")
        for i in this_week:
            print("for loop ran")
            current_comic = m.issue(_id=i.id)
            print(f"{current_comic.series.name=}")
            print(f"{current_comic.variants}")
            for variant in current_comic.variants:
                print(f"{variant.name}")
                print(f"{variant.image}")
            try:
                current_arc = m.arc(_id=i.id)
                print(f"{current_arc.name=}")
            except:
                print("no arc found")
            
            comics.append({
                "title": current_comic.series.name,
                "series_place": current_comic.series.volume,
                "image": current_comic.image,
                "desc": current_comic.desc,
                "volume": current_comic.series.volume,
                "owned": False,
                "variants": current_comic.variants,
            })
            # print(f"{i.id} {i.issue_name}")
            # issue = m.issue(i.id)
            # print(f"{issue.image=}")
            # comics.append({
            #     "title": issue.series.name,
            #     "series_place": issue.series.volume,
            #     "image": issue.image,
            #     "desc": issue.desc
            # })
        print(f"{comics=}")
        return render_template('lookup.html', comics=comics, comics_length=len(comics))
    else:
      return render_template('lookup.html')
    


@bp.route('/lookup/add', methods=['POST'])
def add():
    if request.method != 'POST':
        return "no"
    data = request.get_json()
    print(f"{data['title']=}")
    cursor = db.cursor()
    insert_query = ''' INSERT INTO comics (title, series_number, "desc", image, volume) VALUES (%s, %s, %s, %s, %s); '''
    try:
        cursor.execute(insert_query, (data["title"], data["series_number"], data["desc"], data["image"], data["volume"]))
        db.commit()
    except Exception as e:
        print("Error executing the command:", e)
    return { 'message': "that worked!" }

@bp.route('/library', methods=['GET'])
def view_comics():
    cursor = db.cursor()
    select_query = ''' SELECT * from comics '''
    try:
        cursor.execute(select_query)
        comics_results = cursor.fetchall()
    except Exception as e:
        print("Error executing the command:", e)
    print(f"{comics_results=}")
    return render_template('library.html', comics=comics_results)