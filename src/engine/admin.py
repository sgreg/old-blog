from __future__ import print_function
import os
import re
import cgi
from glob import glob
from datetime import datetime

import database
import template
import ext.mistune as mistune
from engine.model.blog_entry import BlogEntry
from engine.model.blog_tag import BlogTag
from engine.model.blog_category import BlogCategory
from engine.model.blog_comment import BlogComment
from engine.model.project import Project
from engine.model.project_page import ProjectPage
from engine.model.project_link import ProjectLink
from engine.model.static import StaticPage

#   TODO
#   - add db insert/update function to all model types
#   - use model types for show/edit functionality instead of local variables

class AdminBuilder(object):
    def __init__(self):
        query_string = os.environ.get("QUERY_STRING")
        redir_url = os.environ.get("REDIRECT_URL")
        self.method = os.environ.get("REQUEST_METHOD")
        self.query_string = query_string
        self.request = cgi.FieldStorage(keep_blank_values=True)
        #self.template_handler = template.TemplateHandler()

    def send_headers(self):
        print("Status: 200 OK")
        print("Content-type: text/html")
        print("")

    def setup(self):
        database.initialize()
        self.db = database.database
        self.page = "index"
        if self.request.has_key("page"):
            self.page = self.request.getvalue("page")
        self.action = "list"
        if self.request.has_key("action"):
            self.action = self.request.getvalue("action")
        self.dbid = ""
        if self.request.has_key("dbid"):
            self.dbid = self.request.getvalue("dbid")

    def build(self):
        self.send_headers()
        print("""
<!doctype html>
<html class="no-js" lang="">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <title>sgreg.fi</title>
        <meta name="description" content="Sven Gregori - Blog and Projects">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link rel="icon" href="/favicon.png">
        <link rel="apple-touch-icon" href="/apple-touch-icon.png">

        <link rel="stylesheet" href="/css/normalize.css">
        <link rel="stylesheet" href="/css/font-awesome.min.css">
        <link rel="stylesheet" href="/css/font-sgreg.css">
        <link rel="stylesheet" href="/css/prism-sgreg.css">
        <link rel="stylesheet" href="/css/sgreg-1.0.6.css">
    </head>
    <body>
        
        """)
        #self.template_handler.build_page_top()

        self.setup()
        if self.page == "index":
            self.show_index()

        elif self.page == "blog":
            self.show_blog()
        elif self.page == "comments":
            self.show_blog_comments()
        elif self.page == "categories":
            self.show_blog_categories()
        elif self.page == "tags":
            self.show_blog_tags()
        
        elif self.page == "projects":
            self.show_projects()
        elif self.page == "project_pages":
            self.show_project_pages()
        
        elif self.page == "static":
            self.show_static()
        else:
            self.show_error()
        #self.template_handler.build_page_bottom()

        print("""
    </body>
</html>
        """)


    #
    #   INDEX
    #

    def show_index(self):
        print('index<br>')
        print('<a href="?page=blog">Blog</a><br>')
        print('<a href="?page=projects">Projects</a><br>')
        print('<a href="?page=static">Static</a><br>')




    #
    #   BLOG
    #

    def show_blog(self):
        print("blog<br>")
        print('<a href="uberuser.sg">Index</a><br>')
        if self.action == "list":
            self.blog_list()
        elif self.action == "edit" and self.dbid != "":
            self.blog_edit()
        else:
            self.show_error()

    def blog_list(self):
        print('<a href="?page=blog&action=edit&dbid=new">New Entry</a><br>')
        print('<a href="?page=categories">Blog Categories</a><br>')
        print('<a href="?page=tags">Blog Tags</a><br>')
        print('<br>blog list<br>')
        print('<table>')
        self.order = "created"
        if self.request.has_key("order"):
            self.order = self.request.getvalue("order")

        self.order_dir = "asc"
        if self.request.has_key("order_dir"):
            self.order_dir = self.request.getvalue("order_dir")
        
        if self.order_dir == "asc":
            next_order_dir = "desc"
        else:
            next_order_dir = "asc";

        print("<br>order by %s %s<br>" % (self.order, self.order_dir))
        articles = [BlogEntry(row) for row in self.db.getAllArticles(self.order, self.order_dir)]
        print('<thead>')
        print('<td><a href="?page=blog&order=id&order_dir=' + next_order_dir + '">#</a></td>')
        print('<td><a href="?page=blog&order=title&order_dir=' + next_order_dir + '">Title</a></td>')
        print('<td><a href="?page=blog&order=created&order_dir=' + next_order_dir + '">Created</a></td>')
        print('<td>Comments</td>')
        print('</thead>')
        for article in articles:
            print('<tr>')
            print('<td>' + str(article.getId()) + '</td>')
            print('<td><a href="?page=blog&action=edit&dbid=' + str(article.getId()) + '">' + article.getTitle() + '</a></td>')
            print('<td>' + str(article.getCreated()) + '</td>')
            allComments = self.db.getCommentsCountForArticleId(article.getId())
            publishedComments = self.db.getCommentsCountForArticleId(article.getId(), True)
            unpublishedComments = allComments - publishedComments
            unpubCmtString = ""
            if unpublishedComments != 0:
                unpubCmtString = ' <span style="color:#cc0000;">(' + str(unpublishedComments)+ ')</span>'
            print('<td><a href="?page=comments&action=list&dbid=' + str(article.getId()) + '">' + str(allComments) + ' Comments</a>' + unpubCmtString + '</td>')
            print('</tr>')
        print('</table>')


    def blog_edit(self):
        print('<a href="?page=blog">Back</a><br>')

        if (self.dbid != "new"):
            print('<a href="?page=comments&action=list&dbid=' + self.dbid + '">' + str(self.db.getCommentsCountForArticleId(self.dbid)) + ' Comments</a><br>')

        print("<br>blog edit " + self.dbid + "<br>")
        if self.method == "POST" and self.request.has_key("blog_submit"):
            article = BlogEntry((
                int(self.dbid) if self.dbid != "new" else -1,
                self.request.getvalue("blog_title"),
                self.request.getvalue("blog_link"),
                self.request.getvalue("blog_preview"),
                self.request.getvalue("blog_image"),
                self.request.getvalue("blog_content"),
                "",
                datetime.strptime(self.request.getvalue("blog_created"), '%Y-%m-%d %H:%M:%S'),
                (self.request.getvalue("blog_indexed") == "on"),
                (self.request.getvalue("blog_published") == "on"),
            ))
            tags = [tag for tag in self.request.getlist("blog_tags") if tag != ""]
            cats = [cat for cat in self.request.getlist("blog_categories") if cat != ""]
            
            article.setParsed(mistune.markdown(article.getContent(), escape=True))

            if self.request.getvalue("blog_submit") == "save":

                if article.getCreated() == "":
                    article.setCreated(datetime.now().replace(microsecond=0))
            
                if self.dbid == "new":
                    err = article.insertDbEntry(self.db)
                else:
                    err = article.updateDbEntry(self.db)

                if err is None:
                    print("successfully saved!")
                    if self.dbid == "new":
                        self.dbid = self.db.lastrowid()
                        article.fields['id'] = self.dbid
                else:
                    print("Error while writing to db: " + str(err))
                    return


                # FIXME is this still needed? do some better magic?
                tagobjs_db = [BlogTag(row) for row in self.db.getTagsForArticleId(int(self.dbid))]
                taglist_db = [tag.getRelativeLink() for tag in tagobjs_db]
                taglist_form = tags
                tags_deleted = [tag for tag in taglist_db if tag not in taglist_form]
                tags_added = [tag for tag in taglist_form if tag not in taglist_db]

                catobjs_db = [BlogCategory(row) for row in self.db.getCategoriesForArticleId(int(self.dbid))]
                catlist_db = [cat.getRelativeLink() for cat in catobjs_db]
                catlist_form = cats
                cats_deleted = [cat for cat in catlist_db if cat not in catlist_form]
                cats_added = [cat for cat in catlist_form if cat not in catlist_db]


                # FIXME use new model insert/update db functions
                for tag in tags_added:
                    tag_db = self.db.getTagByLink(tag)
                    if tag_db is not None:
                        self.db.execute('insert into blog_tag_map(blog_entry_id, blog_tag_id) values(%s, %s)', (int(self.dbid), tag_db.getId()))
                    else:
                        self.db.execute('insert into blog_tag(name, link) values(%s, %s)', (tag, self.titleToLink(tag)))
                        last_tag_id = self.db.lastrowid()
                        self.db.execute('insert into blog_tag_map(blog_entry_id, blog_tag_id) values(%s, %s)', (int(self.dbid), last_tag_id))

                for tag in tags_deleted:
                    tag_db = self.db.getTagByLink(tag)
                    if tag_db is not None:
                        self.db.execute('delete from blog_tag_map where blog_entry_id=%s and blog_tag_id=%s', (int(self.dbid), tag_db.getId()))


                for cat in cats_added:
                    cat_db = self.db.getCategoryByLink(cat)
                    if cat_db is not None:
                        self.db.execute('insert into blog_category_map(blog_entry_id, blog_category_id) values(%s, %s)', (int(self.dbid), cat_db.getId()))
                    else:
                        self.db.execute('insert into blog_category(name, link) values(%s, %s)', (cat, self.titleToLink(cat)))
                        last_cat_id = self.db.lastrowid()
                        self.db.execute('insert into blog_category_map(blog_entry_id, blog_category_id) values(%s, %s)', (int(self.dbid), last_cat_id))

                for cat in cats_deleted:
                    cat_db = self.db.getCategoryByLink(cat)
                    if cat_db is not None:
                        print("<br><br>deleting cat from db")
                        self.db.execute('delete from blog_category_map where blog_entry_id=%s and blog_category_id=%s', (int(self.dbid), cat_db.getId()))


        elif self.method == "GET" and self.dbid != "new":
            article = self.db.getArticleById(self.dbid)
            if article is None:
                print("no such entry")
                return

            taglist = [BlogTag(row) for row in self.db.getTagsForArticleId(int(self.dbid))]
            tags = [tag.getRelativeLink() for tag in taglist]
            #tags = " ".join(tag.getName() for tag in taglist)

            catlist = [BlogCategory(row) for row in self.db.getCategoriesForArticleId(int(self.dbid))]
            cats = [cat.getRelativeLink() for cat in catlist]
            #categories = " ".join(cat.getName() for cat in catlist)

        else:
            article = BlogEntry()
            article.setCreated(datetime.now().replace(microsecond=0))
            tags = []
            cats = []

        preview_values = {
            "link" : article.getLink(),
            "title" : article.getTitle(),
            "preview_image" : article.getPreviewImage(), # FIXME always make sure there's a valid default image to avoid 404/401 errors
            "preview" : article.getPreview(),
            "date" : article.getCreated().strftime("%a, %d. %b %Y"),
            "comments" : "x"
        }
        print('<h2>Preview</h2>')
        print('<div style="width:100%;overflow:hidden">')
        print("FIXME old template handler leftover, add new one")
        #self.template_handler.build("blog_preview", preview_values)
        print('</div>')

        print('<h2>Article</h2>')
        article.setParsed(mistune.markdown(article.getContent(), escape=True))
        article_values = {
            "title" : article.getTitle(),
            "date" : article.getCreated().strftime("%A, %d. %B %Y"),
            #"date" : self.content.getCreated().strftime("%a, %d. %b %Y"),
            "time" : article.getCreated().strftime("%H:%M"),
            "comment_count" : "x",
            "preview_image" : article.getPreviewImage(),
            "content" : article.getParsed(),
            "tags" : tags,
            "categories" : cats
            # TODO add share links
        }
        print("FIXME old template handler leftover, add new one")
        #self.template_handler.build("blog_article", article_values)

        print("<h2>Edit</h2>")
        print('<form method="POST" class="forms">')

        if self.method == "POST":
            print('<section>')
            print('<button type="primary" name="blog_submit" value="save">Save</button>')
            print('</section>')

        print('<section><label>Title</label>')
        print('<input type="text" name="blog_title" id="blog_title_field" size="50" value="' + article.getTitle().replace('"', '&quot;') + '">')
        print('</section>')
        print('<section><label>Link</label>')
        print('<input type="text" name="blog_link" id="blog_link_field" size="50" value="' + article.getRelativeLink() + '">')
        print('</section>')
        print('<section><label>Preview Image</label>')
        self.printImageSelectionList("blog_image", article.getPreviewImage())
        print('</section>')
        print('<section><label>Preview</label>')
        print('<textarea name="blog_preview" rows="3" cols="80">')
        print(article.getPreview(), end='')
        print('</textarea>')
        print('</section>')
        print('<section><label>Content</label>')
        print('<textarea name="blog_content" rows="20" cols="80">')
        print(article.getContent(), end='')
        print('</textarea>')
        print('</section>')
        print('<section><label>Created</label>')
        print('<input type="text" name="blog_created" value="' + str(article.getCreated()) + '">')
        print('</section>')

        print('<section><label>Tags</label>')
        print('<div id="tagfields">')
        for tag in tags:
            print('<input list="blogtag_list" name="blog_tags" value="' + str(tag) + '">')
        print('</div>')
        print('<input type="button" value="Add Tag" onClick="addInputField(\'tagfields\', \'blog_tags\', \'blogtag_list\');">')
        self.printTagSelectionList()
        print('</section>')

        print('<section><label>Categories</label>')
        print('<div id="catfields">')
        for cat in cats:
            print('<input list="blogcat_list" name="blog_categories" value="' + str(cat) + '">')
        print('</div>')
        print('<input type="button" value="Add Category" onClick="addInputField(\'catfields\', \'blog_categories\', \'blogcat_list\');">')
        self.printCategorySelectionList()
        print('</section>')

        print('<section><label class="checkbox">Indexed</label><input type="checkbox" name="blog_indexed" ' + ('checked' if article.getIndexed() else '') + '/></section>')
        print('<section><label class="checkbox">Published</label><input type="checkbox" name="blog_published" ' + ('checked' if article.getPublished() else '') + '/></section>')
        print('<section>')
        print('<button type="primary" name="blog_submit" value="preview">Preview</button>')
        print('<button type="primary" name="blog_submit" value="save">Save</button>')
        print('</section>')
        print('</form>')
        self.printTitleToLinkJs("blog_title_field", "blog_link_field")
        self.printInputFieldAdderJs()


   
    #
    #   BLOG COMMENTS
    #

    def show_blog_comments(self):
        print('Blog comments<br>')
        print('<a href="uberuser.sg">Index</a><br>')
        if self.action == "list" and self.dbid != "": # dbid == article id
            self.blog_comments_list()
        elif self.action == "edit" and self.dbid != "": # dbid == comment id
            self.blog_comments_edit()
        else:
            self.show_error()

    def blog_comments_list(self):
        print('<a href="?page=blog">Back</a><br>')
        article = self.db.getArticleById(self.dbid);
        print("article " + article.getTitle())

        if self.method == "POST" and self.request.has_key("comment_edit"):
            edit = self.request.getvalue("comment_edit")
            cid = int(self.request.getvalue("comment_id"))
            update = ""
            if edit == "publish":
                update = "published=1"
            elif edit == "unpublish":
                update = "published=0"
            elif edit == "chef":
                update = "is_chef=1"
            elif edit == "unchef":
                update = "is_chef=0"

            if update != "":
                err = self.db.execute('update blog_comment set ' + update + ' where id=%s', (cid,))
                if err is None:
                    print("Successfully saved!")
                else:
                    print("Error while writing to db: " + str(err))

        comments = [BlogComment(row) for row in self.db.getCommentsForArticleId(self.dbid)]
        for comment in comments:
            print('<div>')
            print('<span><b>#' + str(comment.getId()) + '</b></span>')
            print('<span><b>Created:</b> ' + str(comment.getCreated()) + '</span>')
            print('<span><b>Author:</b> ' + comment.getAuthor() + '</span>')
            print('</div>')
            print('<div>')
            print('<span><b>Email:</b> ' + comment.getEmail() + '</span>')
            print('<span><b>Address:</b> ' + comment.getAddress() + '</span>')
            print('<span><b>IP:</b> ' + comment.getIp() + '</span>')
            print('</div>')
            print('<div><b>UserAgent:</b> ' + comment.getUserAgent() + '</div>')
            print('<div><b>Referer:</b> ' + comment.getReferer() + '</div>')
            print('<div><b>Content:</b> <pre>' + comment.getContent() + '</pre></div>')
            print('<form method="POST" class="forms">')
            print('<input type="hidden" name="comment_id" value="' + str(comment.getId()) + '" />')

            if comment.getPublished():
                publish_value = "unpublish"
                publish_text = "Unpublish"
                publish_class = "primary"
            else:
                publish_value = "publish"
                publish_text = "Publish"
                publish_class = ""

            print('<button type="' + publish_class + '" name="comment_edit" value="' + publish_value + '">' + publish_text + '</button>')

            if comment.isChef():
                chef_value = "unchef"
                chef_text = "Unmake chef"
                chef_class = "primary"
            else:
                chef_value = "chef"
                chef_text = "Make chef"
                chef_class = ""

            print('<button type="' + chef_class + '" name="comment_edit" value="' + chef_value + '">' + chef_text + '</button>')
            print('<a href="?page=comments&action=edit&dbid=' + str(comment.getId()) + '">Edit</a>')
            print('</form>')
            print('<br><br>')


    def blog_comments_edit(self):
        comment = self.db.getCommentById(self.dbid)
        if comment is None:
            print("no such comment")
            return

        print('<a href="?page=comments&action=list&dbid=' + str(comment.getBlogEntryId()) + '">Back</a><br>')
        print('Blog edit ' + self.dbid + '<br>')

        if self.method == "POST" and self.request.has_key("comment_edit_submit"):
            content = self.request.getvalue("comment_content")

            if self.request.getvalue("comment_edit_submit") == "save":
                self.db.sanitize(content)
                err = self.db.execute('update blog_comment set content=%s where id=%s', (content, int(self.dbid)))
                if err is None:
                    print("Successfully saved!")
                else:
                    print("Error while writing to db: " + str(err))
        else:
            content = comment.getContent()

        print('<form method="POST" class="forms">')
        print('<textarea name="comment_content" rows="10" cols="80">')
        print(content, end='')
        print('</textarea>')
        print('<button type="primary" name="comment_edit_submit" value="save">Save</button>')
        print('</form>')


    def show_blog_categories(self):
        print('Blog Categories<br>')
        print('<a href="uberuser.sg">Index</a><br>')
        if self.action == "list":
            self.blog_categories_list()
        elif self.action == "edit" and self.dbid != "":
            self.blog_categories_edit()
        else:
            self.show_error()

    def blog_categories_list(self):
        print('<a href="?page=blog">Back</a><br>')
        print('<a href="?page=categories&action=edit&dbid=new">New Category</a><br>')
        print('Category list<br>')
        print('<table>')
        self.order = "id"
        if self.request.has_key("order"):
            self.order = self.request.getvalue("order")

        self.order_dir = "asc"
        if self.request.has_key("order_dir"):
            self.order_dir = self.request.getvalue("order_dir")
        
        if self.order_dir == "asc":
            next_order_dir = "desc"
        else:
            next_order_dir = "asc";
        catobjs = [BlogCategory(row) for row in self.db.getCategoryList(self.order, self.order_dir)]
        print('<thead>')
        print('<td><a href="?page=categories&order=id&order_dir=' + next_order_dir + '">#</a></td>')
        print('<td></td>')
        print('<td><a href="?page=categories&order=name&order_dir=' + next_order_dir + '">Title</a></td>')
        print('<td>Articles</td>')
        print('</thead>')
        for cat in catobjs:
            print('<tr>')
            print('<td>' + str(cat.getId()) + '</td>')
            print('<td><i class="' + cat.getImage() + '"></i></td>')
            print('<td><a href="?page=categories&action=edit&dbid=' + str(cat.getId()) + '">' + cat.getName() + '</a></td>')
            print('<td>' + str(self.db.getArticleCountForCategoryId(cat.getId())) + '</td>')
            print('</tr>')
        print('</table>')


    def blog_categories_edit(self):
        print('<a href="?page=categories">Back</a><br>')
        print('<br>Category edit ' + self.dbid + '<br>')
        if self.method == "POST" and self.request.has_key("cat_submit"):
            cat = BlogCategory((
                int(self.dbid) if self.dbid != "new" else -1,
                self.request.getvalue("cat_name"),
                self.request.getvalue("cat_link"),
                self.request.getvalue("cat_desc"),
                self.request.getvalue("cat_image")
            ))

            if self.request.getvalue("cat_submit") == "save":
                if self.dbid == "new":
                    err = cat.insertDbEntry(self.db)
                else:
                    err = cat.updateDbEntry(self.db)

                if err is None:
                    print("Successfully saved!")
                    if self.dbid == "new":
                        self.dbid = self.db.lastrowid()
                        cat.fields['id'] = self.dbid
                else:
                    print("Error while writing to db: " + str(err))

        elif self.method == "GET" and self.dbid != "new":
            cat = self.db.getCategoryById(self.dbid)
            if cat is None:
                print("no such category")
                return
            print("<h2>Edit</h2>")

        else:
            cat = BlogCategory()
            print("<h2>New</h2>")

        print('<form method="POST" class="forms">')
        print('<section><label>Name</label>')
        print('<input type="text" name="cat_name" id="cat_name" size="50" value="' + cat.getName() + '">')
        print('</section>')
        print('<section><label>Link</label>')
        print('<input type="text" name="cat_link" id="cat_link" size="50" value="' + cat.getRelativeLink() + '">')
        print('</section>')
        print('<section><label>Description</label>')
        print('<input type="text" name="cat_desc" size="50" value="' + cat.getDescription() + '">')
        print('</section>')
        print('<section><label>Image (only icon font images, raw &lt;i class value)</label>')
        print('<input type="text" name="cat_image" size="50" value="' + cat.getImage() + '"> <i class="' + cat.getImage() + '"></i>')
        print('</section>')
        print('<section>')
        print('<button type="primary" name="cat_submit" value="save">Save</button>')
        print('</section>')
        print('</form>')
        self.printTitleToLinkJs("cat_name", "cat_link")



    def show_blog_tags(self):
        print('Blog Tags<br>')
        print('<a href="uberuser.sg">Index</a><br>')
        if self.action == "list":
            self.blog_tags_list()
        elif self.action == "edit" and self.dbid != "":
            self.blog_tags_edit()
        else:
            self.show_error()

    def blog_tags_list(self):
        print('<a href="?page=blog">Back</a><br>')
        print('<a href="?page=tags&action=edit&dbid=new">New Tag</a><br>')
        print('Tag list<br>')
        print('<table>')
        self.order = "id"
        if self.request.has_key("order"):
            self.order = self.request.getvalue("order")

        self.order_dir = "asc"
        if self.request.has_key("order_dir"):
            self.order_dir = self.request.getvalue("order_dir")
        
        if self.order_dir == "asc":
            next_order_dir = "desc"
        else:
            next_order_dir = "asc";
        tagobjs = [BlogTag(row) for row in self.db.getTagList(self.order, self.order_dir)]
        print('<thead>')
        print('<td><a href="?page=tags&order=id&order_dir=' + next_order_dir + '">#</a></td>')
        print('<td><a href="?page=tags&order=name&order_dir=' + next_order_dir + '">Title</a></td>')
        print('<td>Articles</td>')
        print('</thead>')
        for tag in tagobjs:
            print('<tr>')
            print('<td>' + str(tag.getId()) + '</td>')
            print('<td><a href="?page=tags&action=edit&dbid=' + str(tag.getId()) + '">' + tag.getName() + '</a></td>')
            print('<td>' + str(self.db.getArticleCountForTagId(tag.getId())) + '</td>')
            print('</tr>')
        print('</table>')


    def blog_tags_edit(self):
        print('<a href="?page=tags">Back</a><br>')
        print('<br>Tag edit ' + self.dbid + '<br>')
        if self.method == "POST" and self.request.has_key("tag_submit"):
            tag = BlogTag((
                int(self.dbid) if self.dbid != "new" else -1,
                self.request.getvalue("tag_name"),
                self.request.getvalue("tag_link")
            ))

            if self.request.getvalue("tag_submit") == "save":
                if self.dbid == "new":
                    #err = tag.insertDbEntry(self.db)
                    err = self.db.execute('insert into blog_tag(name, link) values(%s, %s)', (tag.getName(), tag.getRelativeLink()))
                else:
                    err = tag.updateDbEntry(self.db)

                if err is None:
                    print("Successfully saved!")
                    if self.dbid == "new":
                        self.dbid = self.db.lastrowid()
                        tag.fields['id'] = self.dbid
                else:
                    print("Error while writing to db: " + str(err))

        elif self.method == "GET" and self.dbid != "new":
            tag = self.db.getTagById(self.dbid)
            if tag is None:
                print("no such tag")
                return
            print("<h2>Edit</h2>")

        else:
            tag = BlogTag()
            print("<h2>New</h2>")

        print('<form method="POST" class="forms">')
        print('<section><label>Name</label>')
        print('<input type="text" name="tag_name" id="tag_name" size="50" value="' + tag.getName() + '">')
        print('</section>')
        print('<section><label>Link</label>')
        print('<input type="text" name="tag_link" id="tag_link" size="50" value="' + tag.getRelativeLink() + '">')
        print('</section>')
        print('<section>')
        print('<button type="primary" name="tag_submit" value="save">Save</button>')
        print('</section>')
        print('</form>')
        self.printTitleToLinkJs("tag_name", "tag_link")



    #
    #   PROJECTS
    #

    def show_projects(self):
        print('Projects<br>')
        print('<a href="uberuser.sg">Index</a><br>')

        if self.action == "list":
            self.projects_list()
        elif self.action == "edit" and self.dbid != "":
            self.projects_edit()
        else:
            self.show_error()

    def projects_list(self):
        print('<a href="?page=projects&action=edit&dbid=new">New Project</a><br><br>')
        print('<a href="?page=project_links&action=TODO">Project Links</a><br>')
        print('<br>Project list<br>')
        print('<table>')
        projects = [Project(row) for row in self.db.getProjects(published_only=False)]
        print('<thead>')
        print('<td>#</td>')
        print('<td>Project</td>')
        print('<td>Publ.</td>')
        print('</thead>')
        for project in projects:
            print('<tr>')
            print('<td>' + str(project.getId()) + '</td>')
            print('<td><a href="?page=projects&action=edit&dbid=%d">%s</a></td>' % (project.getId(), project.getName()))
            print('<td><i class="fa %s"></i></td>' % ("fa-check" if project.getPublished() else "fa-times-circle"))
            print('</tr>')
        print('</table>')


    def projects_edit(self):
        err = None
        dbaction = False

        if self.method == "POST" and self.request.has_key("set_start_page"):
            err = self.db.setProjectStartPage(self.dbid, self.request.getvalue("page_id"))
            dbaction = True

        if self.method == "POST" and self.request.has_key("project_submit"):
            blogtag_link = self.request.getvalue("project_blog_tag")
            if blogtag_link != "" and self.db.getTagByLink(blogtag_link) is None:
                blogtag = BlogTag((-1, self.linkToTitle(blogtag_link), self.titleToLink(blogtag_link)))
                blogtag.insertDbEntry(self.db)
                blogtag_link = blogtag.getRelativeLink()


            project = Project((
                int(self.dbid) if self.dbid != "new" else -1,
                self.request.getvalue("project_name"),
                self.request.getvalue("project_link"),
                self.request.getvalue("project_description"),
                self.request.getvalue("project_image"),
                self.request.getvalue("project_start_page") if self.request.getvalue("project_start_page") != "" else -1,
                blogtag_link,
                self.request.getvalue("project_github"),
                self.request.getvalue("project_hackaday"),
                self.request.getvalue("project_twitter"),
                0,
                (self.request.getvalue("project_published") == "on")
            ))

            pages = None
            links = None
            if self.dbid != "new":
                pages = [ProjectPage(row) for row in self.db.getProjectPages(self.dbid, published_only=False)]
                links = [ProjectLink(row) for row in self.db.getProjectLinks(project.getId())]


            if self.request.getvalue("project_submit") == "save":
                dbaction = True

                if self.dbid == "new":
                    err = project.insertDbEntry(self.db)
                else:
                    err = project.updateDbEntry(self.db)

                if err is None and self.dbid == "new":
                    self.dbid = self.db.lastrowid()
                    project.fields['id'] = self.dbid
                    err = self.project_create_start_page()

                if err is None:
                    (linknums, err) = self.saveProjectLinks(self.dbid)
                    if err is None and linknums > 0:
                        project.setHasOtherLinks(True)
                        project.updateDbEntry(self.db)

                if err is not None:
                    print("Error while writing to db: " + str(err))


        elif self.dbid != "new":
            project = self.db.getProjectById(int(self.dbid), published_only=False)
            if project is None:
                print("No such project")
                return

            pages = [ProjectPage(row) for row in self.db.getProjectPages(project.getId(), published_only=False)]
            links = [ProjectLink(row) for row in self.db.getProjectLinks(project.getId())]

        else:
            project = Project()
            pages = None
            links = None


        print('<a href="?page=projects">Back</a><br>')
        print('<a href="?page=project_pages&action=add&dbid=%s">New Page</a><br><br>' % (self.dbid))

        if dbaction:
            if err is None:
                print("successfully saved!")
            else:
                print("Error while writing to db: " + str(err))
                

        if pages is not None:
            self.project_list_pages(project, pages)


        print("""
<form method="POST" class="forms">
<input type="hidden" name="project_id" value="%s">

<section><label>Title</label>
<input type="text" name="project_name" id="project_name" size="50" value="%s">
</section>

<section><label>Link</label>
<input type="text" name="project_link" id="project_link" size="50" value="%s">
</section>

<section><label>Description</label>
<textarea name="project_description" rows="3" cols="80">
%s</textarea>
</section>

<section><label>Image</label>
%s
</section>

<section><label>Start Page</label>
<input type="text" name="project_start_page" size="5" value="%s">
</section>

<section><label>Blog Tag</label>
<input list="blogtag_list" name="project_blog_tag" value="%s">
</section>

<section><label>Github Repo</label>
https://github.com/sgreg/<input type="text" name="project_github" size="30" value="%s">
</section>

<section><label>Hackaday.io</label>
https://hackaday.io/project/<input type="text" name="project_hackaday" size="30" value="%s">
</section>

<section><label>Twitter Hashtag</label>
https://twitter.com/hashtag/<input type="text" name="project_twitter" size="30" value="%s">
</section>

<div id="otherlinks">
%s
</div>
<input type="button" value="Add Link" onClick="addProjectLink('otherlinks');">

<section><label class="checkbox">Published</label>
<input type="checkbox" name="project_published" %s/></section>
</section>

<button type="primary" name="project_submit" value="save">Save</button>

</form>
        """ % (
            self.dbid,
            project.getName(),
            project.getRelativeLink(),
            project.getDescription(),
            self.getImageSelectionList("project_image", project.getImage()),
            project.getStartPageId(),
            project.getBlogTag(),
            project.getGithub(),
            project.getHackaday(),
            project.getTwitter(),
            self.getProjectLinks(self.dbid),
            "checked" if project.getPublished() else ""
        ))
        self.printTitleToLinkJs("project_name", "project_link")
        self.printTagSelectionList()
        self.printProjectLinkAdder()

    def getProjectLinks(self, project_id):
        if project_id == "new":
            return

        links = [ProjectLink(row) for row in self.db.getProjectLinks(project_id)]
        ret = ""
        for link in links:
            linktype = self.db.getProjectLinkType(link.getLinkTypeId())
            ret += """
<div>
<input type="hidden" name="xlink_id" value="%s">
<input list="link_type" name="xlink_type" value="%s">
<input type="text" name="xlink_title" placeholder="title" value="%s">
<input type="text" name="xlink_url" placeholder="url" value="%s">
<input type="text" name="xlink_weight" placeholder="weight" size="3" value="%s">
</div>
            """ % (str(link.getId()), str(linktype.getName()), link.getTitle(), link.getUrl(), str(link.getWeight()))

        return ret

    def printProjectLinkAdder(self):
        print("""
<datalist id="link_type">
<option value="web">
<option value="oshpark">
<option value="youtube">
<option value="soundcloud">
</datalist>
""")
        print("""
<script type="text/javascript">
function addProjectLink(divName) {
      var newdiv = document.createElement('div');
      newdiv.innerHTML = '\
        <input type="hidden" name="xlink_id" value="-1">\
        <input list="link_type" name="xlink_type">\
        <input type="text" name="xlink_title" placeholder="title">\
        <input type="text" name="xlink_url" placeholder="url">\
        <input type="text" name="xlink_weight" placeholder="weight" size="3">';
      document.getElementById(divName).appendChild(newdiv);
}
</script>
    """)

    def saveProjectLinks(self, project_id):
        ids = self.request.getlist("xlink_id")
        types = self.request.getlist("xlink_type")
        titles = self.request.getlist("xlink_title")
        urls = self.request.getlist("xlink_url")
        weights = self.request.getlist("xlink_weight")

        for i in range(len(ids)):
            if urls[i] == "":
                # empty field, skip
                continue

            linkType = self.db.getProjectLinkTypeByName(types[i])
            link = ProjectLink((
                ids[i],
                project_id,
                linkType.getId(),
                titles[i],
                urls[i],
                weights[i]
            ))

            if ids[i] == "-1":
                err = link.insertDbEntry(self.db)
            else:
                err = link.updateDbEntry(self.db)

            if err is not None:
                return (0, err)

        return (len(ids), None)

    def project_list_pages(self, project, pages):
        print("Project %s with %d pages<br><br>" % (project.getName(), len(pages)))
        print('<table>')
        print('<thead>')
        print('<td>#</td>')
        print('<td>Page Name</td>')
        print('<td>Weight</td>')
        print('<td>Modified</td>')
        print('<td></td>')
        print('<td>Publ.</td>')
        print('</thead>')
        for page in pages:
            print('<tr>')
            print('<td>' + str(page.getId()) + '</td>')
            print('<td><a href="?page=project_pages&action=edit&dbid=%d">%s</a></td>' % (page.getId(), page.getTitle()))
            print('<td>' + str(page.getWeight()) + '</td>')
            print('<td>' + str(page.getModified()) + '</td>')
            print('<td>')
            if page.getId() == int(project.getStartPageId()):
                print("Start Page")
            else:
                print('<form method="POST" class="forms">')
                print('<input type="hidden" name="page_id" value="%s">' % (page.getId()))
                print('<button type="primary" name="set_start_page">Make start page</button>')
                print('</form>')
            print('</td>')
            print('<td><i class="fa %s"></i></td>' % ("fa-check" if page.getPublished() else "fa-times-circle"))
            print('</tr>')
        print('</table>')

        
    def project_create_start_page(self):
        page = ProjectPage((
            -1,
            self.dbid,
            "Overview",
            "overview",
            1,
            datetime.now().replace(microsecond=0),
            1,
            "No content yet",
            "No content yet"
        ))

        err = page.insertDbEntry(self.db)
        if err is None:
            page_id = self.db.lastrowid()
            print("<br>lastrowid %d<br>" % (page_id))
            err = self.db.setProjectStartPage(self.dbid, page_id)

        return err


    #
    #   PROJECT PAGES
    #

    def show_project_pages(self):
        if self.action == "edit":
            self.project_page_edit(project_id=None, page_id=self.dbid)
        elif self.action == "add":
            self.project_page_edit(project_id=self.dbid, page_id=None)
        else:
            self.show_error()

    # edit OR ADD project page.
    #
    #   - if project_id is None, the page with given page_id is edited
    #   - if project_id is not None, a page for the given project_id is added
    #
    def project_page_edit(self, project_id, page_id):
        err = None
        dbaction = False

        print('Project Page<br>')
        print('<a href="uberuser.sg">Index</a><br>')
        print('<a href="?page=projects">Projects</a><br>')

        if self.method == "POST" and self.request.has_key("page_submit"):
            page = ProjectPage((
                page_id if page_id is not None else -1,
                self.request.getvalue("page_project_id"),
                self.request.getvalue("page_title"),
                self.request.getvalue("page_link"),
                self.request.getvalue("page_weight"),
                self.request.getvalue("page_modified"),
                (self.request.getvalue("page_published") == "on"),
                self.request.getvalue("page_content"),
                ""
            ))

            page.setParsed(mistune.markdown(page.getContent(), escape=True))

            if self.request.getvalue("page_submit") == "save":
                if page.getModified() == "":
                    page.setModified(datetime.now().replace(microsecond=0))

                if page.getId() == -1:
                    err = page.insertDbEntry(self.db)
                else:
                    err = page.updateDbEntry(self.db)

                dbaction = True


        elif project_id is None and page_id is not None:
            page = self.db.getProjectPageById(page_id, published_only=False)
            if page is None:
                print("no such page")
                return

        elif project_id is not None:
            page = ProjectPage((-1, project_id, "", "", "", "", 0, "", ""))

        else:
            self.show_error()
            return


        project = self.db.getProjectById(page.getProjectId(), published_only=False)
        if project is None:
            print("no such project")
            return

        print('<a href="?page=projects&action=edit&dbid=%d">Back</a><br>' % (project.getId()))
        if project_id is None:
            print("<br>edit page %s of project %s<br>" % (page.getTitle(), project.getName()))
        else:
            print("<br>create new page for project %s<br>" % (project.getName()))
        

        if dbaction:
            if err is None:
                print("successfully saved!")
                if page.getId() == -1:
                    page.fields['id'] = self.db.lastrowid()
            else:
                print("Error while writing to db: " + str(err))
                


        print("""
<form method="POST" class="forms">
<input type="hidden" name="page_project_id" value="%s">

<section><label>Title</label>
<input type="text" name="page_title" id="page_title" size="50" value="%s">
</section>

<section><label>Link</label>
<input type="text" name="page_link" id="page_link" size="50" value="%s">
</section>

<section><label>Weight</label>
<input type="text" name="page_weight" size="5" value="%s">
</section>

<section><label>Modified</label>
<input type="text" name="page_modified" size="20" value="%s">
</section>

<section><label>Content</label>
<textarea name="page_content" rows="20" cols="80">
%s</textarea>
</section>

<section><label class="checkbox">Published</label>
<input type="checkbox" name="page_published" %s/></section>
</section>

<section>
<button type="primary" name="page_submit" value="preview">Preview</button>
<button type="primary" name="page_submit" value="save">Save</button>
</section>

</form>
        """ % (page.getProjectId(), page.getTitle(), page.getLink(), page.getWeight(), page.getModified(), page.getContent(), "checked" if page.getPublished() else ""))
        self.printTitleToLinkJs("page_title", "page_link")


    #
    #   STATIC
    #

    def show_static(self):
        print('Static<br>')
        print('<a href="uberuser.sg">Index</a><br>')
        if self.dbid == "":
            print('<br>')
            print('<a href="?page=static&dbid=about">About</a><br>')
            print('<a href="?page=static&dbid=contact">Contact</a><br>')
        elif self.dbid == "about" or self.dbid == "contact":
            self.static_edit()
        else:
            print("No such page")


    def static_edit(self):
        err = None
        dbaction = False

        print('<a href="?page=static">Back</a><br>')
        print('<br>%s<br>' % self.dbid)
        
        # preview
        if self.method == "POST" and self.request.has_key("page_submit"):
            page = StaticPage((
                self.request.getvalue("page_id"),
                self.request.getvalue("page_title"),
                self.request.getvalue("page_link"),
                self.request.getvalue("page_content"),
                ""
            ))

            page.setParsed(mistune.markdown(page.getContent(), escape=True))

            if self.request.getvalue("page_submit") == "save":
                dbaction = True
                err = page.updateDbEntry(self.db)

        else:
            page = self.db.getStaticPageByLink(self.dbid)

        if dbaction:
            if err is None:
                print("successfully saved!")
            else:
                print("Error while writing to db: " + str(err))

        print("PREVIEW")
        print(page.getParsed(), end='')

        print("""
<form method="POST" class="forms">
<input type="hidden" name="page_id" value="%s">
<input type="hidden" name="page_title" value="%s">
<input type="hidden" name="page_link" value="%s">

<section><label>Content</label>
<textarea name="page_content" rows="20" cols="80">
%s</textarea>
</section>

<section>
<button type="primary" name="page_submit" value="preview">Preview</button>
<button type="primary" name="page_submit" value="save">Save</button>
</section>

</form>
        """ % (page.getId(), page.getTitle(), page.getRelativeLink(), page.getContent()))




    #
    #   ERROR
    #

    def show_error(self):
        print("error")



    #
    #   UTILS
    #

    def titleToLink(self, title):
        return re.sub("[^a-z0-9 ]", "", title.lower()).replace(" ", "-")

    def linkToTitle(self, title):
        return title.replace("-", " ")

    def printTitleToLinkJs(self, source, dest):
        print("""
<script type="text/javascript">
var source_field = document.getElementById("%s");
function getLinkFromTitle() {
    var replaced = source_field.value.toLowerCase().replace(/[^a-z0-9 ]/g, "").replace(/ /g, "-");
    document.getElementById("%s").setAttribute("value", replaced.toLowerCase());
}
source_field.oninput = getLinkFromTitle;
</script>""" % (source, dest))

    def printInputFieldAdderJs(self):
        print("""
<script type="text/javascript">
function addInputField(divName, inputFieldName, datalist_name) {
      var newdiv = document.createElement('div');
      newdiv.innerHTML = "<input list='" + datalist_name + "' name='" + inputFieldName + "'>";
      document.getElementById(divName).appendChild(newdiv);
}
</script>
    """)

    def printTagSelectionList(self):
        s = '<datalist id="blogtag_list">'
        s += "\n".join('<option value="%s">' % link[0] for link in self.db.getTagLinkList())
        s += "</datalist>"
        print(s)

    def printCategorySelectionList(self):
        s = '<datalist id="blogcat_list">'
        s += "\n".join('<option value="%s">' % link[0] for link in self.db.getCategoryLinkList())
        s += "</datalist>"
        print(s)


    def printImageSelectionList(self, form_field_name, form_field_value=""):
        print(self.getImageSelectionList(form_field_name, form_field_value))

    def getImageSelectionList(self, form_field_name, form_field_value=""):
        s = """
<input list="image_files" name="%s" size="50" value="%s">
<datalist id="image_files"> """  % (form_field_name, form_field_value)

        files = glob("./images/*")
        filenames = [os.path.basename(f) for f in files]
        filenames.sort()

        s += "\n".join(['<option value="%s">' % (f) for f in filenames])
        s += "</datalist>"

        return s

