import config
from datetime import datetime

import ext.quik as quik

from content.error import ErrorPage
from model.blog_category import BlogCategory
from model.blog_comment import BlogComment
from model.blog_entry import BlogEntry
from model.blog_tag import BlogTagCount


class TemplateHandler(object):
    content = None

    def __init__(self, content):
        self.content = content
        self.loader = quik.FileLoader(config.template_dir)


    def build_content_page(self):
        # TODO split main template between standard html part (mostly headers) and content.
        #      use one for index and one for everything else.
        #      keep in mind that header navi and such is same but logo, location and pager-bar are missing from index
        pass

    def build_page(self):
        page_template = self.loader.load_template("page.tpl")

        page_info = self.content.get_page_info()

        meta_data = self.content.get_page_meta_data()
        if meta_data["page_title"] == "":
            meta_data["page_title"] = meta_data["title"]

        data = {}
        template = "error.tpl"
        content_parsed = ""
        content_type = self.content.get_content_type()
        if content_type == self.content.SHOW_ERROR:
            page_info['location_icon'] = "warning"
            page_info['location'] = "404 Not Found"
            data = {"image": "404.png"}

            if isinstance(self.content, ErrorPage):
                page_info['location'] = self.content.getError()
                content_data = self.content.get_content_data()
                data = content_data["data"]

        elif content_type == self.content.SHOW_EMPTY:
            template = "no_content.tpl"

        else:
            content_data = self.content.get_content_data()
            template = content_data['template']
            data = content_data['data']

        content_tpl = self.loader.load_template(template)
        content_parsed = content_tpl.render(data)

        pager_bar_parsed = ""
        has_pager_bar = self.content.has_pager_data()
        if has_pager_bar:
            pager_bar_data = self.content.get_pager_data()
            if pager_bar_data is None:
                pager_bar_parsed = ""
            else:
                pager_bar_tpl = self.loader.load_template(pager_bar_data['template'])
                pager_bar_parsed = pager_bar_tpl.render(pager_bar_data['data'])


        menu_parsed = ""
        has_menu = self.content.has_menu_data()
        if has_menu:
            menu_data = self.content.get_menu_data()
            menu_tpl = self.loader.load_template(menu_data['template'])
            menu_parsed = menu_tpl.render(menu_data['data'])


        page_data = {
            "meta": meta_data,
            "info": page_info,
            "has_pager_bar": has_pager_bar, # XXX could go to page_info?
            "has_pager_space": self.content.has_pager_space(), # XXX could go to page_info?
            "has_menu": has_menu,           # XXX could go to page_info?
            "has_logo": self.content.has_logo(),
            "has_subtitle": self.content.has_subtitle(),
            "has_footer": self.content.has_footer(),
            "pager_bar": pager_bar_parsed,
            "content": content_parsed,
            "menu": menu_parsed
        }

        print(page_template.render(page_data, loader=self.loader))


