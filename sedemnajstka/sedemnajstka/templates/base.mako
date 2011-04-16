<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <link href="/favicon.png" rel="icon" type="image/png" />
        <link href="/style.css" rel="stylesheet" type="text/css" />
        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
        <script src="https://www.google.com/jsapi?key=ABQIAAAAIiJO64nS9X44-5zAPRx_CBQ2dbh21h_ChSbOJ2YbyL15pL-xehSxEyXymi-V54dT254KfCJZfHpG4A" type="text/javascript"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js" type="text/javascript"></script>
        <script src="/js/application.js" type="text/javascript"></script>
        % if hasattr(c, 'title'):
        <title>${c.title} - sedemnajst.si</title>
        % else:
        <title>sedemnajst.si</title>
        % endif
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
                </div>
            </div>
            <div id="nav">
                <div id="nav-l">
                    <a href="/">Arhiv</a> |
                    <a href="/info">Info</a> |
                    <a href="/rankings">Kralji Gnoja</a> |
                    <a href="/users">Uporabniki</a>
                </div>
                <div id="nav-r">
                    % if 'user' in session:
                    <p>ojla, <a href="${url('user', id=session['user'].id)}">${session['user'].nick_name}</a>! (<a href="${url('logout')}">odjava</a>)</p>
                    % else:
                    <a href="${url('login')}">prijava</a>
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
        </div>
    </body>
</html>
