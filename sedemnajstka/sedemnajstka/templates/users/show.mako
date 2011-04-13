<%inherit file="/base.mako" />
<h2><a href="${url('user', id=c.user.id)}" class="elita">${c.user.nick_name}</a></h2>
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
    ${c.posts_per_dow.img()}
    <div class="chart_ctrl">
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
    ${c.posts_per_hour.img()}
    <div class="chart_ctrl">
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
