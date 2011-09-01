<%inherit file="/base.mako" />
<h3>${c.title}</h3>
<div class="yello">
    <div id="login-form">
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

    <div id="login-info">
        <ul>
            <li>Registriraš se lahko preko linka na svojemu profilu, ki ga najdeš
                ${h.link_to('tukaj', url('/users'))}.</li>
            <li>Pozabljeno geslo lahko ${h.link_to(u'resetiraš', url('reset_passwd'))}.</li>
        </ul>
    </div>
    <div class="clear"></div>
</div>
