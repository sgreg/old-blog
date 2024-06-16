import os

from engine import util
from engine import config
from content import Content
from engine.model.project import Project
from engine.model.project_page import ProjectPage, ProjectPageLink
from engine.model.project_link import ProjectLink

class ProjectPage(Content):

    def setup(self):
        self.project = None
        self.page = None
        self.selected = "projects"
        self.location_icon = ""
        self.location = ""

        if self.query_dict["project"] == "":
            self.show = self.SHOW_LIST;
        else:
            self.project = self.db.getProjectByLink(self.query_dict["project"])
            if self.project is None:
                # unknown project
                self.show = self.SHOW_ERROR

            else:
                if self.query_dict["content"] == "":
                    self.page = self.db.getProjectStartPage(self.project.getId())
                else:
                    self.page = self.db.getProjectPageByLink(self.project.getId(), self.query_dict["content"])

                if self.page is None:
                    # unknown project page
                    self.show = self.SHOW_ERROR
                else:
                    self.location = self.project.getName()
                    self.location_icon = "flask"
                    self.show = self.SHOW_PAGE

        self.has_pager = False
        self.has_pager_fill_space = True
        self.has_menu = True
        valid = True

        if self.show == self.SHOW_ERROR:
            valid = False
            self.has_menu = False
        elif self.show == self.SHOW_LIST:
            self.has_menu = False

        return valid

    def get_page_meta_data(self):
        self.meta_data["url"] = util.getCanonical(self.request_uri)

        if self.show == self.SHOW_PAGE:
            if self.query_dict["content"] == "":
                self.meta_data["title"] = "%s" % (self.project.getName())
            else:
                self.meta_data["title"] = "%s: %s" % (self.project.getName(), self.page.getTitle())
            self.meta_data["page_title"] = "%s - sgreg.fi Projects" % (self.meta_data["title"])
            self.meta_data["image"] = util.getCanonicalImage(self.project.getImage())
            self.meta_data["description"] = self.project.getDescription()
        else:
            self.meta_data["url"] = util.getCanonical("/projects/")
            self.meta_data["title"] = "sgreg.fi - The Projects"
            self.meta_data["description"] = config.projects_text

        return self.meta_data

    def get_menu_data(self):
        if not self.has_menu:
            return None

        template = "project_menu.tpl"
        pages = [ProjectPageLink(row) for row in self.db.getProjectPagesLinks(self.project.getId())]
        links = [ProjectLink(row) for row in self.db.getProjectLinks(self.project.getId())]
        for link in links:
            linkType = self.db.getProjectLinkType(link.getLinkTypeId())
            link.setIcon(linkType)
            link.setLinkClass(linkType)

        data = {"project": self.project, "pages": pages, "links": links}
        return {"template": template, "data": data}


    def get_content_data(self):
        template = ""
        data = None

        if self.show == self.SHOW_PAGE:
            template = "project_page.tpl"
            data = {"page": self.page}

        elif self.show == self.SHOW_LIST:
            template = "project_list.tpl"
            projects = [Project(row) for row in self.db.getProjects()]
            data = {"projects": projects}

        return {"template": template, "data": data}

