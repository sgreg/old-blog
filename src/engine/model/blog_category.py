from model import ModelObject

class BlogCategory(ModelObject):
    db_table = "blog_category"
    dbmap = [
        'name',
        'link',
        'description',
        'image'
    ]

    def getId(self):
        return self.fields['id']

    def getName(self):
        return self.fields['name']

    def getNameNbsp(self):
        return self.fields['name'].replace(" ", "&nbsp;")

    def getLink(self):
        # FIXME resolve paths more dynamically
        return "/blog/category/" +self.fields["link"]

    def getRelativeLink(self):
        # FIXME resolve paths more dynamically
        return self.fields["link"]

    def getDescription(self):
        return self.fields['description']

    def getImage(self):
        # TODO add path
        return self.fields['image']


class BlogCategoryCount(BlogCategory):
    dbmap = [
        'name',
        'link',
        'description',
        'image',
        'entries'
    ]

    def getCount(self):
        return self.fields['entries']

    def __str__(self):
        return "[tag id %d  name '%s'  link '%s' %d entries]" % (self.fields['id'], self.fields['name'], self.fields['link'], self.fields['entries'])
