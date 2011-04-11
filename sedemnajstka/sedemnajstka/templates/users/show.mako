<%inherit file="/base.mako" />
<h2><a href="${url('user', id=c.user.id)}">${c.user.nick_name}</a></h2>
<h3>statistika</h3>
<div class="yello">
    <dl>
	<dt><strong>število postov:</strong></dt>
	<dd><a href="${url('user_posts', id=c.user.id)}">${c.user.num_of_posts}</a></dd>
	<dt><strong>število tem:</strong></dt>
	<dd><a href="${url('user_topics', id=c.user.id)}">${c.user.num_of_topics}</a></dd>
    </dl>
</div>
<h3>posti glede na dan tedna</h3>
<div class="yello">
    ${c.posts_per_dow.img()}\
</div>
<h3>posti glede na uro v dnevu</h3>
<div class="yello">
    ${c.posts_per_hour.img()}\
</div>
