from model import ModelObject

class BlogTag(ModelObject):
    db_table = "blog_tag"
    dbmap = [
        'name',
        'link'
    ]

    def getId(self):
        return self.fields['id']

    def getName(self):
        return self.fields['name']

    def getLink(self):
        # FIXME resolve paths more dynamically
        return "/blog/tag/" +self.fields["link"]

    def getRelativeLink(self):
        # FIXME resolve paths more dynamically
        return self.fields["link"]

    def getImage(self):
        # TODO add path
        return self.fields['image']

    def __str__(self):
        return "[tag id %d  name '%s'  link '%s']" % (self.fields['id'], self.fields['name'], self.fields['link'])

class BlogTagCount(BlogTag):
    dbmap = [
        'name',
        'link',
        'entries'
    ]

    fontsize = 0;

    def getCount(self):
        return self.fields['entries']

    def setFontsize(self, fontsize):
        self.fontsize = fontsize

    def getFontsize(self):
        return self.fontsize;

    def __str__(self):
        return "[tag id %d  name '%s'  link '%s' %d entries]" % (self.fields['id'], self.fields['name'], self.fields['link'], self.fields['entries'])
