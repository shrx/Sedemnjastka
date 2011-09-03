<table class="topics full-view">
    <thead>
        <tr>
            <th></th>
            <th>Naslov</th>
            <th>#Odgovorov</th>
            <th>Avtor</th>
        </tr>
    </thead>
    <tbody>
        % for i, (topic, user) in enumerate(c.topics):
        <tr>
            <td class="avatar">
                % if user.avatar:
                ${user.avatar.img()}
                % else:
                <img src="/images/no-avatar.png" width="64" height="54" />
                % endif
            </td>
            <td class="title">
                ${h.link_to(topic.full_title(), url('topic', id=topic.id))}
                <p class="date">${h.fdt(topic.last_post_created_at)}</p>
            </td>
            <td class="posts">${topic.num_of_posts}</td>
            <td class="author">${h.link_to(h.literal(user.nick_name), url('user', id=user.id), class_='elita')}</td>
        </tr>
        % endfor
    </tbody>
</table>
