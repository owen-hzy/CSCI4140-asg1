#! /usr/bin/perl -w

use strict;
use CGI;
use DBI;

use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
# use CGI::Session;
use Digest::SHA qw/sha256_hex/;

# Get database detail
my $db_host = $ENV{"OPENSHIFT_MYSQL_DB_HOST"};
my $db_username = $ENV{"OPENSHIFT_MYSQL_DB_USERNAME"};
my $db_password = $ENV{"OPENSHIFT_MYSQL_DB_PASSWORD"};
my $db_name = $ENV{"OPENSHIFT_APP_NAME"};

#Connect to database
my $db_source = "DBI:mysql:$db_name;host=$db_host";
my $dbh = DBI -> connect($db_source, $db_username, $db_password) or die $DBI::errstr;

my $q = CGI -> new;
my $action = $q -> url_param("action");
$action =~ tr/a-z/A-Z/;

if ($action eq "LOGIN")
{
	login();
}

if ($action eq "LOGOUT")
{
	logout();
}


sub login
{
	
	my $username = $q -> param("username");
	my $password = $q -> param("password");
	my $hashed_password = sha256_hex($password);
	
	my $query = $dbh -> prepare("SELECT * FROM users WHERE username = ? AND password = ?");
	$query -> execute($username, $hashed_password) or die $query -> errstr;
	
	if ($query -> rows == 0)
	{
		print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/login.cgi?f=");
	}else 
	{
#		my @data = $query -> fetchrow_array;
#		my $session = new CGI::Session(undef, undef, {Directory => $ENV{"OPENSHIFT_DATA_DIR"}});
		
#		$session -> param("auth", \@data);
#		$session -> expire("+10h");
		
#		my $cookie = cookie(-name => "CGISESSID", -value => $session -> id, -expires => '+10h', -path => "/cgi-bin");
#		print $q -> header(-cookie => $cookie);
		print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/display.cgi");
	}
	
	$dbh -> disconnect;
}

sub logout
{
	print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/login.cgi?t=");
}

 