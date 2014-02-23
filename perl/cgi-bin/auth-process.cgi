#! /usr/bin/perl -w

use strict;
use CGI;
use DBI;

use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use Digest::SHA qw/sha1_hex sha256_hex/;

do "./include.cgi";

# Get database detail
my $db_host = $ENV{"OPENSHIFT_MYSQL_DB_HOST"};
my $db_username = $ENV{"OPENSHIFT_MYSQL_DB_USERNAME"};
my $db_password = $ENV{"OPENSHIFT_MYSQL_DB_PASSWORD"};
my $db_name = $ENV{"OPENSHIFT_APP_NAME"};

my $q = CGI -> new;
my $action = $q -> url_param("action");
$action =~ tr/a-z/A-Z/;

if ($action eq "LOGIN")
{
	login();
}elsif ($action eq "LOGOUT")
{
	logout();
}


sub login
{
	#Connect to database
	my $db_source = "DBI:mysql:$db_name;host=$db_host";
	my $dbh = DBI -> connect($db_source, $db_username, $db_password) or die $DBI::errstr;
	###
	my $q = CGI -> new;
	my $cookie = $q -> cookie("auth");
	
	if ($cookie)
	{
		my $query = $dbh -> prepare("SELECT * FROM sessions WHERE id = ?");
		$query -> execute($cookie) || die $query -> errstr;
		
		if ($query -> rows == 0)
		{
			undef $cookie;
		}
	}
	
	if (!$cookie)
	{
		if (check_user_password() == 0)
		{		
			print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/login.cgi?e=1");
			exit;
		}else 
		{
			my $sessid = sha1_hex(rand());
			my $time = `date +%s`;
			$time += 36000;
			my $username = $q -> param("username");
			my $auth = sha1_hex($username . rand());
		
			my $query = $dbh -> prepare("INSERT INTO sessions (id, sessid, expire) VALUES (?, ?, ?)");
			$query -> execute($auth, $sessid, $time) || die $query -> errstr;
		
			$query -> finish;
			$dbh -> disconnect;
			
			my $cookie1 = $q -> cookie(-name => "auth", -value => $auth, -expires => "+20d", -path => "/cgi-bin", -httponly => 1);
			my $cookie2 = $q -> cookie(-name => "SESSID", -value => $sessid, -expires => "+10h", -path => "/cgi-bin", -httponly => 1);
			print $q -> header(-cookie => [$cookie1, $cookie2], -refresh => "0; url=http://asg1-wtoughwhard.rhcloud.com/cgi-bin/display.cgi");
		}
	}
	else
	{
		if (check_user_password() == 0)
		{
			print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/login.cgi?e=1");
			exit;
		}
		else
		{
			my $sessid = sha1_hex(rand());
			my $time = `date +%s`;
			$time += 36000;
			
			my $query = $dbh -> prepare("UPDATE sessions SET sessid = ? WHERE id = ?");
			$query -> execute($sessid, $cookie) || die $query -> errstr;
			
			$query -> finish;
			$dbh -> disconnect;
			
			my $cookie1 = $q -> cookie(-name => "auth", -value => $cookie, -expires => "+20d", -path => "/cgi-bin", -httponly => 1);
			my $cookie2 = $q -> cookie(-name => "SESSID", -value => $sessid, -expires => "+10h", -path => "/cgi-bin", -httponly => 1);
			print $q -> header(-cookie => [$cookie1, $cookie2], -refresh => "0; url=http://asg1-wtoughwhard.rhcloud.com/cgi-bin/display.cgi");
			
		}
	}	
}

sub logout
{
	#Connect to database
	my $db_source = "DBI:mysql:$db_name;host=$db_host";
	my $dbh = DBI -> connect($db_source, $db_username, $db_password) or die $DBI::errstr;
	###
	
	my $auth = $q -> cookie("auth");
	my $sessid = $q -> cookie("SESSID");
	my $time = gmtime();
	
	my $query = $dbh -> prepare("UPDATE sessions SET sessid = ?, expire = ?, description = ?, size = ? WHERE id = ?");
	$query -> execute("NULL", "NULL", "NULL", "NULL", $auth) || die $query -> errstr;
	
	$query -> finish;
	$dbh -> disconnect;
	
	my $cookie = $q -> cookie(-name => "SESSID", -value => $sessid, -expires => $time, -path => "/cgi-bin", -httponly => 1);
	print $q -> header(-cookie => $cookie, -refresh => "0; url=http://asg1-wtoughwhard.rhcloud.com/cgi-bin/login.cgi?e=2");
}

 