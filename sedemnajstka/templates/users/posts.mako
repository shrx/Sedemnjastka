<%inherit file="/base.mako" />
${c.posts.pager()}
<ol>
    % for post in c.posts:
    <li>${post.body | n}</li>
    % endfor
</ol>
${c.posts.pager()}
