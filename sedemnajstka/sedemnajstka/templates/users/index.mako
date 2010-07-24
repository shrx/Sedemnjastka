<%inherit file="/base.mako" />
<ul>
    % for user in c.users:
    <li><a href="${url('user', id=user.id)}">${user.nick_name}</a></li>
    % endfor
</ul>
