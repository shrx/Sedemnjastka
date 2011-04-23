<%inherit file="/base.mako" />
<h2>${h.link_to(c.user.nick_name, url('user', id=c.user.id), class_='elita')}</h2>
% if c.user.password == None:
<p><em>${c.user.nick_name} se še ni polastil/a svojega računa. ${c.user.nick_name}, če si to ti,
zakaj ne <a href="${url('claim', id=c.user.id)}">prevzameš svojega računa</a> zdaj.</em></p>
% endif
<h3>statistika</h3>
<div class="yello">
    <dl>
        <dt>število postov</dt>
        <dd>${h.link_to(c.user.num_of_posts, url('user_posts', id=c.user.id))}</dd>
        <dt>število tem</dt>
        <dd>${h.link_to(c.user.num_of_topics, url('user_topics', id=c.user.id))}</dd>
    </dl>
</div>
<h3>posti glede na dan tedna</h3>
<div class="yello">
    <div class="chart">
        ${c.posts_per_dow.img()}
        ${h.form(url('user', id=c.user.id))}
        <p>
            Omeji čas od
            ${h.select('ppdow_start_month', c.ppdow_start_month, c.months)}
            ${h.select('ppdow_start_year', c.ppdow_start_year, c.years)}
            do
            ${h.select('ppdow_end_month', c.ppdow_end_month, c.months)}
            ${h.select('ppdow_end_year', c.ppdow_end_year, c.years)}
            ${h.submit('submit', u'Osveži, Polde!')}
        </p>
        ${h.end_form}
    </div>
</div>
<h3>posti glede na uro v dnevu</h3>
<div class="yello">
    <div class="chart">
        ${c.posts_per_hour.img()}
        ${h.form(url('user', id=c.user.id))}
        <p>
            Omeji čas od
            ${h.select('pph_start_month', c.pph_start_month, c.months)}
            ${h.select('pph_start_year', c.pph_start_year, c.years)}
            do
            ${h.select('pph_end_month', c.pph_end_month, c.months)}
            ${h.select('pph_end_year', c.pph_end_year, c.years)}
            ${h.submit('submit', u'Osveži, Polde!')}
        </p>
        ${h.end_form}
    </div>
</div>
