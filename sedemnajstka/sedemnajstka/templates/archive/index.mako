<%inherit file="/base.mako" />
<div class="date-range-controller">
    ${h.form('/archive', method='GET', id_='date-range-form')}
    <p>
        Prikaži teme od
        ${h.text('from', size=10, value=c.from_.strftime('%d.%m.%Y'), class_='datepicker')}
        do
        ${h.text('to', size=10, value=c.to.strftime('%d.%m.%Y'), class_='datepicker')}
        ${h.submit(None, u'Poženi, schatz!')}
    </p>
    ${h.end_form()}
</div>
<div id="date-range"></div>
<div id="archive-view-controller">
    <div id="archive-limit">
        ${h.form(None)}
        <p>
            Prikaži
            ${h.select('archive_limit', c.limit, options=[('10', '10'), ('25', '25'), ('50', '50')])}
            zapisov
        </p>
        ${h.end_form()}
    </div>
    <div id="archive-view">
        ${h.form(None)}
        <div id="archive-view-radio">
            ${h.radio('archive_view', 'compact', id='compact-view', checked=c.view=='compact')}
            <label for="compact-view">Compact</label>
            ${h.radio('archive_view', 'full', id='full-view', checked=c.view=='full')}
            <label for="full-view">Full</label>
        </div>
        ${h.end_form()}
    </div>
    <div class="clear"></div>
</div>
% if c.view == 'compact':
<%include file='compact-view.mako' />
% elif c.view == 'full':
<%include file='full-view.mako' />
% endif
<div class="pager">
    ${c.topics.pager(format='Skok na stran $link_previous ~2~ $link_next',
                     separator=', ',
                     symbol_next='Naslednja',
                     symbol_previous=u'Prejsnja')}
</div>
