<%inherit file="/base.mako" />
<h3>${c.title}</h3>
<div class="yello">
    <p>Ola, uporabnik ${c.user.nick_name}, če je to tvoje pravo ime.</p>
    <p>V trenutku, ko boš kliknil na gumb, ki te čaka spodaj, boš imel ZS in v
    njem link preko katerega se boš lahko polastil svojega računa tukaj. To ti
    bo omogočilo koristenje nekaj naših bolj naprednih storitev, ki pa žal
    zahtevajo avtentikacijo.</p>
    <p>Nepridipravi, pozor! Skupaj z zgoraj omenjenim linkom bo v uporabnikov ZS
    predal odpotoval tudi IP naslov iz kjer se vrši ta zahteva.</p>
    ${h.form('claim', id=c.user.id)}
    <p>
        ${h.hidden('id', c.user.id)}
        ${h.submit('submit', u'Polasti se svojega računa zdaj!')}
    </p>
    ${h.end_form}
</div>
