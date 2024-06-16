from model import ModelObject

class ProjectLink(ModelObject):
    db_table = "project_link"
    dbmap = [
        'project_id',
        'link_type_id',
        'title',
        'url',
        'weight'
    ]

    linkType = None
    iconString = ""
    iconLinkClass = ""

    def getId(self):
        return self.fields['id']

    def getProjectId(self):
        return self.fields['project_id']

    def getLinkTypeId(self):
        return self.fields['link_type_id']

    def getTitle(self):
        return self.fields['title']

    def getUrl(self):
        return self.fields["url"]

    def getWeight(self):
        return self.fields['weight']


    def getIcon(self):
        return self.iconString

    def setIcon(self, linkType):
        self.linkType = linkType
        if linkType.getIconType() == "fa":
            self.iconString = '<i class="fa fa-%s"></i>' % (linkType.getIcon())
        if linkType.getIconType() == "fsg":
            self.iconString = '<i class="fsg fsg-%s"></i>' % (linkType.getIcon())
        elif linkType.getIconType() == "svg":
            self.iconString = '<img src="/images/%s">' % (linkType.getIcon())

    def getLinkClass(self):
        return self.iconLinkClass

    def setLinkClass(self, linkType):
        self.iconLinkClass = "link-%s" % (linkType.getName())



class ProjectLinkType(ModelObject):
    dbmap = [
        'name',
        'icon_type',
        'icon'
    ]

    def getId(self):
        return self.fields['id']

    def getName(self):
        return self.fields['name']

    def getIconType(self):
        return self.fields['icon_type']

    def getIcon(self):
        return self.fields['icon']


