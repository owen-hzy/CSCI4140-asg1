#! /usr/bin/perl -w

use strict;
use CGI;
use DBI;

do "./include.cgi";
my $q = CGI -> new;
my $session = session_check();

print $q -> header();
print $q -> start_html(-title=>"UPLOAD", -meta=>{"http-equiv"=>"content-type", "content"=>"text/html; charset=UTF-8"});

print <<"TOPBAR";
<section>
<form method="POST" action="view_handle.cgi?action=change">
<label for="row">Dimension:</label>
<input type="text" name="row" id="row" maxlength="1" />x<input type="text" name="column" maxlength="1" />
<select name="sort">
	<option value="size" selected>File Size</option>
	<option value="name">Name</option>
	<option value="time">Upload time</option>
</select>

<select name="order">
	<option value="ascending" selected>Ascending</option>
	<option value="descending">Descending</option>
</select>

<input type="submit" value="Change" />
</form>
<hr />
TOPBAR







print <<"FOOTER";
<hr />
<section>
<form method="POST" action="view.cgi?action=go">
<label for="page">Page<input type="text" name="page" id="page" maxlength="3" value="1" /> of 10</label>
<input type="submit" value="Go to page" />
</form>
</section>
FOOTER

