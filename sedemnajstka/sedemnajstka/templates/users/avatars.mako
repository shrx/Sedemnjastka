<h3>zgodovina avatarjev</h3>
<div class="yello">
    <table>
        % for i, avatar in enumerate(c.user.avatars):
        % if (i + 1) % 2 == 0:
        <tr class="even">
        % else:
        <tr class="odd">
        % endif
            <td><span class="date">${h.fdt(avatar.created_at)}</span></td>
            <td>${avatar.img()}</td>
        </tr>
        % endfor
    </table>
</div>
