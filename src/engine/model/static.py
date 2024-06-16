from model import ModelObject

class StaticPage(ModelObject):
    db_table = "static_page"
    dbmap = [
        'title',
        'link',
        'content',
        'parsed'
    ]

    def getId(self):
        return self.fields['id']

    def getTitle(self):
        return self.fields['title']

    def getLink(self):
        # XXX this needs /<path to webroot>/projects/<project name>/ prefixed
        return self.fields["link"]

    def getRelativeLink(self):
        return self.fields["link"]

    def getContent(self):
        return self.fields['content']

    def getParsed(self):
        return self.fields['parsed']

    def setParsed(self, parsed_content):
        self.fields["parsed"] = parsed_content

