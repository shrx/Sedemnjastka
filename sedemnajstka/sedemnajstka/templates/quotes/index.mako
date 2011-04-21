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
                <p><strong>${h.link_to(quote.post.user.nick_name, url('user', id=quote.post.user.id))}</strong></p>
                <img src="http://www.joker.si/mn3njalnik/uploads//av-${quote.post.user.id}.gif" />
                <img src="http://www.joker.si/mn3njalnik/uploads//av-${quote.post.user.id}.jpg" />
                <img src="http://www.joker.si/mn3njalnik/uploads//av-${quote.post.user.id}.png" />
                <p>Sporočil: ${quote.post.user.num_of_posts}</p>
                <p><strong>Napisano:</strong></p>
                <p>${quote.post.created_at}</p>
            </td>
            <td>
                <p><em>${h.link_to(quote.post.topic.title, url('topic', id=quote.post.topic.id))}</em></p>
                ${quote.post.body}
            </td>
        </tr>
        <tr class="even">
            <td>${h.link_to('Permalink', url('quote', id=quote.id))}</td>
            <td>
                <a href="${url('user', id=quote.post.user.id)}" class="profile"><img src="/images/icon_profile.gif" width="59" height="18" alt="profil" /></a>
                <div class="votes">
                    % if 'user' in session and not quote.voted_by(session['user']):
                    ${h.link_to('+', url('quote_upvote', id=quote.id), class_='upvote')}
                    (${quote.upvotes - quote.downvotes})
                    ${h.link_to('-', url('quote_downvote', id=quote.id), class_='downvote')}
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
