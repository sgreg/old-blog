-- changed: news table added
USE sgreg;

DROP TABLE IF EXISTS static_page;
DROP TABLE IF EXISTS news;

DROP TABLE IF EXISTS blog_tag_map;
DROP TABLE IF EXISTS blog_category_map;

DROP TABLE IF EXISTS blog_comment;
DROP TABLE IF EXISTS blog_entry;
DROP TABLE IF EXISTS blog_tag;
DROP TABLE IF EXISTS blog_category;

DROP TABLE IF EXISTS project_link;
DROP TABLE IF EXISTS project_page;
DROP TABLE IF EXISTS project_type_map;
DROP TABLE IF EXISTS project_type;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS project_link_type;


CREATE TABLE static_page (
    id INT PRIMARY KEY UNIQUE NOT NULL,
    title VARCHAR(100) NOT NULL,
    link VARCHAR(100) NOT NULL,
    content TEXT,
    parsed TEXT
);

INSERT INTO static_page(id, title, link) VALUES(1, "About", "about");
INSERT INTO static_page(id, title, link) VALUES(2, "Contact", "contact");

CREATE TABLE news (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    content VARCHAR(100) NOT NULL,
    created DATETIME NOT NULL,
    published BOOLEAN DEFAULT 0
);

CREATE TABLE blog_entry (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    title VARCHAR(100) UNIQUE NOT NULL,
    link VARCHAR(100) UNIQUE NOT NULL,
    preview VARCHAR(255) DEFAULT "",
    preview_image VARCHAR(100) DEFAULT "",
    content TEXT NOT NULL,
    parsed TEXT NOT NULL,
    created DATETIME NOT NULL,
    published BOOLEAN default 1,
    indexed BOOLEAN default 1
);

CREATE TABLE blog_tag (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(64) UNIQUE NOT NULL,
    link VARCHAR(64) UNIQUE NOT NULL
);

CREATE TABLE blog_tag_map (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    blog_entry_id INT NOT NULL,
    blog_tag_id INT NOT NULL,
    FOREIGN KEY(blog_entry_id) REFERENCES blog_entry(id),
    FOREIGN KEY(blog_tag_id) REFERENCES blog_tag(id),
    CONSTRAINT tag_map UNIQUE(blog_entry_id, blog_tag_id)
);

CREATE TABLE blog_category (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(64) UNIQUE NOT NULL,
    link VARCHAR(64) UNIQUE NOT NULL,
    description VARCHAR(100),
    image VARCHAR(100)
);

CREATE TABLE blog_category_map (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    blog_entry_id INT NOT NULL,
    blog_category_id INT NOT NULL,
    FOREIGN KEY(blog_entry_id) REFERENCES blog_entry(id),
    FOREIGN KEY(blog_category_id) REFERENCES blog_category(id),
    CONSTRAINT category_map UNIQUE(blog_entry_id, blog_category_id)
);

CREATE TABLE blog_comment (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    blog_entry_id INT NOT NULL,
    author VARCHAR(64) NOT NULL,
    email VARCHAR(64),
    address VARCHAR(100),
    content TEXT NOT NULL,
    created DATETIME NOT NULL,
    is_chef BOOLEAN default 0,
    published BOOLEAN default 0,
    ip VARCHAR(50),
    useragent VARCHAR(100),
    referer VARCHAR(100),
    FOREIGN KEY(blog_entry_id) REFERENCES blog_entry(id)
);


CREATE TABLE project (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    link VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(200) NOT NULL,
    image VARCHAR(100) NOT NULL,
    start_page INT DEFAULT -1,
    blog_tag_link VARCHAR(100) DEFAULT "",
    github VARCHAR(100),
    hackaday VARCHAR(100),
    twitter VARCHAR(100),
    other_links BOOLEAN DEFAULT 0, -- xxx or just check the db for links
    published BOOLEAN DEFAULT 0,
    CONSTRAINT UNIQUE(link)
);

CREATE TABLE project_type (
    id INT PRIMARY KEY UNIQUE NOT NULL,
    name VARCHAR(50),
    icon_type VARCHAR(10),
    icon VARCHAR(100)
);

INSERT INTO project_type(id, name, icon_type, icon) VALUES(1, "Software", "svg", "software");
INSERT INTO project_type(id, name, icon_type, icon) VALUES(2, "Hardware", "svg", "hardware");
INSERT INTO project_type(id, name, icon_type, icon) VALUES(3, "Firmware", "svg", "firmware");
INSERT INTO project_type(id, name, icon_type, icon) VALUES(4, "App", "fa", "tablet");
INSERT INTO project_type(id, name, icon_type, icon) VALUES(5, "Mechanics", "fa", "wrench");
INSERT INTO project_type(id, name, icon_type, icon) VALUES(6, "Webservice", "fa", "wifi");

CREATE TABLE project_type_map (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    project_id INT NOT NULL,
    project_type_id INT NOT NULL,
    FOREIGN KEY(project_id) REFERENCES project(id),
    FOREIGN KEY(project_type_id) REFERENCES project_type(id),
    CONSTRAINT UNIQUE(project_id, project_type_id)
);

CREATE TABLE project_page (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    project_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    link VARCHAR(100) NOT NULL,
    weight INT NOT NULL DEFAULT 99,
    modified DATETIME NOT NULL,
    published BOOLEAN DEFAULT 0,
    content TEXT NOT NULL,
    parsed TEXT NOT NULL,
    FOREIGN KEY(project_id) REFERENCES project(id),
    CONSTRAINT project_link UNIQUE(project_id, link)
);

CREATE TABLE project_link_type (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
    icon_type VARCHAR(10),
    icon VARCHAR(100)
);

INSERT INTO project_link_type(id, name, icon_type, icon) VALUES(1, "web", "fa", "globe");
INSERT INTO project_link_type(id, name, icon_type, icon) VALUES(2, "oshpark", "fa", "gear");
INSERT INTO project_link_type(id, name, icon_type, icon) VALUES(3, "youtube", "fa", "youtube-play");
INSERT INTO project_link_type(id, name, icon_type, icon) VALUES(4, "soundcloud", "fa", "soundcloud");

CREATE TABLE project_link (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    project_id INT NOT NULL,
    link_type_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    url VARCHAR(200) NOT NULL,
    weight INT NOT NULL DEFAULT 99,
    FOREIGN KEY(project_id) REFERENCES project(id),
    FOREIGN KEY(link_type_id) REFERENCES project_link_type(id)
);

