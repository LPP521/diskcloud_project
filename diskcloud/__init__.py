def create_app(debug=False):
    from flask import Flask

    app = Flask(__name__)

    # @app.before_first_request
    # def check_config():
    #     pass

    #import config from file
    if debug is True:
        app.config.from_pyfile('config/debug_config.py')
    else:
        app.config.from_pyfile('config/production_config.py')

    # add blueprint
    from .blueprint.font_end.bp import font_end
    from .blueprint.back_end.bp import back_end

    app.register_blueprint(font_end, url_prefix='/diskcloud/')
    app.register_blueprint(back_end, url_prefix='/diskcloud/api/')

    # add url route
    # from .views.settings import Settings
    # from .views.about import About
    # app.add_url_rule('/settings','settings',Settings)
    # app.add_url_rule('/about','about',About)

    # add custom command
    import diskcloud.cli

    diskcloud.cli.init_app(app)
    # @click.argument('host','username','password')
    # init_db(host,username,password):

    # register teardown appcontextfunction
    @app.teardown_appcontext
    def teardown_db(self):
        from flask import g

        db = g.pop('db',None)
        if db is not None:
            db.close()

    return app
