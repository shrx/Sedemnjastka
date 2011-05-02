<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
        <link href="/favicon.png" rel="icon" type="image/png" />
        <link href="/style.css" rel="stylesheet" type="text/css" />
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/themes/sunny/jquery-ui.css" rel="stylesheet" type="text/css" />
        <script src="https://www.google.com/jsapi?key=ABQIAAAAIiJO64nS9X44-5zAPRx_CBQ2dbh21h_ChSbOJ2YbyL15pL-xehSxEyXymi-V54dT254KfCJZfHpG4A" type="text/javascript"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js" type="text/javascript"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/jquery-ui.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/i18n/jquery-ui-i18n.min.js" type="text/javascript"></script>
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
                        <form action="/search" method="GET">
                            <input type="text" name="q" size="25" />
                            <input type="submit" value="išči" />
                        </form>
                    </div>
                </div>
            </div>
            <div id="nav">
                <div id="nav-l">
                    <a href="/">Arhiv</a> |
                    <a href="/quotes">baza navedkov</a> |
                    <a href="/info">Info</a> |
                    <a href="/rankings">Kralji Gnoja</a> |
                    <a href="/users">Uporabniki</a>
                </div>
                <div id="nav-r">
                    % if 'user' in session:
                    <p>ojla, ${h.link_to(session['user'].nick_name, url('user_edit'))}! (${h.link_to('odjava', url('logout'))})</p>
                    % else:
                    ${h.link_to('prijava', url('login'))}
                    % endif
                </div>
                <div class="clear"></div>
            </div>
            <a href="http://github.com/ans/sedemnajstka"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://d3nwyuy0nl342s.cloudfront.net/img/e6bef7a091f5f3138b8cd40bc3e114258dd68ddf/687474703a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f7265645f6161303030302e706e67" alt="Fork me on GitHub"></a>
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
                    <input type="hidden" name="cmd" value="_donations" />
                    <input type="hidden" name="business" value="XM5WN5RDUBAGC" />
                    <input type="hidden" name="lc" value="SI" />
                    <input type="hidden" name="item_name" value="sedemnajst.si" />
                    <input type="hidden" name="currency_code" value="EUR" />
                    <input type="hidden" name="bn" value="PP-DonationsBF:btn_donateCC_LG.gif:NonHosted" />
                    <input type="image" src="https://www.paypalobjects.com/WEBSCR-640-20110401-1/en_US/i/btn/btn_donateCC_LG.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!" />
                    <img alt="" border="0" src="https://www.paypalobjects.com/WEBSCR-640-20110401-1/en_US/i/scr/pixel.gif" width="1" height="1" />
                </form>
                <img src="/images/powered_by_gnu_emacs.png" width="100" height="36" alt="Powered by GNU Emacs" />
                <img src="/images/button-k1.png" width="88" height="30" alt="Powered by Debian" />
                <img src="/images/pythonPowered2.png" width="93" height="46" alt="Powered by Python" />
                <img src="/images/pg-power.png" width="130" height="47" alt="Powered by Postgres" />
            </div>
        </div>
    </body>
</html>
