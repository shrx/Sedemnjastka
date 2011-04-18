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
                    <p><strong><a href="${url('user', id=c.post.user.id)}" name="post-${c.post.id}" class="elita">${c.post.user.nick_name}</a></strong></p>
                    <img src="http://www.joker.si/mn3njalnik/uploads//av-${c.post.user.id}.gif" />
                    <img src="http://www.joker.si/mn3njalnik/uploads//av-${c.post.user.id}.jpg" />
                    <img src="http://www.joker.si/mn3njalnik/uploads//av-${c.post.user.id}.png" />
                    <p>Sporočil: ${c.post.user.num_of_posts}</p>
                    <p><strong>Napisano:</strong></p>
                    <p>${c.post.created_at}</p>
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
