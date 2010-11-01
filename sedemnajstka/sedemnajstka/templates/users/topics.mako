<%inherit file="/base.mako" />
${c.topics.pager()}
<table>
    % for i, topic in enumerate(c.topics):
    % if i % 2 == 0:
    <tr class="even">
    % else:
    <tr class="odd">
    % endif
        <td><a href="${url('topic', id=topic.id)}">${topic.full_title()}</a></td>
        <td><a href="${url('user', id=c.user.id)}">${c.user.nick_name}</a></td>
    </tr>
    % endfor
</table>
${c.topics.pager()}
