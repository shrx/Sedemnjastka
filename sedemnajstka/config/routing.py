"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    # archive
    map.connect('/', controller='archive', action='index')
    map.connect('/archive', controller='archive', action='index')
    map.connect('/archive/{page:\d+}', controller='archive', action='index')

    # topics
    map.connect('topic', '/topics/{id:\d+}')

    # users
    map.connect('/users', controller='users', action='index')
    map.connect('user', '/users/{id:\d+}', controller='users', action='show')

    return map
