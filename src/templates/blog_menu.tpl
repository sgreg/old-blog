<div class="sidebox">
    <h1>Categories</h1>
    <ul class="no-list-style">
    #for @cat in @categories:
        <li><a href="@cat.getLink()"><i class="@cat.getImage()"></i>@cat.getName()</a></li>#end
    </ul>
</div>

<div class="sidebox">
    <h1>Tags</h1>
    <p class="sidebox-tags center">
    #for @tag in @tags:
        <a style="font-size:@{tag.getFontsize()}px;" href="@tag.getLink()">@tag.getName()</a>#end
    </p>
</div>

