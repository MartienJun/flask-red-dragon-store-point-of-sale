import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'red-dragon-store.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # register the database commands
    from . import db
    db.init_app(app)

    # register the auth blueprints to the app
    from . import auth
    app.register_blueprint(auth.bp)

    from . import purchase
    app.register_blueprint(purchase.bp)
    app.add_url_rule('/', endpoint='index')

    from . import product
    app.register_blueprint(product.bp)

    from . import user
    app.register_blueprint(user.bp)

    return app