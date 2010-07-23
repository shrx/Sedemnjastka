<%inherit file="/base.mako" />
${c.posts.pager()}
<ol>
    <% num = 0 %>
    % for post in c.posts:
    % if num % 2 == 0:
    <li class="even">
    % else:
    <li class="odd">
    % endif
        <h2><a href="${url('user', id=c.user.id)}">${c.user.nick_name}</a></h2>
        <p class="meta"><em>${post.created_at}</em></p>
        <p>${post.body}</p>
    </li>
    % endfor
</ol>
${c.posts.pager()}
