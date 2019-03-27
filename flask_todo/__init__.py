# from . import manager
import psycopg2
import datetime

from flask import Flask, request, render_template

# man = manager.Manager()
# man.add_item('thing1')
# man.add_item('thing2')
connection = psycopg2.connect("dbname=todo host=localhost")
manager = connection.cursor()

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)

    else:
        app.config.from_mapping(test_config)

    @app.route('/')
    def index():
        manager.execute("SELECT * FROM items;")

        return render_template('index.html', items=manager.fetchall())
    
    @app.route('/create', methods=['GET', 'POST'])
    def create():
        if request.method == 'GET':
            return render_template('create.html', task=None)
        
        elif request.method == 'POST':
            task = request.form['task']

            manager.execute("""
            INSERT INTO items (task, completed, date_created)
            VALUES (%s, False, %s);
            """,
            (task, datetime.datetime.now())
            )

            connection.commit()

            return render_template('create.html', task=task)
    
    @app.route('/update')
    def update():
        pass

    return app