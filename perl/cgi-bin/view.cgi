#! /usr/bin/perl -w

use strict;
use CGI;
use DBI;

do "./include.cgi";
my $q = CGI -> new;
my $session = session_check();
my $mix = $q -> cookie("mix") || "2-4-size-ASC";
my @cookie = split(/-/, $mix);

my $row = $cookie[0];
my $column = $cookie[1];
my $sort = $cookie[2];
my $order = $cookie[3];

print $q -> header();
print $q -> start_html(-title=>"VIEW", -meta=>{"http-equiv"=>"content-type", "content"=>"text/html; charset=UTF-8"});

print <<"TOPBAR";
<section>
<form method="POST" action="view_handle.cgi?action=change">
<label for="row">Dimension:</label>
<input type="text" name="row" id="row" maxlength="1" />x<input type="text" name="column" maxlength="1" />
<select name="sort">
	<option value="size" selected>File Size</option>
	<option value="name">Name</option>
	<option value="upload_time">Upload time</option>
</select>

<select name="order">
	<option value="ASC" selected>Ascending</option>
	<option value="DESC">Descending</option>
</select>

<input type="submit" value="Change" />
</form>
<hr />
TOPBAR

my @data = get_data($sort, $order);
my $count = 0;
if ($session != 1)
{
	print "<form method='POST' action='view_handle.cgi?action=delete'>";
}
print "<table cellpadding='5pt' cellspacing='5pt'>";

for (my $i = 0; $i < $row; $i++)
{
	print "<tr>";
	for (my $j = 0; $j < $column; $j++)
	{
		$_ = $data[$count];
		my ($filename, $ext) = /([a-z0-9-_]+).([a-z0-9-_]+)/;
	
		my $thumb_name = $filename . "_thumb." . $ext;
		my $description = $data[$count + 1];
		print <<"CONTENT";
		<td>
		<a href='../data/$data[$count]'>
		<img src='../data/$thumb_name' title='$description'></a>
CONTENT
		if ($session == 1){
			print "<br /><figcation>$data[$count]</figcation>";
		}else
		{
			print "<br /><figcation><input type='checkbox' name='$data[$count]' value='selected' />$data[$count]</figcation>";
		}
		print "</td>";
		$count += 2;
	
		if ($count >= scalar @data)
		{
			last;
		}	
	}
	print "</tr>";
	if ($count >= scalar @data)
	{
		last;
	}
}

print "</table>";
if ($session != 1){
	print "<input type='submit' value='Remove selected' />";
	print "</form>";
}




print <<"FOOTER";
<hr />
<section>
<form method="POST" action="view.cgi?action=go">
<label for="page">Page<input type="text" name="page" id="page" maxlength="3" value="1" /> of 10</label>
<input type="submit" value="Go to page" />
</form>
</section>
FOOTER

