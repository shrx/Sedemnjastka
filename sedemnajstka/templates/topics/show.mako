<%inherit file="/base.mako" />
<h1>${c.topic.full_title()}</h1>
${c.posts.pager()}
<ol>
    % for post in c.posts:
    <li>${post.body | n}</li>
    % endfor
</ol>
${c.posts.pager()}
