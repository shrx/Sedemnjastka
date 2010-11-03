<%inherit file="/base.mako" />
${c.posts.pager()}
<ol>
    % for i, (post, topic) in enumerate(c.posts):
    % if i % 2 == 0:
    <li class="even">
    % else:
    <li class="odd">
    % endif
        <h2><a href="${url('user', id=c.user.id)}">${c.user.nick_name}</a></h2>
        <p class="meta"><em>@ ${post.created_at},
        v: <a href="${url('topic', id=topic.id)}#post-${post.id}">${topic.title}</a></em></p>
        <p>${post.body}</p>
    </li>
    % endfor
</ol>
${c.posts.pager()}
