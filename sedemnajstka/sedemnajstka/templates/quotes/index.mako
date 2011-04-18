<%inherit file="/base.mako" />
<h2>${c.title}</h2>
% for quote in c.quotes:
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
                <p><strong><a href="${url('user', id=quote.post.user.id)}" name="post-${quote.post.id}" class="elita">${quote.post.user.nick_name}</a></strong></p>
                <img src="http://www.joker.si/mn3njalnik/uploads//av-${quote.post.user.id}.gif" />
                <img src="http://www.joker.si/mn3njalnik/uploads//av-${quote.post.user.id}.jpg" />
                <img src="http://www.joker.si/mn3njalnik/uploads//av-${quote.post.user.id}.png" />
                <p>Sporočil: ${quote.post.user.num_of_posts}</p>
                <p><strong>Napisano:</strong></p>
                <p>${quote.post.created_at}</p>
            </td>
            <td>
                <p><em><a href="${url('topic', id=quote.post.topic.id)}#post-${quote.post.id}">${quote.post.topic.title}</a></em></p>
                ${quote.post.body}
            </td>
        </tr>
        <tr class="even">
            <td><a href="${url('quote', id=quote.id)}">Permalink</a></td>
            <td>
                <a href="${url('user', id=quote.post.user.id)}" class="profile"><img src="/images/icon_profile.gif" width="59" height="18" alt="profil" /></a>
                <div class="votes">
                    % if 'user' in session and not quote.voted_by(session['user']):
                    <a href="${url('quote_upvote', id=quote.id)}" class="upvote">+</a>
                    (${quote.upvotes - quote.downvotes})
                    <a href="${url('quote_downvote', id=quote.id)}" class="downvote">-</a>
                    % else:
                    (${quote.upvotes - quote.downvotes})
                    % endif
                </div>
            </td>
        </tr>
    </tbody>
</table>
<br />
% endfor
