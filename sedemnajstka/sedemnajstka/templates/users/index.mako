<%inherit file="/base.mako" />
<table>
    <thead>
	<tr>
	    <th>Ime</th>
	    <th>Sporočil</th>
	</tr>
    </thead>
    <tbody>
	% for i, user in enumerate(c.users):
	% if i % 2 == 0:
	<tr class="even">
	    % else:
	<tr class="odd">
	    % endif
            <td><a href="${url('user', id=user.id)}">${user.nick_name}</a></td>
	    <td>${user.num_of_posts}</td>
	</tr>
	% endfor
    </tbody>
</table>
