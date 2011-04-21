<%inherit file="/base.mako" />
<table>
    <thead>
        <tr>
            <th>Ime</th>
            <th>Sporočil</th>
        </tr>
    </thead>
    <tbody>
        % for i, user in enumerate(c.users):
        % if i % 2 == 0:
        <tr class="even">
            % else:
        <tr class="odd">
            % endif
            <td>${h.link_to(user.nick_name, url('user', id=user.id), class_='elita')}</td>
            <td>${user.num_of_posts}</td>
        </tr>
        % endfor
    </tbody>
</table>
