<div class="sidebox">
    <h1>Table of Contents</h1>
    <ul class="no-list-style">
    #for @page in @pages:
        <li><a href="@project.getLink()/@page.getLink()">@page.getTitle()</a></li>#end
    </ul>
</div>

<div class="sidebox">
    <h1>Project Links</h1>
    <ul class="no-list-style">
#if(@project.hasBlogTag())
        <li><a href="/blog/tag/@project.getBlogTag()"><i class="fa fa-tag"></i>Related Blog articles</a></li>
#end
#if(@project.hasLinks())
    #if(@project.hasGithub())
        <li><a href="@project.getGithubLink()" target="_blank" class="link-github"><i class="fa fa-github"></i>Github repository</a></li>
    #end
    #if(@project.hasHackaday())
        <li><a href="@project.getHackadayLink()" target="_blank" class="link-hackaday"><i class="fsg fsg-hackaday"></i>Hackaday.io project page</a></li>
    #end
    #if(@project.hasTwitter())
        <li><a href="@project.getTwitterLink()" target="_blank" class="link-twitter"><i class="fa fa-twitter"></i>\#@project.getTwitter() </a></li>
    #end
#for @link in @links:
        <li><a href="@link.getUrl()" target="_blank" class="@link.getLinkClass()">@link.getIcon()@link.getTitle()</a>
#end
#else
        <li>No Links</li>
#end
    </ul>
</div>
