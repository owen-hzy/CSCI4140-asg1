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

sub check_name_type
{
	my $filename = shift;
	$_ = $filename;
	my ($name, $ext) = /([a-z0-9-_]+).([a-z0-9-_]+)/;
	
	my $q = CGI -> new;
	my $upload_dir = $ENV{"OPENSHIFT_DATA_DIR"};
	
	my $result = `/usr/bin/identify \"$upload_dir/tmp/$filename\"`;
	my @type = split(/ /, $result);

	if ($name && ($type[1] eq "JPEG" || $type[1] eq "PNG" || $type[1] eq "GIF"))
	{	
		return 1;
	}else
	{
		`/bin/rm -rf \"$upload_dir/tmp"`;
		print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/upload_form.cgi?e=2");
		exit 0;
	}
}

sub check_duplicate
{
	my $filename = shift;
	my $description = shift;
	
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
	
	my $q = CGI -> new;
	
	my $query = $dbh -> prepare("SELECT * FROM photos WHERE name = ?");
	$query -> execute($filename) or die $query -> errstr;
	
	if ($query -> rows != 0)
	{
		$query -> finish;
		
		my $sessid = $q -> cookie("SESSID");
		
		$query = $dbh -> prepare("UPDATE sessions SET (desc = ?) WHERE sessid = ?");
		$query -> execute('$description', $sessid) || die $query -> errstr;
		
		$query -> finish;
		$dbh -> disconnect;
		
		print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/duplicate.cgi");
		exit 0;	
	}
}

sub insert_photo
{	
	my $filename = shift;
	my $description = shift;
	my $totalBytes = shift;
	
	# Database Info
	my $db_host =       $ENV{'OPENSHIFT_MYSQL_DB_HOST'};
	my $db_username =   $ENV{'OPENSHIFT_MYSQL_DB_USERNAME'};
	my $db_password =   $ENV{'OPENSHIFT_MYSQL_DB_PASSWORD'};
	my $db_name =       $ENV{'OPENSHIFT_APP_NAME'};
	###
	my $upload_dir = $ENV{"OPENSHIFT_DATA_DIR"};
	my $q = CGI -> new;
	
	`/bin/mv \"$upload_dir/tmp/$filename\" \"$upload_dir\$filename\"`;
	`/bin/rm -rf \"$upload_dir/tmp\"`;
	
	$_ = $filename;
	my ($name, $ext) = /([a-z0-9-_]+).([a-z0-9-_]+)/;
	
	my $thumb_name = $name . "_thumb." . $ext;
	`/usr/bin/convert \"$upload_dir/$filename\" -resize 30% \"$upload_dir/$thumb_name\"`;
	
	my $time = `/bin/date +%s`;
	
	# Connect the database
	my $db_source = "DBI:mysql:$db_name;host=$db_host";
	my $dbh = DBI -> connect($db_source, $db_username, $db_password) || die $DBI::errstr;
	###
	
	my $query = $dbh -> prepare("INSERT INTO photos (name, thumb_name, size, upload_time, description) VALUES (?, ?, ?, ?, ?)");
	$query -> execute($filename, $thumb_name, $totalBytes, $time, $description) || die $query -> errstr;
	
	$query -> finish;
	$dbh -> disconnect;
	
	print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/upload_form.cgi?e=5");
}

sub update_photo
{
	my $filename = shift;
	my $description = shift;
	my $totalBytes = shift;

	# Database Info
	my $db_host =       $ENV{'OPENSHIFT_MYSQL_DB_HOST'};
	my $db_username =   $ENV{'OPENSHIFT_MYSQL_DB_USERNAME'};
	my $db_password =   $ENV{'OPENSHIFT_MYSQL_DB_PASSWORD'};
	my $db_name =       $ENV{'OPENSHIFT_APP_NAME'};
	###
	my $upload_dir = $ENV{"OPENSHIFT_DATA_DIR"};
	my $q = CGI -> new;

	`/bin/rm -rf \"$upload_dir/tmp\"`;
	
	$_ = $filename;
	my ($name, $ext) = /([a-z0-9-_]+).([a-z0-9-_]+)/;
	
	my $thumb_name = $name . "_thumb." . $ext;
	`/usr/bin/convert \"$upload_dir/$filename\" -resize 30% \"$upload_dir/$thumb_name\"`;
	
	my $time = `/bin/date +%s`;
	
	# Connect the database
	my $db_source = "DBI:mysql:$db_name;host=$db_host";
	my $dbh = DBI -> connect($db_source, $db_username, $db_password) || die $DBI::errstr;
	###
	
	my $query = $dbh -> prepare("UPDATE photos SET (size =?, upload_time = ?, description =?) WHERE name = ?");
	$query -> execute($totalBytes, $time, $description, $filename) || die $query -> errstr;
	
	$query -> finish;
	$dbh -> disconnect;
	
	print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/upload_form.cgi?e=5");
}