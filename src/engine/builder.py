import os
import cgi

import template
import database
from content.index import IndexPage
from content.static import StaticPage
from content.error import ErrorPage
from content.blog import BlogPage
from content.projects import ProjectPage

class PageBuilder(object):
    DEBUG = False
    valid_categories = [
            "index",
            "blog",
            "projects",
            "static"
    ]

    valid_request = False
    valid_subrequest = False

    def __init__(self):
        query_string = os.environ.get("QUERY_STRING")
        redir_url = os.environ.get("REDIRECT_URL")
        method = os.environ.get("REQUEST_METHOD")

        # query string sanitazion
        if query_string is None or "=" not in query_string:
            query_string = 'page=index'

        self.query_string = query_string
        self.request = cgi.FieldStorage(keep_blank_values=True)
        self.query = dict(f.split('=') for f in query_string.split('&'))
        self.page = "index"


    def build(self):
        self.sanitize_request()
        self.validate_query_string()
        try:
            database.initialize()
        except:
            self.send_header()
            print("We are experiencing technical difficulties. oh oh..")
            return
        self.assign_content()
        self.setup_content()
        self.send_header()
        self.display_content()

    def sanitize_request(self):
        # TODO ..if needed? for POST requests maybe, but probably at some other place then
        pass

    def is_query_string_valid(self):
        if self.query is None:
            return False

        if not self.query.has_key('page'):
            return False

        if self.query['page'] not in self.valid_categories:
            return False

        if self.query['page'] == "error":
            return False

        return True

    def validate_query_string(self):
        self.valid_request = self.is_query_string_valid()
        if self.valid_request:
            self.page = self.query["page"]
        else:
            self.page = "error"

    def assign_content(self):
        if self.page == "index":
            self.content = IndexPage()
        elif self.page == "blog":
            self.content = BlogPage()
        elif self.page == "projects":
            self.content = ProjectPage()
        elif self.page == "static":
            self.content = StaticPage()
        elif self.page == "error":
            self.content = ErrorPage()
        else:
            self.content = IndexPage() # or what else? Error? MissingPage()? shouldn't happen..

    def setup_content(self):
        self.content.set_request_data(self.query, self.request)
        self.valid_subrequest = self.content.setup()
        self.template_handler = template.TemplateHandler(self.content)

    def send_header(self):
        if self.valid_request and self.valid_subrequest:
            print("Status: 200 OK")
        elif isinstance(self.content, ErrorPage):
            print("Status: " + self.content.getError())
        else:
            print("Status: 404 Not Found")

        print("Content-type: text/html")
        print("")

    def display_debug(self):
        print("<!--")
        print("valid: " + str(self.valid_request))
        print(self.query)
        print(os.environ)
        print("query string: " +self.query_string)
        print("-->")

    def display_content(self):
        if self.DEBUG:
            self.display_debug()

        self.template_handler.build_page()

