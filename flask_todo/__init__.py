from manager import Manager

from flask import Flask, render_template


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
        man = Manager()
        man.add_item('thing1')
        man.add_item('thing2')

        return render_template('index.html', items=man.item_list)

    return app