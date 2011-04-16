<%inherit file="/base.mako" />
<h3>${c.title}</h3>
<div class="yello">
    ${h.form(url('passwd', token=c.user.token))}
    <dl class="flat">
        <dt>geslo</dt>
        <dd>${h.password('passwd')}</dd>
        <dt>potrdi geslo</dt>
        <dd>${h.password('passwd_confirm')}</dd>
    </dl>
    <p>${h.submit('submit', u'Nastavi geslo in se polasti svojega računa')}</p>
    ${h.end_form}
</div>
