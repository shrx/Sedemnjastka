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

    # auth
    map.connect('login', '/login', controller='auth', action='login')
    map.connect('logout', '/logout', controller='auth', action='logout')

    # archive
    map.connect('/', controller='archive', action='index')
    map.connect('/archive', controller='archive', action='index')
    map.connect('/archive/{page:\d+}', controller='archive', action='index')

    # topics
    map.connect('topic', '/topics/{id:\d+}', controller='topics', action='show')
    map.connect('/topics/{id:\d+}/{page:\d+}', controller='topics', action='show')

    # users
    map.connect('/users', controller='users', action='index')
    map.connect('/users.json', controller='users', action='index', content_type='application/json')
    map.connect('user', '/users/{id:\d+}', controller='users', action='show')

    map.connect('user_avatars', '/users/{id:\d+}/avatars', controller='users', action='avatars')

    map.connect('user_posts', '/users/{id:\d+}/posts', controller='users', action='posts')
    map.connect('/users/{id:\d+}/posts/{page:\d+}', controller='users', action='posts')

    map.connect('user_topics', '/users/{id:\d+}/topics', controller='users', action='topics')
    map.connect('/users/{id:\d+}/topics/{page:\d+}', controller='users', action='topics')

    map.connect('user_edit', '/users/edit', controller='users', action='edit')

    map.connect('claim', '/users/{id:\d+}/claim', controller='users', action='claim')
    map.connect('passwd', '/users/passwd/{token}', controller='users', action='passwd')

    map.connect('user_chart_1', '/users/{id:\d+}/charts/{type}', controller='users', action='charts')
    map.connect('user_chart_2', '/users/{id:\d+}/charts/{type}/limit/{limit:\d+}', controller='users', action='charts')
    map.connect('user_chart_3', '/users/{id:\d+}/charts/{type}/start/{start}/end/{end}', controller='users', action='charts')

    # rankings
    map.connect('/rankings', controller='rankings', action='index')

    # info
    map.connect('/info', controller='info', action='index')

    # quotes
    map.connect('/quotes', controller='quotes', action='create', conditions=dict(method=['PUT']))
    map.connect('quote', '/quotes/{id:\d+}', controller='quotes', action='show')
    map.connect('quote_post', '/quotes/new/{post:\d+}', controller='quotes', action='new')
    map.connect('quotes', '/quotes', controller='quotes', action='index', conditions=dict(method=['GET']))

    map.connect('quote_upvote', '/quotes/{id:\d+}/vote/up', controller='quotes', action='vote', way='up')
    map.connect('quote_downvote', '/quotes/{id:\d+}/vote/down', controller='quotes', action='vote', way='down')

    # search
    map.connect('search', '/search', controller='search', action='index')

    # collage
    map.connect('/collage', controller='collage', action='index')

    # games
    map.connect('/games', controller='games', action='index')

    map.connect('/games/guess-avatar', controller='guess_avatar', action='index')
    map.connect('/games/guess-avatar/guessed', controller='guess_avatar', action='guessed')

    return map
