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
                <p><strong>${h.link_to(quote.post.user.nick_name, url('user', id=quote.post.user.id), class_='elita')}</strong></p>
                <img src="${quote.post.user.avatar}" />
                <p>Sporočil: ${quote.post.user.num_of_posts}</p>
                <p><strong>Napisano:</strong></p>
                <p>${quote.post.created_at}</p>
            </td>
            <td>
                <p><em>${h.link_to(quote.post.topic.title, url('topic', id=quote.post.topic.id))}</em></p>
                ${quote.post.body}
                <br />
                <br />
                <iframe src="http://www.facebook.com/plugins/like.php?href=${'http://' + request.environ['HTTP_HOST'] + url('quote', id=quote.id) | u}&amp;send=false&amp;layout=standard&amp;width=450&amp;show_faces=false&amp;action=like&amp;colorscheme=light&amp;font=verdana&amp;height=35&amp;locale=sl_SI" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:450px; height:35px;" allowTransparency="true"></iframe>
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
