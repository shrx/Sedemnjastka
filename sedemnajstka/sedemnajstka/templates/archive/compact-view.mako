<table class="topics compact-view">
    <thead>
        <tr>
            <th>Naslov</th>
            <th>#Odgovorov</th>
            <th>Avtor</th>
        </tr>
    </thead>
    <tbody>
        % for i, (topic, user) in enumerate(c.topics):
        <tr>
            <td class="title">
                % if 'user' in session:
                ${h.link_to(topic.full_title(), url('topic', id=topic.id), class_='topic-summary')}
                % else:
                ${h.link_to(topic.full_title(), url('topic', id=topic.id))}
                % endif
            </td>
            <td class="posts">${topic.num_of_posts}</td>
            <td class="author">${h.link_to(h.literal(user.nick_name), url('user', id=user.id), class_='elita')}</td>
        </tr>
        % endfor
    </tbody>
</table>
