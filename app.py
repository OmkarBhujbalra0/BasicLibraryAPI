# Importing Required Libraries
import os
from flask import Flask,request,render_template,jsonify
from flask_sqlalchemy import SQLAlchemy

# Initializing Flask

app = Flask(__name__)

# Creating SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydtb.db"

db = SQLAlchemy(app)

class BookStore(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    author = db.Column(db.String(50),nullable=False)
    year = db.Column(db.Integer,nullable=False)

# Route to get all the data
@app.route("/books",methods=["GET"])
def getbooks():
        books = BookStore.query.all()
        # Will return all the books available in the database
        return jsonify([{"id":book.id,"title":book.title,"author":book.author,"year":book.year} for book in books])

# Route to add books in Database
@app.route("/books",methods=["POST"])
def post_books():
    data = request.json
    new_book = BookStore(title=data["title"],author=data["author"],year=data["year"])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message":"Book added successfully!"}),201

# Route to get specific book
@app.route("/book/<int:id>",methods=["GET"])
def get_single_book(id):
    book = BookStore.query.get(id)
    if book:
         return jsonify({"Id":book.id,"Title":book.title,"Author":book.author,"Year":book.year})
    return jsonify({"error":"Book not Found"}),404

# Route to update specific book
@app.route("/book/<int:id>",methods=["PUT"])
def update_book(id):
     book = BookStore.query.get(id)
     if book:
          data = request.json
          book.title = data["title"]
          book.author = data["author"]
          book.year = data["year"]
          db.session.commit()
          return jsonify({"message":"Book Updated Successfully"})
     return jsonify({"error":"Book not Found"}),404

# Route to delete specific book
@app.route("/book/<int:id>",methods=["DELETE"])
def delete_book(id):
     book = BookStore.query.get(id)
     if book:
          db.session.delete(book)
          db.session.commit()
          return jsonify({"message":"Book Deleted Successfully"})
     return jsonify({"error":"Book Not Found"}),404
 
with app.app_context():
    db.create_all()

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port)