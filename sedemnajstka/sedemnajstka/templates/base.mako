<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
        <link href="/favicon.png" rel="icon" type="image/png" />
        <link href="/css/style.css" rel="stylesheet" type="text/css" />
        <link href="/css/demo_page.css" rel="stylesheet" type="text/css" />
        <link href="/css/demo_table_jui.css" rel="stylesheet" type="text/css" />
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/themes/sunny/jquery-ui.css" rel="stylesheet" type="text/css" />
        <script src="https://www.google.com/jsapi?key=ABQIAAAAIiJO64nS9X44-5zAPRx_CBQ2dbh21h_ChSbOJ2YbyL15pL-xehSxEyXymi-V54dT254KfCJZfHpG4A" type="text/javascript"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/jquery-ui.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/i18n/jquery-ui-i18n.min.js" type="text/javascript"></script>
        <script src="/js/jquery.dataTables.min.js" type="text/javascript"></script>
        <script src="/js/jquery.cookie.js" type="text/javascript"></script>
        <script src="/js/jquery.qtip-1.0.0-rc3.min.js" type="text/javascript"></script>
        <script src="/js/naked_password-0.2.4.min.js" type="text/javascript"></script>
        <script src="/js/application.js" type="text/javascript"></script>
        % if hasattr(c, 'title'):
        <title>${c.title} - sedemnajst.si</title>
        % else:
        <title>sedemnajst.si</title>
        % endif
        <script type="text/javascript">
            var _gaq = _gaq || [];
            _gaq.push(['_setAccount', 'UA-22838996-1']);
            _gaq.push(['_trackPageview']);

            (function() {
            var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
            ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
            var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
            })();
        </script>
    </head>
    <body>
        % if h.os.path.basename(h.pylons.config['__file__']) == 'development.ini':
        <div class="warning">
            To je razvijalska inačica!
        </div>
        % endif
        <div id="container">
            <div id="header">
                <div id="header-r">
                    <h1><a href="/"><img src="/images/header_l.gif" width="496" height="79" alt="sedemnajst.si" /></a></h1>
                    <div class="clear"></div>
                    <div id="search">
                        <form action="/search" method="get">
                            <p>
                                <input type="text" name="q" size="25" />
                                <input type="submit" value="Išči" />
                            </p>
                        </form>
                    </div>
                </div>
            </div>
            <div id="nav">
                <div id="nav-l">
                    <a href="/">Arhiv</a> |
                    <a href="/quotes">baza navedkov</a> |
                    <a href="/games">Igrice</a> |
                    <a href="/collage">Kolaž</a> |
                    <a href="/rankings">Kralji Gnoja</a> |
                    <a href="/users">Uporabniki</a>
                </div>
                <div id="nav-r">
                    % if 'user' in session:
                    <p>
                        ojla, ${h.link_to(h.literal(session['user'].nick_name), url('user', id=session['user'].id))}!
                        (${h.link_to('nastavitve', url('user_edit'))} | ${h.link_to('odjava', url('logout'))})
                    </p>
                    % else:
                    ${h.link_to('prijava', url('login'), id='open-login-dialog')}
                    <div id="login-dialog">
                        ${h.form('/login')}
                        <dl class="flat">
                            <dt>uporabniško ime</dt>
                            <dd>${h.text('nick_name', size=42)}</dd>
                            <dt>geslo</dt>
                            <dd>${h.password('password', size=42)}</dd>
                        </dl>
                        <p>
                            ${h.hidden('return_to', request.url)}
                            ${h.submit('submit', 'Prijavi me')}
                        </p>
                        ${h.end_form()}
                        <p style="text-align: right">${h.link_to('pozabljeno geslo?', url('reset_passwd'))}</p>
                    </div>
                    % endif
                </div>
                <div class="clear"></div>
            </div>
            <% messages = h.flash.pop_messages() %>
            % if messages:
            <ul id="flash-messages">
                % for message in messages:
                <li>${message}</li>
                % endfor
            </ul>
            % endif
            ${self.body()}
            <div id="footer">
                <form action="https://www.paypal.com/cgi-bin/webscr" method="post">
                    <p>
                        <input type="hidden" name="cmd" value="_donations" />
                        <input type="hidden" name="business" value="XM5WN5RDUBAGC" />
                        <input type="hidden" name="lc" value="SI" />
                        <input type="hidden" name="item_name" value="sedemnajst.si" />
                        <input type="hidden" name="currency_code" value="EUR" />
                        <input type="hidden" name="bn" value="PP-DonationsBF:btn_donateCC_LG.gif:NonHosted" />
                        <input type="image" src="https://www.paypalobjects.com/WEBSCR-640-20110401-1/en_US/i/btn/btn_donateCC_LG.gif" name="submit" alt="PayPal - The safer, easier way to pay online!" />
                        <img alt="" src="https://www.paypalobjects.com/WEBSCR-640-20110401-1/en_US/i/scr/pixel.gif" width="1" height="1" />
                    </p>
                </form>
                <a href="http://repo.or.cz/w/sedemnajstka.git"><img src="/images/git-logo.png" width="72" height="27" alt="sedemnajstka.git" /></a>
                <a href="http://www.slackware.com/"><img src="/images/simplepwrSW.gif" width="136" height="47" alt="Powered by Slackware" /></a>
                <a href="http://www.python.org/"><img src="/images/python-powered-w-100x40.png" width="100" height="40" alt="Powered by Python" /></img></a>
                <p class="date">
                % if c.next_run.seconds / 60 > 0 and c.next_run.seconds / 60 < 17:
                Ta arhiv je ${h.ftd(c.archive_age)} star. Naslednjič bo
                posodobljen čez ${h.ftd(c.next_run)}.
                % else:
                Ta arhiv je ${h.ftd(c.archive_age)} star&mdash;posodablja se
                <em>zdaj</em>!
                % endif
                </p>
            </div>
        </div>
    </body>
</html>
