<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <link href="/favicon.png" rel="icon" type="image/png" />
        <link href="/style.css" rel="stylesheet" type="text/css" />
        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
        % if hasattr(c, 'title'):
        <title>${c.title} - nigger.it.cx</title>
        % else:
        <title>nigger.it.cx</title>
        % endif
    </head>
    <body>
        <p class="navigation">
            [ <a href="/">ARHIV</a> |
            <a href="/users">UPORABNIKI</a> ]
            <span class="title">
                % if hasattr(c, 'title'):
                [ ${c.title} ]
                % else:
                [ nigger.it.cx ]
                % endif
            </span>
        </p>
        ${self.body()}
    </body>
</html>
