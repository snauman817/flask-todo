import datetime

from flask import Flask, request, render_template


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        # flask itself has a user for the database
        DB_NAME='todo',
        DB_USER='flasktodo_user',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)

    else:
        app.config.from_mapping(test_config)

    from . import db
    db.init_app(app)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        
        if request.method == 'GET':
            con = db.get_db()
            cur = con.cursor()

            cur.execute("SELECT * FROM items;")

            todo_results = cur.fetchall()
            cur.close()

            return render_template('index.html', items=todo_results, action="All")
        
        elif request.method == 'POST':
            action = request.form['action']

            con = db.get_db()
            cur = con.cursor()

            if action == 'All':
                cur.execute("SELECT * FROM items;")

                todo_results = cur.fetchall()
                cur.close()

                return render_template('index.html', items=todo_results, action="All")

            elif action == 'Completed':
                cur.execute("SELECT * FROM items WHERE completed = True;")

                todo_results = cur.fetchall()
                cur.close()

                return render_template('index.html', items=todo_results, action="Completed")

            elif action == 'Uncompleted':
                cur.execute("SELECT * FROM items WHERE completed = False;")

                todo_results = cur.fetchall()
                cur.close()

                return render_template('index.html', items=todo_results, action="Uncompleted")
            
    
    @app.route('/create', methods=['GET', 'POST'])
    def create():
        if request.method == 'GET':
            return render_template('create.html', task=None)
        
        elif request.method == 'POST':
            task = request.form['task']

            con = db.get_db()
            cur = con.cursor()

            cur.execute("""
                INSERT INTO items (task, completed, date_created)
                VALUES (%s, False, %s);
                """,
                (task, datetime.datetime.now())
            )

            con.commit()
            cur.close()

            return render_template('create.html', task=task)
    
    @app.route('/update', methods=['GET', 'POST'])
    def update():
        if request.method == 'GET':
            con = db.get_db()
            cur = con.cursor()

            cur.execute("SELECT * FROM items WHERE completed = False;")

            items = cur.fetchall()

            cur.close()

            return render_template('update.html', items=items)
        
        if request.method == 'POST':
            con = db.get_db()
            cur = con.cursor()

            item_id = request.form['task']

            cur.execute("""
                UPDATE items
                SET completed = True
                WHERE id = %s;
                """,
                (item_id)
            )

            con.commit()

            cur.execute("SELECT * FROM items WHERE completed = False;")
            items = cur.fetchall()

            cur.close()

            return render_template('update.html', items=items)

    return app