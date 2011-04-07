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
        % for i, (post, user) in enumerate(c.posts):
        % if i % 2 == 0:
        <tr class="even">
        % else:
        <tr class="odd">
        % endif
            <td class="author">
                <p><strong><a name="post-${post.id}">${user.nick_name}</a></strong></p>
                <img src="http://www.joker.si/mn3njalnik/uploads//av-${user.id}.gif" />
                <img src="http://www.joker.si/mn3njalnik/uploads//av-${user.id}.jpg" />
                <img src="http://www.joker.si/mn3njalnik/uploads//av-${user.id}.png" />
                <p>Sporočil: ${user.num_of_posts}</p>
                <p><strong>Napisano:</strong></p>
                <p>${post.created_at}</p>
            </td>
            <td>${post.body}</td>
        </tr>
        % if i % 2 == 0:
        <tr class="even">
        % else:
        <tr class="odd">
        % endif
            <td><a href="#top">Nazaj na vrh</a></td>
            <td>
                <a href="${url('user', id=user.id)}">
                    <img src="/images/icon_profile.gif" width="59" height="18" alt="profil" />
                </a>
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
