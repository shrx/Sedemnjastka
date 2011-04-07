<%inherit file="/base.mako" />
<h2>${c.user.nick_name}</h2>
<table>
    <thead>
	<tr>
	    <th>število postov</th>
	    <th>število tem</th>
	</tr>
    </thead>
    <tbody>
	<tr class="odd">
	    <td><a href="${url('user_posts', id=c.user.id)}">${c.user.num_of_posts}</a></td>
	    <td><a href="${url('user_topics', id=c.user.id)}">${c.user.num_of_topics}</a></td>
	</tr>
    </tbody>
</table>
