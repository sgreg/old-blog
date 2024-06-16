import os
from cgi import FieldStorage

from engine import database, util

class Content(object):
    SHOW_LIST  = 1
    SHOW_PAGE  = 2
    SHOW_EMPTY = 3
    SHOW_ERROR = 4

    def __init__(self):
        self.request_uri = os.environ.get("REQUEST_URI")
        self.query_string = os.environ.get("QUERY_STRING")
        self.query_dict = dict()
        self.request_fields = FieldStorage(None, None, [])
        self.request_method = os.environ.get("REQUEST_METHOD")
        self.db = database.database
        self.show = self.SHOW_ERROR
        self.has_pager = False
        self.has_pager_fill_space = False
        self.has_menu = False
        self.has_logo_shown = True
        self.has_subtitle_shown = True
        self.has_footer_shown = True
        self.selected = ""
        self.location_icon = "question-circle"
        self.location = "Unknown"
        self.meta_data = {
            "type": "website",
            "url": util.getCanonical("/"),
            "title": "Sven Gregori - Software by Profession, Electronics by Obsession",
            "image": util.getCanonicalImage("board.png"),
            "description": "A personal blog and project collection about programming, electronics, general tinkering and DIY stuff and some home recording.",
            "page_title": ""
        }

    def set_request_data(self, query_dict, request_fields):
        self.query_dict = query_dict
        self.request_fields = request_fields

    def setup(self):
        return False

    def get_content_type(self):
        return self.show

    def get_page_meta_data(self):
        return self.meta_data

    def get_page_info(self):
        page_info = {
            "location": self.location,
            "location_icon": self.location_icon,
            "selected": self.selected
        }

        return page_info

    def has_logo(self):
        return self.has_logo_shown

    def has_subtitle(self):
        return self.has_subtitle_shown

    def has_footer(self):
        return self.has_footer_shown

    def has_menu_data(self):
        return self.has_menu

    def get_menu_data(self):
        return None

    def has_pager_space(self):
        return self.has_pager_fill_space

    def has_pager_data(self):
        return self.has_pager

    def get_pager_data(self):
        return None

    def get_content_data(self):
        return None

