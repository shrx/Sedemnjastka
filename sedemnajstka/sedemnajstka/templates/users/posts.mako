<%inherit file="/base.mako" />
<h2>${c.title}</h2>
<div class="pager">
    ${c.posts.pager(format='Skok na stran $link_previous ~2~ $link_next',
                     separator=', ',
                     symbol_next='Naslednja',
                     symbol_previous=u'Prejsnja')}
</div>
<table class="posts">
    <thead>
        <tr>
            <th>Avtor</th>
            <th>Sporočilo</th>
        </tr>
    </thead>
    <tbody>
        % for i, (post, topic) in enumerate(c.posts):
        % if i % 2 == 0:
        <tr class="even">
        % else:
        <tr class="odd">
        % endif
            <td class="author">
                <p><strong><a href="${url('user', id=c.user.id)}" name="post-${post.id}" class="elita">${c.user.nick_name}</a></strong></p>
                <img src="http://www.joker.si/mn3njalnik/uploads//av-${c.user.id}.gif" />
                <img src="http://www.joker.si/mn3njalnik/uploads//av-${c.user.id}.jpg" />
                <img src="http://www.joker.si/mn3njalnik/uploads//av-${c.user.id}.png" />
                <p>Sporočil: ${c.user.num_of_posts}</p>
                <p><strong>Napisano:</strong></p>
                <p>${post.created_at}</p>
            </td>
            <td>
		<p><em><a href="${url('topic', id=topic.id)}#post-${post.id}">${topic.title}</a></em></p>
		${post.body}
	    </td>
        </tr>
        % if i % 2 == 0:
        <tr class="even">
        % else:
        <tr class="odd">
        % endif
            <td><a href="#top">Nazaj na vrh</a></td>
            <td>
                <a href="${url('user', id=c.user.id)}" class="profile"><img src="/images/icon_profile.gif" width="59" height="18" alt="profil" /></a>
                <a href="${url('quote_post', post=post.id)}" class="quote"><img src="/images/icon_quote.gif" width="59" height="18" alt="navedek" /></a>
            </td>
        </tr>
        % endfor
    </tbody>
</table>
<div class="pager">
    ${c.posts.pager(format='Skok na stran $link_previous ~2~ $link_next',
                     separator=', ',
                     symbol_next='Naslednja',
                     symbol_previous=u'Prejsnja')}
</div>
