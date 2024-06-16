from model import ModelObject

class Project(ModelObject):
    db_table = "project"
    dbmap = [
        'name',
        'link',
        'description',
        'image',
        'start_page',
        'blog_tag_link',
        'github',
        'hackaday',
        'twitter',
        'other_links',
        'published'
    ]

    def getId(self):
        return self.fields['id']

    def getName(self):
        return self.fields['name']

    def getLink(self):
        # FIXME resolve paths more dynamically
        return "/projects/" +self.fields["link"]

    def getRelativeLink(self):
        # FIXME resolve paths more dynamically
        return self.fields["link"]

    def getDescription(self):
        return self.fields['description']

    def getImage(self):
        return self.fields['image']

    def getStartPageId(self):
        return self.fields['start_page']

    def hasBlogTag(self):
        return self.fields['blog_tag_link'] != ""

    def getBlogTag(self):
        return self.fields['blog_tag_link']

    def hasLinks(self):
        return self.hasBlogTag() or self.hasGithub() or self.hasHackaday() or self.hasTwitter() or self.hasOtherLinks()

    def hasGithub(self):
        return self.fields['github'] != ""

    def getGithub(self):
        return self.fields['github']

    def getGithubLink(self):
        return "https://github.com/sgreg/" + self.fields['github']

    def hasHackaday(self):
        return self.fields['hackaday'] != ""

    def getHackaday(self):
        return self.fields['hackaday']

    def getHackadayLink(self):
        return "https://hackaday.io/project/" + self.fields['hackaday']

    def hasTwitter(self):
        return self.fields['twitter'] != ""

    def getTwitter(self):
        return self.fields['twitter']

    def getTwitterLink(self):
        return "https://twitter.com/hashtag/" + self.fields['twitter']

    def hasOtherLinks(self):
        return self.fields['other_links']

    def setHasOtherLinks(self, value):
        self.fields['other_links'] = value

    def getPublished(self):
        return self.fields['published'];

    def setPublished(self, published):
        self.fields['published'] = published;

