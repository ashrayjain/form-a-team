import webapp2
import jinja2
import os
from Db_Schema import *

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                       autoescape=True)
class Handler(webapp2.RequestHandler):
    """Handler Class with Utility functions for Templates"""

    def __write__(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def __render_str__(self, template, **params):
        t = jinja_environment.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.__write__(self.__render_str__(template, **kw))

class MainHandler(Handler):
    def get(self):
        self.render("form-team.html", Event="test")

#class CreateEventHandler(Handler):
#    def post(self):
#        data = self.

app = webapp2.WSGIApplication([
    ('/', MainHandler)
#    ('/ajax/createEvent', CreateEventHandler)
], debug=True)
