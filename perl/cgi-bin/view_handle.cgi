#! /usr/bin/perl -w

use CGI;
use DBI;
use strict;

do "./include.cgi";

my $q = CGI -> new;
my $action = $q -> url_param("action");
$action =~ tr/a-z/A-Z/;

if ($action eq "DELETE")
{
	# Check the session info
	if (session_check() == 1)
	{
		print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/login.cgi?e=3");
		exit;
	}
	###
	
	my @data = get_data();
	for (my $i = 0; $i < scalar @data; $i += 2)
	{
		my $select = $q -> param("$data[$i]");
		if (!$select)
		{
			next;
		}else
		{
			# Database Info
			my $db_host =       $ENV{'OPENSHIFT_MYSQL_DB_HOST'};
			my $db_username =   $ENV{'OPENSHIFT_MYSQL_DB_USERNAME'};
			my $db_password =   $ENV{'OPENSHIFT_MYSQL_DB_PASSWORD'};
			my $db_name =       $ENV{'OPENSHIFT_APP_NAME'};
			###
	
			# Connect the database
			my $db_source = "DBI:mysql:$db_name;host=$db_host";
			my $dbh = DBI -> connect($db_source, $db_username, $db_password) || die $DBI::errstr;
			###
			my $upload_dir = $ENV{"OPENSHIFT_DATA_DIR"};
			
			my $query = $dbh -> prepare("DELETE FROM photos WHERE name = ?");
			$query -> execute($data[$i]) || die $query -> errstr;
			
			$query -> finish;
			$dbh -> disconnect;
			
			$_ = $data[$i];
			my ($filename, $ext) = /([a-z0-9-_]+).([a-z0-9-_]+)/;
	
			my $thumb_name = $filename . "_thumb." . $ext;
			`/bin/rm -f \"$upload_dir/$data[$i]\"`;
			`/bin/rm -f \"$upload_dir/$thumb_name\"`;
			
		}
	}
 	print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/view.cgi");
}

if ($action eq "CHANGE")
{
	my $cookieo = $q -> cookie("mix") || "2-4-size-ASC";
	my $page_nu = $q -> url_param("p") || 1;
	my @array = split(/-/, $cookieo);
	
	my $row = $q -> param("row") || $array[0];
	my $column = $q -> param("column") || $array[1];
	my $sort = $q -> param("sort") || $array[2];
	my $order = $q -> param("order") || $array[3];

	my $mix = $row . "-" . $column . "-" . $sort . "-" . $order;
	my $cookien = $q -> cookie(-name => "mix", -value => $mix, -expires => "+1h", -path => "/cgi-bin");
	
	print $q -> header(-cookie => $cookien, refresh => "0.1; url=http://asg1-wtoughwhard.rhcloud.com/cgi-bin/view.cgi");
}

if ($action eq "GO")
{
	my $page = $q -> param("page") || 1;
	
	print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/view.cgi?p=$page");
}







