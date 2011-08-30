<%inherit file="/base.mako" />
<div class="pager">
    ${c.topics.pager(format='Skok na stran $link_previous ~2~ $link_next',
                     separator=', ',
                     symbol_next='Naslednja',
                     symbol_previous=u'Prejsnja')}
</div>
<table class="topics">
    <thead>
        <tr>
            <th>Teme</th>
            <th>Odgovori</th>
            <th>Avtor</th>
        </tr>
    </thead>
    <tbody>
        % for i, (topic, user) in enumerate(c.topics):
        <tr>
            <td class="title">${h.link_to(topic.full_title(), url('topic', id=topic.id))}</td>
            <td class="posts">${topic.num_of_posts}</td>
            <td class="author">${h.link_to(h.literal(user.nick_name), url('user', id=user.id), class_='elita')}</td>
        </tr>
        % endfor
    </tbody>
</table>
<div class="pager">
    ${c.topics.pager(format='Skok na stran $link_previous ~2~ $link_next',
                     separator=', ',
                     symbol_next='Naslednja',
                     symbol_previous=u'Prejsnja')}
</div>
