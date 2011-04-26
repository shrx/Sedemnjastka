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
                <p><strong>${h.link_to(c.quote.post.user.nick_name, url('user', id=c.quote.post.user.id), class_='elita')}</strong></p>
                <img src="${c.quote.post.user.avatar}" />
                <p>Sporočil: ${c.quote.post.user.num_of_posts}</p>
                <p><strong>Napisano:</strong></p>
                <p>${c.quote.post.created_at}</p>
            </td>
            <td>
                <p><em>${h.link_to(c.quote.post.topic.title, url('topic', id=c.quote.post.topic.id))}</em></p>
                ${c.quote.post.body}
                <br />
                <br />
                <iframe src="http://www.facebook.com/plugins/like.php?href=${'http://' + request.environ['HTTP_HOST'] + url('quote', id=c.quote.id) | u}&amp;send=false&amp;layout=standard&amp;width=450&amp;show_faces=false&amp;action=like&amp;colorscheme=light&amp;font=verdana&amp;height=35&amp;locale=sl_SI" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:450px; height:35px;" allowTransparency="true"></iframe>
            </td>
        </tr>
        <tr class="even">
            <td></td>
            <td>
                <a href="${url('user', id=c.quote.post.user.id)}" class="profile"><img src="/images/icon_profile.gif" width="59" height="18" alt="profil" /></a>
                <div class="votes">
                    % if 'user' in session and not c.quote.voted_by(session['user']):
                    ${h.link_to('+', url('quote_upvote', id=c.quote.id), class_='upvote')}
                    (${c.quote.upvotes - c.quote.downvotes})
                    ${h.link_to('-', url('quote_downvote', id=c.quote.id), class_='downvote')}
                    % else:
                    (${c.quote.upvotes - c.quote.downvotes})
                    % endif
                </div>
            </td>
        </tr>
    </tbody>
</table>
