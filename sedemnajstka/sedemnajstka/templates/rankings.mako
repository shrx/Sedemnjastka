<%inherit file="/base.mako" />
<h3>poste radi pišejo:</h3>
<table>
    % for i, user in enumerate(c.users_by_posts):
    % if i % 2 == 0:
    <tr class="even">
    % else:
    <tr class="odd">
    % endif
        <td>${i + 1}</td>
        <td>${h.link_to(user.nick_name, url('user', id=user.id), class_='elita')}</td>
        <td>${user.num_of_posts}</td>
    </tr>
    % endfor
</table>
<h3>teme radi odpirajo:</h3>
<table>
    % for i, user in enumerate(c.users_by_topics):
    % if i % 2 == 0:
    <tr class="even">
    % else:
    <tr class="odd">
    % endif
        <td>${i + 1}</td>
        <td>${h.link_to(user.nick_name, url('user', id=user.id), class_='elita')}</td>
        <td>${user.num_of_topics}</td>
    </tr>
    % endfor
</table>
