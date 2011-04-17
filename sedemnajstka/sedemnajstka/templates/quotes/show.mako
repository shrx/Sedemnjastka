<%inherit file="/base.mako" />
<h2>${c.title}</h2>
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
                <p><strong><a href="${url('user', id=c.quote.post.user.id)}" name="post-${c.quote.post.id}" class="elita">${c.quote.post.user.nick_name}</a></strong></p>
                <img src="http://www.joker.si/mn3njalnik/uploads//av-${c.quote.post.user.id}.gif" />
                <img src="http://www.joker.si/mn3njalnik/uploads//av-${c.quote.post.user.id}.jpg" />
                <img src="http://www.joker.si/mn3njalnik/uploads//av-${c.quote.post.user.id}.png" />
                <p>Sporočil: ${c.quote.post.user.num_of_posts}</p>
                <p><strong>Napisano:</strong></p>
                <p>${c.quote.post.created_at}</p>
	    </td>
	    <td>
		<p><em><a href="${url('topic', id=c.quote.post.topic.id)}#post-${c.quote.post.id}">${c.quote.post.topic.title}</a></em></p>
                ${c.quote.post.body}
            </td>
        </tr>
        <tr class="even">
            <td></td>
            <td>
                <a href="${url('user', id=c.quote.post.user.id)}" class="profile"><img src="/images/icon_profile.gif" width="59" height="18" alt="profil" /></a>
                <div class="votes">
                    % if 'user' in session and not c.quote.voted_by(session['user']):
                    <a href="${url('quote_upvote', id=c.quote.id)}" class="upvote">+</a>
                    (${c.quote.upvotes - c.quote.downvotes})
                    <a href="${url('quote_downvote', id=c.quote.id)}" class="downvote">-</a>
                    % else:
                    (${c.quote.upvotes - c.quote.downvotes})
                    % endif
                </div>
            </td>
        </tr>
    </tbody>
</table>
