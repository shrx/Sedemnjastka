<%inherit file="/base.mako" />
<h3>dodaj navedek</h3>
<div class="yello">
    ${h.form('/quotes', method='PUT')}

    <table class="posts">
        <thead>
            <tr>
                <th>Avtor</th>
                <th>Sporočilo</th>
            </tr>
        </thead>
        <tbody>
            <tr class="even">
                <td class="author">
                    <p><strong>${h.link_to(c.post.user.nick_name, url('user', id=c.post.user.id), class_='elita')}</strong></p>
                    % if c.post.avatar:
                    ${c.post.avatar.img()}
                    % endif
                    <p>Sporočil: ${c.post.user.num_of_posts}</p>
                    <p><strong>Napisano:</strong></p>
                    <p>${h.fdt(c.post.created_at)}</p>
                </td>
                <td>${c.post.body}</td>
            </tr>
        </tbody>
    </table>

    <p>
        ${h.hidden('post', c.post.id)}
        ${h.submit('submit', 'Dodaj v bazo navedkov')}
    </p>

    ${h.end_form()}
</div>
