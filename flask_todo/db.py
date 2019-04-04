import os
import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        DB_URL = os.environ.get('DATABASE_URL', None)

        if DB_URL:
            g.db = psycopg2.connect(DB_URL, sslmode='require')
        # g sets up a connection to the database
        else:
            g.db = psycopg2.connect(
                f"dbname={current_app.config['DB_NAME']}" +
                f" user={current_app.config['DB_USER']}"
            )

    return g.db

# closes the connection to the database
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# creates the database
def init_db():
    db = get_db()

    # sql file to point towards
    with current_app.open_resource('schema.sql') as f:
        cur = db.cursor()
        cur.execute(f.read())
        cur.close()
        db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    print('\n--------------')
    print('\nrunning init app\n')
    print('--------------\n')
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)