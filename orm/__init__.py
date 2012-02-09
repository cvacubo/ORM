from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from orm.models import initialize_sql

def main(global_config, **settings): # pragma: no cover
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'orm:static', cache_max_age=3600)

    config.add_route('home', '/main')
    config.add_view('orm.views.my_view',
                    route_name='home',
                    renderer='templates/mytemplate.pt')


    config.add_route('relations', '/test')
    config.add_view('orm.views.view_relations', route_name='relations', renderer='templates/view_template.pt')

    config.add_route('all_parents', '/parents')
    config.add_view('orm.views.view_all_parents', route_name='all_parents', request_method='GET', renderer='string')

    config.add_route('balance', '/balance')
    config.add_view('orm.views.view_balance', route_name='balance', request_method='GET', renderer='string')

    return config.make_wsgi_app()

