<p>
    ${c.one.avatar.img()}
</p>
${h.form('/games/guess-avatar/guessed', id="ga-form")}
<ul>
    % for user in c.users:
    <li>
        <button class="guess" value="${user.id}" name="user_id">
            ${user.nick_name}
        </button>
    </li>
    % endfor
</ul>
${h.hidden('avatar_id', value=c.one.avatar.id)}
${h.end_form()}
