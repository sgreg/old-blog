from __future__ import print_function
import os
import re
import math
from datetime import datetime

from engine import util
from engine import config
from content import Content
from engine.model.blog_entry import BlogEntry, BlogEntryPreview
from engine.model.blog_category import BlogCategory, BlogCategoryCount
from engine.model.blog_comment import BlogComment
from engine.model.blog_tag import BlogTag, BlogTagCount

#   TODO
#   - add "listed" flag to db
#       -> if 0, don't show in tag/category listings
#       -> use for e.g. news section
#       -> ..or then add new type "news" but that's mostly copy/paste from blog type

class BlogPage(Content):

    def setup(self):
        self.show = self.SHOW_LIST
        self.filter = self.query_dict["filter"] if self.query_dict.has_key("filter") else ""
        self.filter_content = ""
        self.content = None
        self.selected = "blog"
        self.location_icon = ""
        self.location = ""
        self.current_page = 1
        self.article_count = 0
        self.base_link = "/blog/"
        self.search_link = ""

        self.has_new_comment_submit = False

        self.check_pager() # sets self.content_request and self.current_page
        count = config.blog_entries_per_page
        offset = config.blog_entries_per_page * (self.current_page-1)

        if self.request_method == "POST" and self.request_fields.has_key("comment_submit"):
            self.has_new_comment_submit = True

        if self.filter == "":
            # no filter, list all articles - page number in query_dict["content"]
            # rewriterule regex magic actually makes /blog/<number> to filter=&content=<number>
            self.content = [BlogEntryPreview(row) for row in self.db.getArticles(count, offset)]
            self.setup_pager()
            if len(self.content) > 0 and self.current_page <= self.page_count:
                self.show = self.SHOW_LIST
            else:
                self.show = self.SHOW_EMPTY

        elif self.filter == "article":
            if self.query_dict["content"] == "":
                # no actual article selected, show error
                self.show = self.SHOW_ERROR

            else:
                article = self.db.getArticleByLink(self.query_dict["content"])
                if article is not None:
                    # article valid, display it
                    self.location_icon = ""
                    self.location = "" # don't show any location
                    self.show = self.SHOW_PAGE
                    self.content = article
                else:
                    # article invalid, show error
                    self.show = self.SHOW_ERROR

        elif self.filter == "tag":
            if self.query_dict["content"] == "":
                # no actual tag selected, show error
                # FIXME is this really an error case? what else could be shown? list of tags?
                self.show = self.SHOW_ERROR

            else:
                tag = self.db.getTagByLink(self.content_request)
                if tag is not None:
                    self.filter_content = tag.getName()
                    self.content = [BlogEntryPreview(row) for row in self.db.getArticlesByTagId(tag.getId(), count, offset)]
                    
                    self.location_icon = "tag"
                    self.location = tag.getName()

                    self.setup_pager(tag.getId())
                    if len(self.content) > 0 and self.current_page <= self.page_count:
                        self.show = self.SHOW_LIST
                    else:
                        self.show = self.SHOW_EMPTY
                else:
                    self.show = self.SHOW_ERROR

        elif self.filter == "category":
            if self.query_dict["content"] == "":
                # no actual category selected, show error
                # FIXME again, is this really error case?
                self.show = self.SHOW_ERROR
 
            else:
                category = self.db.getCategoryByLink(self.content_request)
                if category is not None:
                    self.filter_content = category.getName()
                    self.content = [BlogEntryPreview(row) for row in self.db.getArticlesByCategoryId(category.getId(), count, offset)]
                    self.location_icon = category.getImage()
                    self.location = category.getName()

                    self.setup_pager(category.getId())
                    if len(self.content) > 0 and self.current_page <= self.page_count:
                        self.show = self.SHOW_LIST
                    else:
                        self.show = self.SHOW_EMPTY
                else:
                    self.show = self.SHOW_ERROR

        else:
            self.show = self.SHOW_ERROR


        self.has_pager = True
        self.has_menu = True
        valid = True

        if self.show == self.SHOW_PAGE:
            self.has_pager = False # XXX might have for prev/next article navigation!
            self.has_menu = False
        elif self.show == self.SHOW_EMPTY:
            self.has_pager = False
            self.has_pager_fill_space = True
        elif self.show == self.SHOW_ERROR:
            self.has_pager = False
            valid = False

        return valid
        

    def get_page_meta_data(self):
        self.meta_data["url"] = util.getCanonical(self.request_uri)

        if self.show == self.SHOW_PAGE:
            self.meta_data["type"] = "article"
            self.meta_data["title"] = self.content.getTitle().replace('"', '&quot;')
            self.meta_data["page_title"] = "%s - sgreg.fi Blog" % (self.content.getTitle())
            self.meta_data["image"] = util.getCanonicalImage(self.content.getPreviewImage())
            self.meta_data["description"] = self.content.getPreview().replace('"', '&quot;')

        elif self.show == self.SHOW_LIST and self.filter != "" and self.filter_content != "":
            if self.filter == "tag":
                # FIXME
                self.meta_data["title"] = "Blog Articles tagged with %s (page %s)" % (self.filter_content, self.current_page)
                self.meta_data["description"] = "All blog articles tagged with %s" % (self.filter_content)
            else:
                self.meta_data["title"] = "Blog Articles in category %s (page %s)" % (self.filter_content, self.current_page)
                self.meta_data["description"] = "All blog articles in the category %s" % (self.filter_content)

        else:
            self.meta_data["url"] = util.getCanonical("/blog/")
            self.meta_data["title"] = "sgreg.fi - the Blog of Sven Gregori"
            self.meta_data["description"] = config.blog_text

        return self.meta_data


    def check_pager(self):
        # TODO find out how to deal with general blog pages. i.e. /blog/n or rather /blog/list/all/n
        self.content_request = self.query_dict["content"]
        if self.filter == "" and re.match(r"^[0-9]+/?$", self.content_request):
            current_page = self.content_request.split("/", 1)[0]
        elif self.filter != "" and  "/" in self.content_request:
            (self.content_request, current_page) = self.content_request.split("/", 1)
        else:
            current_page = 1

        try:
            self.current_page = int(current_page)
        except ValueError:
            self.current_page = 1


    def setup_pager(self, dbid=0):
        self.base_link = "/blog/%s/%s/" % (self.filter, self.content_request)

        if self.filter == "category":
            self.article_count = self.db.getArticleCountForCategoryId(dbid)
        elif self.filter == "tag":
            self.article_count = self.db.getArticleCountForTagId(dbid)
        else: # all pages
            # TODO
            self.article_count = self.db.getArticlesCount()
            self.base_link = "/blog/"

        self.page_count = int(math.ceil(float(self.article_count) / config.blog_entries_per_page))

    def get_pager_data(self):
        if not self.has_pager:
            return None

        template = ""
        data = None
        if self.show == self.SHOW_PAGE:
            # XXX not yet, TODO add prev/next article
            template = ""
            comments = None
            data = {}
        elif self.show == self.SHOW_LIST:
            template = "blog_pager_bar.tpl"
            data = {
                "cnt" : self.article_count,
                "page_count": self.page_count,
                "pages": range(self.page_count + 1)[1:],
                "current_page": self.current_page,
                "base_link": self.base_link
            }

        return {"template": template, "data": data}


    def get_menu_data(self):
        if not self.has_menu:
            return None

        cats = [BlogCategory(row) for row in self.db.getCategoryList()]

        blog_tag_counts = [BlogTagCount(row) for row in self.db.getTagListCount()]
        if len(blog_tag_counts) > 0:
            max_count = max([t.getCount() for t in blog_tag_counts])
            min_count = min([t.getCount() for t in blog_tag_counts])
            diff = max_count - min_count
            if diff == 0:
                delta = 1
            else:
                delta = float(config.blog_tagcloud_max_font - config.blog_tagcloud_min_font) / diff

            for t in blog_tag_counts:
                t.setFontsize(config.blog_tagcloud_min_font + (delta * (t.getCount() - 1)))

        menu_data = {
            "template": "blog_menu.tpl", # FIXME should content/* really know anything about templates?
            "data": {
                "categories": cats,
                "tags": blog_tag_counts
            }
        }

        return menu_data

    def get_content_data(self):
        template = ""
        data = None

        if self.show == self.SHOW_PAGE:
            template = "blog_article.tpl"
            categories = [BlogCategory(row) for row in self.db.getCategoriesForArticleId(self.content.getId())]
            tags = [BlogTag(row) for row in self.db.getTagsForArticleId(self.content.getId())]
            comments = [BlogComment(row) for row in self.db.getCommentsForArticleId(self.content.getId(), True)]
            new_comment_submitted = self.handle_new_comment()
            data = {"article" : self.content, "categories": categories, "tags": tags, "comments": comments, "new_comment": new_comment_submitted}

        elif self.show == self.SHOW_LIST:
            template = "blog_list.tpl"
            for entry in self.content:
                entry.setCommentCount(self.db.getCommentsCountForArticleId(entry.getId(), True))
                entry.setCategories([BlogCategory(row) for row in self.db.getCategoriesForArticleId(entry.getId())][:config.blog_preview_max_categories])
            data = {"blog_entries": self.content}

        return {"template": template, "data": data}


    def handle_new_comment(self):
        new_comment_submitted = False

        if self.has_new_comment_submit:
            newcmt_ip = ""
            if os.environ.has_key("REMOTE_ADDR"):
                newcmt_ip = os.environ.get("REMOTE_ADDR")
            newcmt_useragent = ""
            if os.environ.has_key("HTTP_USER_AGENT"):
                newcmt_useragent = os.environ.get("HTTP_USER_AGENT")
            newcmt_referer = ""
            if os.environ.has_key("HTTP_REFERER"):
                newcmt_referer = os.environ.get("HTTP_REFERER")

            new_comment = BlogComment((
                -1,
                self.content.getId(),
                self.request_fields.getvalue("comment_author"),
                self.request_fields.getvalue("comment_email"),
                self.request_fields.getvalue("comment_address"),
                self.request_fields.getvalue("comment_content"),
                datetime.now(),
                0,
                config.blog_comments_auto_publish,
                newcmt_ip,
                newcmt_useragent,
                newcmt_referer
            ))

            if self.request_fields.getvalue("comment_submit") == "add":
                new_comment.insertDbEntry(self.db)
                new_comment_submitted = True
            
        return new_comment_submitted

