<%inherit file="/base.mako" />
<h3>${c.title}</h3>
<div class="yello">
    <div id="guess-avatar" class="ga-choice">
        <%include file="/guess-avatar/choice.mako" />
    </div>
    <div id="avatar-history">
        <table id="guessing-history">
            % for i, ag in enumerate(c.avatar_guesses):
            % if i % 2 == 0:
            <tr class="even">
                % else:
            <tr class="odd">
                % endif
                <td><span class="date">${h.fdt(ag.created_at)}</span></td>
                <td>${ag.guessed_avatar_.img()}</td>
                <td>
                    % if ag.guessed:
                    <span class="correct-guess">&#x2714;</span>
                    % else:
                    <span class="wrong-guess">&#x2718;</span>
                    % endif
                </td>
            </tr>
            % endfor
        </table>
    </div>
</div>
