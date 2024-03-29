"""The base Controller API

Provides the BaseController class for subclassing.
"""
from datetime import datetime, timedelta

from pylons import session, request, url, tmpl_context as c
from pylons.controllers import WSGIController
from pylons.controllers.util import redirect
from pylons.templating import render_mako as render

from sedemnajstka.model.meta import Session
from sedemnajstka.model import Info

class BaseController(WSGIController):

    requires_auth = []

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()

    def __before__(self, action):
        if action in self.requires_auth:
            if 'user' not in session:
                session['return_to'] = request.path_info
                session.save()
                redirect(url('login'))

        last_run = Session.query(Info). \
            filter(Info.attribute=='archive_last_run'). \
            first()
        c.archive_age = datetime.now() - datetime. \
            strptime(last_run.value, '%Y-%m-%d %H:%M:%S')
        c.next_run = timedelta(minutes=17) - c.archive_age
