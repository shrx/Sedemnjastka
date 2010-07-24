from sedemnajstka.tests import *

class TestTopicsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='topics', action='index'))
        # Test response...
