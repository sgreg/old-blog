<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <title>@meta.page_title</title>
        <meta name="description" content="@meta.description">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" href="/favicon.png">
        <link rel="apple-touch-icon" href="/apple-touch-icon.png">
        <link rel="canonical" href="@meta.url">
        <meta name="twitter:card" content="summary">
        <meta name="twitter:site" content="\@anotherSven">
        <meta name="twitter:title" content="@meta.title">
        <meta name="twitter:description" content="@meta.description">
        <meta name="twitter:image" content="@meta.image">
        <meta property="og:type" content="@meta.type">
        <meta property="og:url" content="@meta.url">
        <meta property="og:title" content="@meta.title">
        <meta property="og:image" content="@meta.image">
        <meta property="og:description" content="@meta.description">
        <meta property="og:site_name" content="sgreg.fi">
        <link rel="stylesheet" href="/css/normalize.css">
        <link rel="stylesheet" href="/css/font-awesome.min.css">
        <link rel="stylesheet" href="/css/font-sgreg.css">
        <link rel="stylesheet" href="/css/prism-sgreg.css">
        <link rel="stylesheet" href="/css/sgreg-1.0.6.css">
    </head>
    <body>
    
<div class="page-container flexbox flexrow">
    <div class="head-container flexbox flexrow">
        #if(@has_logo)
        <div class="head-logo flexbox">
            <p id="head-logo-title"><b>sgreg</b>.fi</p>
        </div>
        #end
        <div class="head-right-container">
            <div class="head-right-navi">
                <ul class="paginate">
                    <li#if(@info.selected == "") class="selected"#end><a href="/"><i class="fa fa-home"></i>Home</a></li>
                    <li#if(@info.selected == "blog") class="selected"#end><a href="/blog/"><i class="fa fa-pencil"></i>Blog</a></li>
                    <li#if(@info.selected == "projects") class="selected"#end><a href="/projects/"><i class="fa fa-flask"></i>Projects</a></li>
                    <li#if(@info.selected == "about") class="selected"#end><a href="/about/"><i class="fa fa-user"></i>About</a></li>
                </ul>
            </div>
            #if(@has_subtitle)
            <div class="head-right-title center">#if(@info.location_icon != "")<i class="fa fa-@info.location_icon"></i>#end@info.location</div>
            #end
        </div>
    </div>


    #if (@has_pager_bar)
    <div class="pager-bar center">
    @pager_bar
    </div>
    #end
    #if (@has_pager_space)
    <div class="pager-space"></div>
    #end
    
    <div class="main">
    @content
    </div>
    
    #if (@has_menu)
    <div class="main-menu">
        @menu
    </div>
    #end

    #if (@has_pager_bar)
    <div class="pager-bar pager-bar-bottom center">
    @pager_bar
    </div>
    #end
    <div class="footer flexbox flexrow">
    #if (@has_footer)
        <div class="footer-logo"></div>
        <div class="footer-links">
            <ul class="no-list-style">
                <li><a href="/" class="footer-link">Home</a></li>
                <li><a href="/blog/" class="footer-link">Blog</a></li>
                <li><a href="/projects/" class="footer-link">Projects</a></li>
                <li><a href="/about/" class="footer-link">About</a></li>
            </ul>
        </div>
    #end
        <div class="footer-follow flexbox flexrow">
            <ul class="no-list-style">
                <li class="inline"><a href="https://github.com/sgreg" target="_blank" title="Github" class="footer-link link-github"><i class="fa fa-github fa-2x"></i></a></li>
                <li class="inline"><a href="https://reddit.com/user/anotherSven/" target="_blank" title="Reddit" class="footer-link link-reddit"><i class="fa fa-reddit fa-2x"></i></a></li>
                <li class="inline"><a href="https://hackaday.io/sgreg" target="_blank" title="Hackaday.io" class="footer-link link-hackaday"><i class="fsg fsg-hackaday fsg-2x"></i></a></li>
                <li class="inline"><a href="https://twitter.com/anotherSven" target="_blank" title="Twitter" class="footer-link link-twitter"><i class="fa fa-twitter fa-2x"></i></a></li>
                <li class="inline"><a href="https://oshpark.com/profiles/sgreg" target="_blank" title="OSH Park" class="footer-link link-oshpark"><i class="fsg fsg-oshpark fsg-2x"></i></a></li>
                <li class="inline"><a href="https://soundcloud.com/anothersven" target="_blank" title="SoundCloud" class="footer-link link-soundcloud"><i class="fa fa-soundcloud fa-2x"></i></a></li>
                <li class="inline"><a href="https://youtube.com/channel/UCjL9Zkd7WKy825iUPQ27Iaw" target="_blank" title="YouTube" class="footer-link link-youtube"><i class="fa fa-youtube-play fa-2x"></i></a></li>
                <li class="inline"><a href="https://fi.linkedin.com/in/svengregori" target="_blank" title="LinkedIn" class="footer-link link-linkedin"><i class="fa fa-linkedin-square fa-2x"></i></a></li>
            </ul>
        </div>
    </div>
    <div class="copyright center">
<span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">sgreg.fi</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Sven Gregori</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/" target="_blank">Creative Commons Attribution 4.0 International License</a>.
    </div>
</div>
    <script src="/js/prism.js"></script>
    </body>
</html>

