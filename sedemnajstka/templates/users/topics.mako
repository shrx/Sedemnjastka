<%inherit file="/base.mako" />
${c.topics.pager()}
<ul>
    % for topic in c.topics:
    <li><a href="${url('topic', id=topic.id)}">${topic.full_title()}</a></li>
    % endfor
</ul>
${c.topics.pager()}
