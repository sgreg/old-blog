from model import ModelObject

class BlogEntry(ModelObject):
    db_table = "blog_entry"
    dbmap = [
        'title',
        'link',
        'preview',
        'preview_image',
        'content',
        'parsed',
        'created',
        'indexed',
        'published'
    ]

    def getId(self):
        return self.fields["id"]

    def getTitle(self):
        return self.fields["title"]

    def getLink(self):
        # FIXME resolve paths more dynamically
        return "/blog/article/" +self.fields["link"]

    def getRelativeLink(self):
        # FIXME resolve paths more dynamically
        return self.fields["link"]

    def getPreview(self):
        return self.fields["preview"]

    def getPreviewImage(self):
        return self.fields["preview_image"]

    def getContent(self):
        return self.fields["content"]

    def getParsed(self):
        return self.fields["parsed"]
    
    def setParsed(self, parsed_content):
        self.fields["parsed"] = parsed_content

    def getCreated(self):
        return self.fields["created"]

    def setCreated(self, created):
        self.fields["created"] = created

    def getIndexed(self):
        return self.fields["indexed"]

    def getPublished(self):
        return self.fields["published"]


    def __str__(self):
        return "BlogEntry [id %s title '%s']" % (self.fields['id'], self.fields['title']) 


class BlogEntryPreview(BlogEntry):
    # FIXME preview doesn't really need 'content' and 'parsed', would be more efficient without
    #       but that will require adjustments to all database functions...
    comments = 0
    categories = []

    def setCommentCount(self, count):
        self.comments = count

    def  getCommentCount(self):
        return self.comments

    def setCategories(self, categories):
        self.categories = categories

    def getCategories(self):
        return self.categories

