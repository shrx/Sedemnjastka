<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <link href="/favicon.png" rel="icon" type="image/png" />
        <link href="/style.css" rel="stylesheet" type="text/css" />
        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
	<script type="text/javascript" src="/js/jquery-1.5.2.min.js"></script>
	<script type="text/javascript" src="/js/application.js"></script>
        % if hasattr(c, 'title'):
        <title>${c.title} - sedemnajst.si</title>
        % else:
        <title>sedemnajst.si</title>
        % endif
    </head>
    <body>
        <div id="header">
	    <div id="header-r">
		<h1><a href="/"><img src="/images/header_l.gif" width="496" height="79" alt="sedemnajst.si" /></a></h1>
		<div class="clear"></div>
	    </div>
	</div>
        <p class="navigation">
            <a href="/">Arhiv</a> |
            <a href="/info">Info</a> |
            <a href="/rankings">Kralji Gnoja</a> |
            <a href="/users">Uporabniki</a>
        </p>
        ${self.body()}
    </body>
</html>
