<ul class="no-list-style">
    #set @prev_page = @current_page - 1:
    #set @next_page = @current_page + 1:
    #if(@current_page == 1) <li class="disabled">&lt;</li>
    #else <li><a href="@base_link@prev_page">&lt;</a></li>
    #end

    #for @page in @pages:
    #if(@page == @current_page) <li class="selected">@page</li>
    #else <li><a href="@base_link@page">@page</a></li>
    #end
    #end

    #if(@current_page == @page_count) <li class="disabled">&gt;</li>
    #else <li><a href="@base_link@next_page">&gt;</a></li>
    #end
</ul>

