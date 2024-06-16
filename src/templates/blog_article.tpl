<div class="blog-article">
    <h1 id="blog-article-headline" class="center">@article.getTitle()</h1>
    <p id="blog-article-timestamp" class="center"><i class="fa fa-calendar"></i>@article.getCreated()</p>
    <div class="blog-article-headimage center" style="background-image: url('/images/@article.getPreviewImage()')"></div>
    <div class="blog-article-content">
@article.getParsed()
    </div>
    <div class="blog-article-bottom">
        <p class="blog-article-bottom-title inline">Categories</p>
        <ul class="no-list-style inline">
        #for @cat in @categories:
            <li class="inline"><a href="@cat.getLink()"><i class="fa fa-@cat.getImage()"></i>@cat.getName()</a></li>#end
        </ul>
    </div>
    <div class="blog-article-bottom">
        <p class="blog-article-bottom-title inline">Tags</p>
        <ul class="no-list-style inline">
        #for @tag in @tags:
            <li class="inline"><a href="@tag.getLink()"><i class="fa fa-tag"></i>@tag.getName()</a></li>#end
        </ul>
    </div>
</div>
