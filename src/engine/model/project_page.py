from model import ModelObject

class ProjectPageLink(ModelObject):
    db_table = "project_page"
    dbmap = [
        'project_id',
        'title',
        'link',
        'weight',
        'modified',
        'published'
    ]

    def getId(self):
        return self.fields['id']

    def getProjectId(self):
        return self.fields['project_id']

    def getTitle(self):
        return self.fields['title']

    def getLink(self):
        # XXX this needs /<path to webroot>/projects/<project name>/ prefixed
        return self.fields["link"]

    def getRelativeLink(self):
        return self.fields["link"]

    def getWeight(self):
        return self.fields['weight']

    def getModified(self):
        return self.fields['modified']

    def setModified(self, modified):
        self.fields['modified'] = modified

    def getPublished(self):
        return self.fields['published'];

    def setPublished(self, published):
        self.fields['published'] = published;



class ProjectPage(ProjectPageLink):
    dbmap = [
        'project_id',
        'title',
        'link',
        'weight',
        'modified',
        'published',
        'content',
        'parsed'
    ]

    def getContent(self):
        return self.fields['content']

    def getParsed(self):
        return self.fields['parsed']

    def setParsed(self, parsed_content):
        self.fields["parsed"] = parsed_content


