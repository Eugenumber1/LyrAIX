from flask import Flask, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/') # url for my app
def index():
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)


    """
    <div class="content">
    <h1>Task Manager</h1>
    <table>
        <tr>
            <th>Task</th>
            <th>Added</th>
            <th>Actions</th>
        </tr>
    </table>
</div>"""