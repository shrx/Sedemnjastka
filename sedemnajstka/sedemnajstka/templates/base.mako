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
        <script type="text/javascript">
            var _gaq = _gaq || [];
            _gaq.push(['_setAccount', 'UA-19427685-1']);
            _gaq.push(['_trackPageview']);

            (function() {
                var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
                ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
                var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
            })();
        </script>
    </head>
    <body>
        <p class="navigation">
            [ <a href="/">ARHIV</a> |
            <a href="/rankings">KRALJI GNOJA</a> |
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
