<%inherit file="/base.mako" />
${c.topics.pager()}
<table>
    <% num = 0 %>
    % for topic, user in c.topics:
    % if num % 2 == 0:
    <tr class="even">
    % else:
    <tr class="odd">
    % endif
        <td><a href="${url('topic', id=topic.id)}">${topic.full_title()}</a></td>
        <td><a href="${url('user', id=user.id)}">${user.nick_name}</a></td>
    </tr>
    <% num += 1 %>
    % endfor
</table>
${c.topics.pager()}