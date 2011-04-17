<%inherit file="/base.mako" />
<h3>${c.title}</h3>
<div class="yello">
    ${h.form(url('user_edit'))}
    <dl class="flat">
        <dt>trenutno geslo</dt>
        <dd>${h.password('cur_passwd')}</dd>
        <dt>novo geslo</dt>
        <dd>${h.password('new_passwd')}</dd>
        <dt>potrdi novo geslo</dt>
        <dd>${h.password('new_passwd_confirm')}</dd>
    </dl>
    <p>${h.submit('submit', 'Shrani')}</p>
    ${h.end_form}
</div>
