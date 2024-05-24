from flask import Flask, render_template, request, redirect, url_for #url-vygeneruje url redirect-přesměruje na jinou url request-je objekt, který obsahuje všechny informace o aktuálním požadavku
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # Nastavení URI pro SQLite databázi
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Zakázání sledování změn v databázi
db = SQLAlchemy(app)  # Inicializace SQLAlchemy pro manipulaci s databází

class Todo(db.Model):  # Definice modelu pro tabulku Todo
    task_id = db.Column(db.Integer, primary_key=True)  # Primární klíč úkolu
    name = db.Column(db.String(100))  # Název úkolu
    done = db.Column(db.Boolean)  # Stav dokončení úkolu

@app.route('/')  # Definice cesty pro hlavní stránku
def home():
    todo_list = Todo.query.all()  # Načtení všech úkolů z databáze
    return render_template('base.html', todo_list=todo_list)  # Vykreslení šablony s daty o úkolech

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get("name")  # Získání názvu úkolu z formuláře
    new_task = Todo(name=name, done=False)  # Vytvoření nového úkolu
    db.session.add(new_task)  # Přidání úkolu do databáze
    db.session.commit()  # Potvrzení změn v databázi
    return redirect(url_for("home"))  # Přesměrování na hlavní stránku

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.get(todo_id)  # Získání úkolu podle jeho ID
    todo.done = not todo.done  # Změna stavu dokončení úkolu
    db.session.commit()  # Potvrzení změn v databázi
    return redirect(url_for("home"))  # Přesměrování na hlavní stránku

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)  # Získání úkolu podle jeho ID
    db.session.delete(todo)  # Smazání úkolu z databáze
    db.session.commit()  # Potvrzení změn v databázi
    return redirect(url_for("home"))  # Přesměrování na hlavní stránku

if __name__ == '__main__':  # Spuštění aplikace pouze pokud je spuštěna přímo, nikoliv importována jako modul
    app.run()  # Spuštění webového serveru
