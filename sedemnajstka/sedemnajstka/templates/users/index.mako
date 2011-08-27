<%inherit file="/base.mako" />
<h2>${c.title}</h2>
<table id="users-index">
    <thead>
        <tr>
            <th>Ime</th>
            <th>Sporočil</th>
        </tr>
    </thead>
    <tbody>
        % for user in c.users:
        <tr>
            <td>${h.link_to(user.nick_name, url('user', id=user.id), class_='elita')}</td>
            <td>${user.num_of_posts}</td>
        </tr>
        % endfor
    </tbody>
</table>
