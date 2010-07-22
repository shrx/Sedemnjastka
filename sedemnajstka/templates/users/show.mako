<%inherit file="/base.mako" />
<h1>${c.user.nick_name}</h1>
<dl>
    <dt>stevilo postov:</dt>
    <dd>${c.user.num_of_posts}</dt>
    <dt>stevilo tem:</dt>
    <dd><a href="${url('user_topics', id=c.user.id)}">${c.user.num_of_topics}</a></dt>
</dl>
