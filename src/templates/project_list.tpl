
<div class="project-list-containeri flexbox flexrow">
#for @project in @projects:
<div class="project-list-box">
<a href="@project.getLink()">
    <div class="project-list-box-front center" style="background-image: url('/images/@project.getImage()');">
        <h1>@project.getName()</h1>
    </div>
    <div class="project-list-box-back center">
        <h1>@project.getName()</h1>
        <p class="project-list-text justify">@project.getDescription()</p>
    </div>
</a>
</div>
#end
</div>
