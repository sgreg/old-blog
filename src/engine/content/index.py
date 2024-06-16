from content import Content
from engine import config

class IndexPage(Content):
    def setup(self):
        self.has_pager = False
        self.has_pager_fill_space = False
        self.has_menu = False
        self.has_logo_shown = False
        self.has_subtitle_shown = False
        self.has_footer_shown = False
        self.show = self.SHOW_PAGE

        return True

    def get_content_data(self):
        blog_text = config.blog_text
        projects_text = config.projects_text
        return {"template": "index.tpl", "data": {"blog_text": blog_text, "projects_text": projects_text}}

