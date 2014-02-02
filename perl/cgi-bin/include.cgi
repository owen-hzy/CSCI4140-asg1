#! /usr/bin/perl -w

use CGI;
use DBI;
use strict;

sub session_check
{
	
	my $db_host =       $ENV{'OPENSHIFT_MYSQL_DB_HOST'};
	my $db_username =   $ENV{'OPENSHIFT_MYSQL_DB_USERNAME'};
	my $db_password =   $ENV{'OPENSHIFT_MYSQL_DB_PASSWORD'};
	my $db_name =       $ENV{'OPENSHIFT_APP_NAME'};
	
	my $q = CGI -> new;
	my $sessid = $q -> cookie("SESSID");
	if (!$sessid)
	{
		print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/login.cgi?e=3");
		exit;
	}else
	{		
		# Connect the database
		my $db_source = "DBI:mysql:$db_name;host=$db_host";
		my $dbh = DBI -> connect($db_source, $db_username, $db_password) || die $DBI::errstr;
		###
		
		my $query = $dbh -> prepare("SELECT * from sessions WHERE sessid = ?");
		$query -> execute($sessid) || die $query -> errstr;
		my @data = $query -> fetchrow_array; 
		
		if ($query -> rows == 0)
		{
			$query -> finish;
			$dbh -> disconnect;
			
			print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/login.cgi?e=3");
			exit;
		}elsif ($data[1] < `date +%s`)
		{
			my $query = $dbh -> prepare("DELETE FROM sessions WHERE sessid = ?");
			$query -> execute($sessid) || die $query -> errstr;
			
			$query -> finish;
			$dbh -> disconnect;
			
			print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/login.cgi?e=3");
			exit;
		}
		
		$query -> finish;
		$dbh -> disconnect;
		
	}
	
}