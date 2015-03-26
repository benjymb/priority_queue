from datetime import datetime
import re
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)


class PriorityQueue(db.Model):

    __tablename__ = 'priority_queue'
    id = db.Column('queue_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    priority = db.Column(db.Integer)

    def __init__(self, queue_id, name, priority):
        self.id = queue_id
        self.name = name
        self.priority = priority

    @staticmethod
    def get_queues():
        return PriorityQueue.query.order_by(PriorityQueue.priority.desc()).all()


class Task(db.Model):

    __tablename__ = 'task'
    id = db.Column('task_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    order = db.Column(db.String(100))
    priority = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('priority_queue.queue_id'))
    user = db.relationship(
        "PriorityQueue", backref=db.backref('task', order_by=id)
    )

    def __init__(self, queue_id, name, priority):
        self.id = queue_id
        self.name = name
        self.priority = priority


@app.route('/')
def show_all():
    return render_template('show_all.html', queues=PriorityQueue.get_queues())


# This view method responds to the URL /new for the methods GET and POST
@app.route('/new', methods=['GET', 'POST'])
def new():
    return render_template('show_all.html', queues=PriorityQueue.get_queues())


if __name__ == '__main__':
    db.create_all()
    app.run()
