<%inherit file="/base.mako" />
<h3>${c.title}</h3>
<div class="yello">
    ${h.form('/login')}
    <dl class="flat">
        <dt>uporabniško ime</dt>
        <dd>${h.text('nick_name', size=42)}</dd>
        <dt>geslo</dt>
        <dd>${h.password('password', size=42)}</dd>
    </dl>
    <p>${h.submit('submit', 'Prijavi me')}</p>
    ${h.end_form()}
</div>
