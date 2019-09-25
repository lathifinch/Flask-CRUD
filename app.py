from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # tell where the db /// for relative path
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        get_note = request.form['content']
        new_note = Todo(content=get_note)

        try:
            db.session.add(new_note)
            db.session.commit()
            return redirect('/')
        except:
            return "ada masalah saat menambah catatan"

    else:
        notes = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', notes=notes)

@app.route('/delete/<int:id>')
def delete(id):
    note_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "ada masalah saat menghapus catatan"

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    note_to_edit = Todo.query.get_or_404(id)

    if request.method == 'POST':
        note_to_edit.content = request.form['content']
        note_to_edit.date_created = datetime.utcnow()

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "ada masalah saat mengedit catatan"

    else:
        return render_template('edit.html', note=note_to_edit)

if __name__ == '__main__':
    app.run(debug=True) # menampilkan error di web
