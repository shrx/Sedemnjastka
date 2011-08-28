<tr>
    <td><span class="date">${h.fdt(c.avatar_guess.created_at)}</span></td>
    <td>${c.avatar_guess.guessed_avatar_.img()}</td>
    <td>
        % if c.avatar_guess.guessed:
        <span class="correct-guess">&#x2714;</span>
        % else:
        <span class="wrong-guess">&#x2718;</span>
        % endif
    </td>
</tr>
