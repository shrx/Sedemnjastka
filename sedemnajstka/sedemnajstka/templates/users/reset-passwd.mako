<%inherit file="/base.mako" />
<h3>${c.title}</h3>
<div class="yello">
    <p>S klikom na spodnji gumb bo v tvoj ZS predal odromal link, preko katerega
        boš lahko nastavil/a svoje novo geslo.</p>
    ${h.form(url('reset_passwd'))}
    <dl class="flat">
        <dt>tvoje uporabniško ime</dt>
        <dd>${h.text('nick_name', size=42)}</dd>
    </dl>
    <p>${h.submit('submit', 'Resetiraj geslo')}</p>
    ${h.end_form()}
</div>
