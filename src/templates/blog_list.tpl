<div class="blog-preview-container">
#for @entry in @blog_entries:
    <div class="blog-preview-box flexbox flexrow">
    <a href="@entry.getLink()" class="blog-preview-link-box">
        <div class="blog-preview-image-box"><img src="/images/@{entry.getPreviewImage()}" class="blog-preview-image"></div></a>
        <div class="blog-preview-content">
            <h1 class="blog-preview-title"><a href="@entry.getLink()">@entry.getTitle()</a></h1>
            <p class="blog-preview-info">@entry.getCreated()</p>
            <p class="blog-preview-text justify">@entry.getPreview()</p>
        </div>
        #set @i = 1:
        #for @cat in @entry.getCategories():
        <div class="blog-preview-category blog-preview-category-@{i}"><i class="@cat.getImage()"></i><span><a href="@cat.getLink()">@cat.getNameNbsp()</a></span></div>
            #set @i = @i + 1:
        #end
    </div>
#end
</div>
