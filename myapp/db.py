import sqlite3

import click
from flask import current_app, g #note -current_app-, -g-
from flask.cli import with_appcontext


def get_db():
    """
    Connect to the application's configured database. The connection is unique for each 
    request and will be reused if this is called again.
    """
    if 'db' not in g:
        g.db = sqlite3.connect( #note -sqlite3.connect-
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row #note -sqlite3.Row-

    return g.db


def close_db(e=None): #note -close_db-
    """If this request connected to the database, close the connection."""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f: #note -open_sources-
        db.executescript(f.read().decode('utf8'))


@click.command('init-db') #note -click.command()-
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Register database functions with the Flask app. This is called by the application factory."""
    app.teardown_appcontext(close_db) #note -app.teardown_appcontext()-
    app.cli.add_command(init_db_command) #note -app.cli.add_command()-


"""
Note:

-current_app-
current_app is another special object that points to the Flask application handling the request. 
Since you used an application factory, there is no application object when writing the rest of 
your code. get_db will be called when the application has been created and is handling a request, 
so current_app can be used.


-g-
g is a special object that is unique for each request. It is used to store data that might be 
accessed by multiple functions during the request. The connection is stored and reused instead 
of creating a new connection if get_db is called a second time in the same request.


-sqlite3.connect()-
sqlite3.connect() establishes a connection to the file pointed at by the DATABASE configuration key. 
This file doesn’t have to exist yet, and won’t until you initialize the database later.


-sqlite3.Row-
sqlite3.Row tells the connection to return rows that behave like dicts. This allows accessing the 
columns by name.


-close_db-
close_db checks if a connection was created by checking if g.db was set. If the connection exists, 
it is closed. Further down you will tell your application about the close_db function in the 
application factory so that it is called after each request.


-open_resource()-
open_resource() opens a file relative to the myapp package, which is useful since you won’t 
necessarily know where that location is when deploying the application later. get_db returns a 
database connection, which is used to execute the commands read from the file.


-click.command()-
click.command() defines a command line command called init-db that calls the init_db function and 
shows a success message to the user. You can read Command Line Interface to learn more about writing 
commands.


-app.teardown_appcontext()-
app.teardown_appcontext() tells Flask to call that function when cleaning up after returning 
the response.


-app.cli.add_command()-
app.cli.add_command() adds a new command that can be called with the flask command.
"""