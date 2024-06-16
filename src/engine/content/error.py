from content import Content

class ErrorPage(Content):
    def setup(self):
        self.code = "404"
        self.error = "Unknown"
        if self.query_dict.has_key("code"):
            self.code = self.query_dict["code"]

        if self.code == "404":
            self.error = "Not Found"
        elif self.code == "403":
            self.error = "Forbidden"

        self.has_pager = False
        self.has_menu = False
        self.has_pager_fill_space = True
        self.show = self.SHOW_ERROR

        self.location = self.getError()
        return False

    def getError(self):
        return "%s %s" % (self.code, self.error)

    def get_content_data(self):
        template = "error.tpl"
        image = "404.png"
        if self.code == "403":
            image = "403.png"

        return {template: "template", "data": {"image": image}}

