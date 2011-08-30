<%inherit file="/base.mako" />
<h2>${c.title}</h2>
<div class="pager">
    ${c.posts.pager(format='Skok na stran $link_previous ~2~ $link_next',
                     separator=', ',
                     symbol_next='Naslednja',
                     symbol_previous=u'Prejsnja')}
</div>
% for post, topic in c.posts:
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
                <p><strong>${h.link_to(h.literal(c.user.nick_name), url('user', id=c.user.id), class_='elita')}</strong></p>
                % if post.avatar:
                ${post.avatar.img()}
                % endif
                <p>Sporočil: ${c.user.num_of_posts}</p>
                <p><strong>Napisano:</strong></p>
                <p>${h.fdt(post.created_at)}</p>
            </td>
            <td>
                <p><em>${h.link_to(topic.title, url('topic', id=topic.id))}</em></p>
                ${post.body}
            </td>
        </tr>
        <tr class="even">
            <td><a href="#top">Nazaj na vrh</a></td>
            <td>
                <a href="${url('user', id=c.user.id)}" class="profile"><img src="/images/icon_profile.gif" width="59" height="18" alt="profil" /></a>
                <a href="${url('quote_post', post=post.id)}" class="quote"><img src="/images/icon_quote.gif" width="59" height="18" alt="navedek" /></a>
            </td>
        </tr>
    </tbody>
</table>
<br />
% endfor
<div class="pager">
    ${c.posts.pager(format='Skok na stran $link_previous ~2~ $link_next',
                     separator=', ',
                     symbol_next='Naslednja',
                     symbol_previous=u'Prejsnja')}
</div>
