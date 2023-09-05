from flask import Blueprint, render_template, request

bp = Blueprint('books', __name__, url_prefix='/books', static_folder='static', template_folder="../templates/books")

@bp.route('/')
def index(request):
  # put in isbn number
  book_data = {
    "authors": []
  }

  isbn_request = requests.get("https://openlibrary.org/isbn/9781442472433", headers={'accept': 'application/json'})
  data = isbn_request.json()
  print(data)
  book_data["title"] = data["title"]
  if "description" in data:
    book_data["description"] = data["description"]

  # Need to add validation if they don't have the key authors, or author and figure out how to get the author
  for author in data["authors"]:
    print("for loop ran")
    authors_request = requests.get(f"https://openlibrary.org{author['key']}", headers={'accept': 'application/json'})
    data = authors_request.json()
    print(data)
    book_data["authors"].append(data["name"])
  

  # then through the data for authors, if no authors look at the works 
    # make a works request, then you can get the author key
      # from author key look up author
    # if author key was in there, then look up the author with the key
  # return object
  # https://openlibrary.org/swagger/docs#/
  print(f"{book_data=}")
  return 'Book found!'

