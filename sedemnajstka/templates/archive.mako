${c.topics.pager()}
<table>
    % for topic, user in c.topics:
    <tr>
        <td><a href="${url('topic', id=topic.id)}">${topic.full_title()}</a></td>
        <td><a href="${url('user', id=user.id)}">${user.nick_name}</a></td>
    </tr>
    % endfor
</table>
${c.topics.pager()}
