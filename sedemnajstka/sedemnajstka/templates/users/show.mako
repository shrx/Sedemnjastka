<%inherit file="/base.mako" />
<div id="user-info">
    <div id="user-basic-info">
        <h2>${h.link_to(c.user.nick_name, url('user', id=c.user.id), class_='elita')}</h2>
        % if c.user.password == None:
        <p><em>${c.user.nick_name} se še ni polastil/a svojega računa. ${c.user.nick_name}, če si to ti,
                zakaj ne <a href="${url('claim', id=c.user.id)}">prevzameš svojega računa</a> zdaj.</em></p>
        % endif
    </div>
    <div id="user-avatar">
        % if c.user.avatar:
        ${c.user.avatar.img()}
        % endif
        <p>${h.link_to(u'prikaži celotno zgodovino avatarjev', url('user_avatars', id=c.user.id), id='load-avatar-history')}</p>
    </div>
</div>
<div class="clear"></div>
<div id="avatar-history">
</div>
<h3>statistika</h3>
<div class="yello">
    <dl>
        <dt>število postov</dt>
        <dd>${h.link_to(c.user.num_of_posts, url('user_posts', id=c.user.id))}</dd>
        <dt>število tem</dt>
        <dd>${h.link_to(c.user.num_of_topics, url('user_topics', id=c.user.id))}</dd>
        <dt>uganjenih avatarjev</dt>
        <dd><strong>${c.avatars_guessed}/${c.avatar_guesses_total} (${int((c.avatars_guessed / float(c.avatar_guesses_total)) * 100)}%)</strong></dd>
    </dl>
</div>
<h3>posti glede na dan tedna</h3>
<div class="yello">
    <div class="chart">
        <div id="ppdow-tabs">
	    <ul>
                <li>${h.link_to('Zadnji teden', url('user_chart_2', id=c.user.id, type='ppdow', limit=7))}</li>
                <li>${h.link_to('Zadnji trije meseci', url('user_chart_2', id=c.user.id, type='ppdow', limit=90))}</li>
                <li>${h.link_to('Zadnje pol leta', url('user_chart_2', id=c.user.id, type='ppdow', limit=180))}</li>
                <li>${h.link_to('Zadnje leto', url('user_chart_2', id=c.user.id, type='ppdow', limit=360))}</li>
                <li>${h.link_to('Vseskozi', url('user_chart_1', id=c.user.id, type='ppdow'))}</li>
	    </ul>
            <form action="">
                <p>
                    Omeji čas od
                    <input class="datepicker" name="ppdow-start-date" id="ppdow-start-date" />
                    do
                    <input class="datepicker" name="ppdow-end-date" id="ppdow-end-date" />
                    ${h.hidden('ppdow-user-id', c.user.id)}
                    <input type="submit" value="Poženi, Afriški Američan!" id="ppdow-do" />
                </p>
            </form>
        </div>
    </div>
</div>
<h3>posti glede na uro v dnevu</h3>
<div class="yello">
    <div class="chart">
        <div id="pph-tabs">
	    <ul>
                <li>${h.link_to('Zadnji teden', url('user_chart_2', id=c.user.id, type='pph', limit=7))}</li>
                <li>${h.link_to('Zadnji trije meseci', url('user_chart_2', id=c.user.id, type='pph', limit=90))}</li>
                <li>${h.link_to('Zadnje pol leta', url('user_chart_2', id=c.user.id, type='pph', limit=180))}</li>
                <li>${h.link_to('Zadnje leto', url('user_chart_2', id=c.user.id, type='pph', limit=360))}</li>
                <li>${h.link_to('Vseskozi', url('user_chart_1', id=c.user.id, type='pph'))}</li>
	    </ul>
            <form action="">
                <p>
                    Omeji čas od
                    <input class="datepicker" id="pph-start-date" />
                    do
                    <input class="datepicker" id="pph-end-date" />
                    ${h.hidden('pph-user-id', c.user.id)}
                    <input type="submit" value="Poženi, Afriški Američan!" id="pph-do" />
                </p>
            </form>
        </div>
    </div>
</div>
