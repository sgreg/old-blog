import MySQLdb as mysql

from engine import config
from engine.model.blog_entry import BlogEntry
from engine.model.blog_comment import BlogComment
from engine.model.blog_category import BlogCategory
from engine.model.blog_tag import BlogTag
from engine.model.project import Project
from engine.model.project_page import ProjectPage
from engine.model.project_link import ProjectLink, ProjectLinkType
from engine.model.static import StaticPage

class Database(object):
    def __init__(self):
        self.db = mysql.connect(user='sgreg', passwd='sgreg', db='sgreg')
        self.cursor = self.db.cursor()

    #
    #   Common Database functions
    #

    def execute(self, sql_string, params):
        try:
            self.cursor.execute(sql_string, params)
            self.db.commit()
            return None
        except mysql.MySQLError as exc:
            return exc

    def lastrowid(self):
        return self.cursor.lastrowid

    def query(self, query_string, params=None):
        self.cursor.execute(query_string, params)
        return self.cursor.fetchall()

    def queryOne(self, query_string, params=None):
        self.cursor.execute(query_string, params)
        return self.cursor.fetchone()



    #
    #   Static page related functions
    #
    def getStaticPageByLink(self, link):
        result = self.queryOne("select * from static_page where link=%s", (link,))
        if result is not None:
            return StaticPage(result)
        return None



    #
    #   Blog related functions
    #

    def getFrontPageArticles(self):
        return self.getArticles(config.blog_entries_per_page, 0)

    def getAllArticles(self, order="id", order_dir="asc"):
        # NOTE needs "'...' % (..)" or it will quote order/order_desc and it won't work
        result = self.query("select * from blog_entry order by %s %s" % (order, order_dir))
        return result

    def getArticles(self, count, offset, published_only=True):
        result = self.query("select * from blog_entry %s order by created desc, id desc limit %s,%s" % ("where published=1" if published_only else "", offset, count))
        return result

    def getArticlesCount(self, published_only=True):
        result = self.queryOne("select count(id) from blog_entry %s" % ("where published=1" if published_only else ""))
        return result[0]

    def getArticleById(self, id):
        result = self.queryOne("select * from blog_entry where id=%s", (id,))
        if result is not None:
            return BlogEntry(result)
        return None

    def getArticleByLink(self, link):
        result = self.queryOne("select * from blog_entry where link=%s", (link,))
        if result is not None:
            return BlogEntry(result)
        return None

    def getArticlesByTagId(self, tagId, count, offset):
        query_string = """
            select blog_entry.* from blog_entry
                inner join blog_tag_map on 
                    blog_entry.id=blog_tag_map.blog_entry_id and
                    blog_tag_map.blog_tag_id=%%s
                    order by blog_entry.created desc, blog_entry.id desc limit %s,%s""" % (offset, count)
        
        result = self.query(query_string, (tagId,))
        return result
    

    def getArticlesByCategoryId(self, catId, count, offset):
        query_string = """
            select blog_entry.* from blog_entry
                inner join blog_category_map on 
                    blog_entry.id=blog_category_map.blog_entry_id and
                    blog_category_map.blog_category_id=%%s
                    order by blog_entry.created desc, blog_entry.id desc limit %s,%s""" % (offset, count)
        
        result = self.query(query_string, (catId,))
        return result

    def getNextArticle(self, created):
        result = self.queryOne("select * from blog_entry where created > %s order by created asc, id asc limit 1", (created, ))
        if result is not None:
            return BlogEntry(result)
        return None;

    def getPreviousArticle(self, created):
        result = self.queryOne("select * from blog_entry where created < %s order by created desc, id desc limit 1", (created, ))
        if result is not None:
            return BlogEntry(result)
        return None;

    def getCommentsCountForArticleId(self, article_id, publishedOnly=False):
        query = "select count(id) from blog_comment where blog_entry_id=%s"
        if publishedOnly:
            query += " and published=1"
        result = self.queryOne(query, (article_id,))
        return result[0]

    def getCommentsForArticleId(self, article_id, publishedOnly=False):
        query = "select * from blog_comment where blog_entry_id=%s"
        if publishedOnly:
            query += " and published=1"
        result = self.query(query, (article_id,))
        return result

    def getCommentById(self, comment_id):
        result = self.queryOne("select * from blog_comment where id=%s", (comment_id,))
        if result is not None:
            return BlogComment(result)
        return None

    def getCategoriesForArticleId(self, articleId):
        result = self.query("""
            select blog_category.* from blog_category
                inner join blog_category_map on 
                    blog_category.id=blog_category_map.blog_category_id and
                    blog_category_map.blog_entry_id=%s""", (articleId,))
        
        return result

    def getTagsForArticleId(self, articleId):
        result = self.query("""
            select blog_tag.* from blog_tag
                inner join blog_tag_map on 
                    blog_tag.id=blog_tag_map.blog_tag_id and
                    blog_tag_map.blog_entry_id=%s""", (articleId,))
        
        return result

    def getTagById(self, tag_id):
        result = self.queryOne("select * from blog_tag where id=%s", (tag_id,))
        if result is not None:
            return BlogTag(result)
        return None

    def getTagByName(self, tag_name):
        result = self.queryOne("select * from blog_tag where name=%s", (tag_name,))
        if result is not None:
            return BlogTag(result)
        return None

    def getTagByLink(self, tag_link):
        result = self.queryOne("select * from blog_tag where link=%s", (tag_link,))
        if result is not None:
            return BlogTag(result)
        return None

    def getTagList(self, order="name", order_dir="asc"):
        result = self.query("select * from blog_tag order by %s %s" % (order, order_dir))
        return result

    def getTagLinkList(self, order="name", order_dir="asc"):
        result = self.query("select link from blog_tag order by %s %s" % (order, order_dir))
        return result

    def getArticleCountForTagId(self, tag_id):
        result = self.queryOne("select count(id) from blog_tag_map where blog_tag_id=%s", (tag_id,))
        return result[0]

    def getTagListCount(self, sort_name=True, non_zero=True):
        result = self.query("""
            select blog_tag.*, count(blog_tag_map.blog_tag_id) as entries from blog_tag
            left join blog_tag_map on (blog_tag.id = blog_tag_map.blog_tag_id)
            group by blog_tag.id %s
            order by %s;
        """ % ("having(entries > 0)" if non_zero else "", "blog_tag.name asc" if sort_name else "entries desc"))
        return result


    def getCategoryById(self, category_id):
        result = self.queryOne("select * from blog_category where id=%s", (category_id,))
        if result is not None:
            return BlogCategory(result)
        return None

    def getCategoryByName(self, category_name):
        result = self.queryOne("select * from blog_category where name=%s", (category_name,))
        if result is not None:
            return BlogCategory(result)
        return None

    def getCategoryByLink(self, category_link):
        result = self.queryOne("select * from blog_category where link=%s", (category_link,))
        if result is not None:
            return BlogCategory(result)
        return None

    def getCategoryList(self, order="name", order_dir="asc"):
        #XXX query("", ()) will escape the order values and default order by id
        result = self.query("select * from blog_category order by %s %s" % (order, order_dir))
        return result

    def getCategoryLinkList(self, order="name", order_dir="asc"):
        result = self.query("select link from blog_category order by %s %s" % (order, order_dir))
        return result

    def getArticleCountForCategoryId(self, category_id):
        result = self.queryOne("select count(id) from blog_category_map where blog_category_id=%s", (category_id,))
        return result[0]

    

    #
    # Projects related functions
    #

    def getProjects(self, published_only=True):
        result = self.query("select * from project %s order by name" % ("where published=1" if published_only else ""))
        return result

    def getProjectById(self, project_id, published_only=True):
        result = self.queryOne("select * from project where " + ("published=1 and " if published_only else "") + "id=%s", (project_id,))
        if result is not None:
            return Project(result)
        return None

    def getProjectByLink(self, link, published_only=True):
        result = self.queryOne("select * from project where " + ("published=1 and " if published_only else "") + "link=%s", (link,))
        if result is not None:
            return Project(result)
        return None

    def getProjectStartPage(self, project_id):
        result = self.queryOne("select * from project_page where id=(select start_page from project where id=%s)", (project_id,))
        if result is not None:
            return ProjectPage(result)
        return None

    def setProjectStartPage(self, project_id, page_id):
        return self.execute('update project set start_page=%s where id=%s', (page_id, project_id))

    def getProjectPagesLinks(self, project_id, published_only=True):
        result = self.query("select id, project_id, title, link, weight, modified, published from project_page where " + ("published=1 and " if published_only else "") + "project_id=%s order by weight asc", (project_id,))
        return result

    def getProjectPages(self, project_id, published_only=True):
        result = self.query("select * from project_page where " + ("published=1 and " if published_only else "") + "project_id=%s order by weight asc", (project_id,))
        return result

    def getProjectLinks(self, project_id):
        result = self.query("select * from project_link where project_id=%s order by weight asc", (project_id,))
        return result

    def getProjectLinkType(self, link_type_id):
        result = self.queryOne("select * from project_link_type where id=%s", (link_type_id,))
        if result is not None:
            return ProjectLinkType(result)
        return None

    def getProjectLinkTypeByName(self, link_type_name):
        result = self.queryOne("select * from project_link_type where name=%s", (link_type_name,))
        if result is not None:
            return ProjectLinkType(result)
        return None

    def getProjectPageByLink(self, project_id, link, published_only=True):
        result = self.queryOne("select * from project_page where " + ("published=1 and " if published_only else "") + "project_id=%s and link=%s", (project_id, link))
        if result is not None:
            return ProjectPage(result)
        return None

    def getProjectPageById(self, page_id, published_only=True):
        result = self.queryOne("select * from project_page where " + ("published=1 and " if published_only else "") + "id=%s", (page_id, ))
        if result is not None:
            return ProjectPage(result)
        return None

database = None
def initialize():
    global database
    database = Database()

