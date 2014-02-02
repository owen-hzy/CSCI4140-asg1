#! /usr/bin/perl -w

use strict;
use CGI;
use DBI;

do "./include.cgi";
my $q = CGI -> new;
my $session = session_check();
my $mix = $q -> cookie("mix") || "2-4-size-ASC";
my @cookie = split(/-/, $mix);
my $page_nu = $q -> url_param("p") || 1;

my $row = $cookie[0];
my $column = $cookie[1];
my $sort = $cookie[2];
my $order = $cookie[3];

print $q -> header();
print <<"HEADER";
<!DOCTYPE html>
<html>
<head>
<title>VIEW</title>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
</head>
<body>
HEADER

print <<"TOPBAR";
<section>
<form method="POST" action="view_handle.cgi?action=change&p=$page_nu">
<label for="row">Dimension:</label>
<input type="number" name="row" id="row" maxlength="1" min="1" max="9" value="$row"/>x
<input type="number" name="column" maxlength="1" value="$column" min="1" max="9" />
TOPBAR

my @sort_ex = ("size", "name", "upload_time");
print "<select name='sort'>";
foreach my $sort_item (@sort_ex)
{
	if ($sort_item eq $sort)
	{
		print "<option value='$sort_item' selected>$sort_item</option>";
	}else
	{
		print "<option value='$sort_item'>$sort_item</option>";
	}
}
print "</select>";


print "<select name='order'>";
if ($order eq "ASC")
{
	print "<option value=''ASC' selected>Ascending</option><option value='DESC'>Descending</option>";
}else
{
	print "<option value=''ASC'>Ascending</option><option value='DESC' selected>Descending</option>";
}
	
print "</select>";

print "<input type='submit' value='Change' />";
print "</form>";
print "<hr />";

my @data = get_data($sort, $order);
my $photonu = (scalar @data)/2;
my $total = $row * $column;
my $page = $photonu/$total;
if (int($page) != $page)
{
	$page = int($page) + 1;
}
my $count = ($page_nu - 1) * 2 * $total;
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
			print "<figcaption>$data[$count]</figcaption>";
		}else
		{
			print "<figcaption><input type='checkbox' name='$data[$count]' value='selected' />$data[$count]</figcaption>";
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
<form method="POST" action="view_handle.cgi?action=go">
<label for="page">Page<input type="number" name="page" id="page" maxlength="3" value="$page_nu" min="1" max="$page" /> of $page</label>
<input type="submit" value="Go to page" />
</form>
</section>
FOOTER

if ($session != 1)
{
	print "<a href='http://asg1-wtoughwhard.rhcloud.com/cgi-bin/display.cgi'>Back to Display</a>";
}else
{
	print "<a href='http://asg1-wtoughwhard.rhcloud.com/cgi-bin/login.cgi'>Back to Login</a>";
}

print $q -> end_html;




