<%inherit file="/base.mako" />
<h2>${c.title}</h2>
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
        </tr>
    </thead>
    <tbody>
        % for i, topic in enumerate(c.topics):
        <tr>
            <td class="title">${h.link_to(topic.full_title(), url('topic', id=topic.id))}</td>
            <td class="posts">${topic.num_of_posts}</td>
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
