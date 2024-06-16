from model import ModelObject
from blog_tag import BlogTag

class BlogComment(ModelObject):
    db_table = "blog_comment"
    dbmap = [
        'blog_entry_id',
        'author',
        'email',
        'address',
        'content',
        'created',
        'is_chef',
        'published',
        'ip',
        'useragent',
        'referer'
    ]

    def getId(self):
        return self.fields['id']

    def getBlogEntryId(self):
        return self.fields['blog_id']

    def getAuthor(self):
        return self.fields['author']

    def getEmail(self):
        return self.fields['email']

    def getAddress(self):
        return self.fields['address']

    def getContent(self):
        return self.fields['content']

    def getCreated(self):
        return self.fields['created']

    def isChef(self):
        return self.fields['is_chef']

    def getPublished(self):
        return self.fields['published']

    def getIp(self):
        return self.fields['ip']

    def getUserAgent(self):
        return self.fields['useragent']

    def getReferer(self):
        return self.fields['referer']

    def __str__(self):
        return "BlogEntry [id %d blog entry %d written by %s on %s]" % (self.fields['id'], self.fields['blog_id'], self.fields['author'], str(self.fields['created'])) 
