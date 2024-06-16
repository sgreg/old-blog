from content import Content

class StaticPage(Content):

    def setup(self):
        self.selected = "projects"
        self.location_icon = "gears"
        self.location = "Projects"

        if self.query_dict["content"] == "":
            self.show = self.SHOW_ERROR

        elif self.query_dict["content"] == "about":
            self.selected = "about"
            self.location_icon = "user"
            self.location = "About"
            self.show = self.SHOW_PAGE

        elif self.query_dict["content"] == "contact":
            self.selected = "contact"
            self.location_icon = "envelope"
            self.location = "Contact"
            self.show = self.SHOW_PAGE

        else:
            self.show = self.SHOW_ERROR

        self.has_pager = False
        self.has_pager_fill_space = True
        self.has_menu = False
        valid = True
        if self.show == self.SHOW_ERROR:
            valid = False

        return valid


    def get_content_data(self):
        if self.show == self.SHOW_PAGE:
            template = "static_page.tpl"
            page = self.db.getStaticPageByLink(self.query_dict["content"])
            data = {"page": page}

            return {"template": template, "data": data}

        return None


