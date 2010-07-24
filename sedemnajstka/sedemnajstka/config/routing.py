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
    map.connect('topic', '/topics/{id:\d+}', controller='topics', action='show')
    map.connect('/topics/{id:\d+}/{page:\d+}', controller='topics', action='show')

    # users
    map.connect('/users', controller='users', action='index')
    map.connect('user', '/users/{id:\d+}', controller='users', action='show')

    map.connect('user_posts', '/users/{id:\d+}/posts', controller='users', action='posts')
    map.connect('/users/{id:\d+}/posts/{page:\d+}', controller='users', action='posts')

    map.connect('user_topics', '/users/{id:\d+}/topics', controller='users', action='topics')
    map.connect('/users/{id:\d+}/topics/{page:\d+}', controller='users', action='topics')

    return map
