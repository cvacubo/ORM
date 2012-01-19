from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from orm.models import initialize_sql

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'orm:static', cache_max_age=3600)

    #config.add_route('home', '/')
    #config.add_view('orm.views.my_view',
    #                route_name='home',
    #                renderer='templates/mytemplate.pt')


    config.add_route('relations', '/test')
    config.add_view('orm.views.view_relations', route_name='relations', renderer='templates/view_template.pt')

    return config.make_wsgi_app()

