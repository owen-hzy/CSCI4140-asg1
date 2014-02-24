#! /usr/bin/perl -w

use CGI;
use DBI;
use strict;
use Digest::SHA qw/sha1_hex sha256_hex/;

sub session_check
{
	
	my $db_host =       $ENV{'OPENSHIFT_MYSQL_DB_HOST'};
	my $db_username =   $ENV{'OPENSHIFT_MYSQL_DB_USERNAME'};
	my $db_password =   $ENV{'OPENSHIFT_MYSQL_DB_PASSWORD'};
	my $db_name =       $ENV{'OPENSHIFT_APP_NAME'};
	
	my $q = CGI -> new;
	my $auth = $q -> cookie("auth");
	my $sessid = $q -> cookie("SESSID");
	if (!$sessid || !$auth)
	{
		return 1;
	}else
	{		
		# Connect the database
		my $db_source = "DBI:mysql:$db_name;host=$db_host";
		my $dbh = DBI -> connect($db_source, $db_username, $db_password) || die $DBI::errstr;
		###
		
		my $query = $dbh -> prepare("SELECT * from sessions WHERE id = ? AND sessid = ?");
		$query -> execute($auth, $sessid) || die $query -> errstr;
		my @data = $query -> fetchrow_array; 
		
		if ($query -> rows == 0)
		{
			$query -> finish;
			$dbh -> disconnect;
			
			return 1;
		}elsif ($data[2] < `date +%s`)
		{
			my $query = $dbh -> prepare("UPDATE sessions SET sessid = ?, expire = ?, description = ?, size = ? WHERE id = ?");
			$query -> execute("NULL", "NULL", "NULL", "NULL", $auth) || die $query -> errstr;
			
			$query -> finish;
			$dbh -> disconnect;
			
			return 1;
		}
		
		$query -> finish;
		$dbh -> disconnect;
	}
	return 0;
}

sub check_name_type
{
	my $filename = shift;
	$_ = $filename;
	my ($name, $ext) = /([a-z0-9-_]+).([a-z0-9-_]+)/;
	$ext =~ tr/a-z/A-Z/;
	
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
	my $size = shift;
	
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
		
		my $query = $dbh -> prepare("UPDATE sessions SET description = ?, size = ? WHERE sessid = ?");
		$query -> execute($description, $size, $sessid) || die $query -> errstr;
		
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
	my $name = shift;
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
	
	$_ = $name;
	my ($filename, $ext) = /([a-z0-9-_]+).([a-z0-9-_]+)/;
	
	my $thumb_name = $filename . "_thumb." . $ext;
	`/usr/bin/convert \"$upload_dir/$name\" -resize 30% \"$upload_dir/$thumb_name\"`;
	
	my $time = `/bin/date +%s`;
	
	# Connect the database
	my $db_source = "DBI:mysql:$db_name;host=$db_host";
	my $dbh = DBI -> connect($db_source, $db_username, $db_password) || die $DBI::errstr;
	###
	
	my $query = $dbh -> prepare("UPDATE photos SET size =?, upload_time = ?, description = ? WHERE name = ?");
	$query -> execute($totalBytes, $time, $description, $name) || die $query -> errstr;
	
	$query -> finish;
	$dbh -> disconnect;
	
	print $q -> redirect("http://asg1-wtoughwhard.rhcloud.com/cgi-bin/upload_form.cgi?e=5");
}

sub get_data
{
	my $q = CGI -> new;
	
	my $sort = shift || "size";
	my $order = shift || "ASC";
	
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
	
	my @data = ();
	my $query = $dbh -> prepare("SELECT name, description FROM photos ORDER BY $sort $order");
	$query -> execute() || die $query -> errstr;
	
	while (my @result = $query -> fetchrow_array)
	{
		push(@data, $result[0]);
		push(@data, $result[1]);
	}
	
	$query -> finish;
	$dbh -> disconnect;
	
	return @data;
}

sub check_user_password
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
	
	my $q = CGI -> new;
	my $username = $q -> param("username");
	my $password = $q -> param("password");
	my $hashed_password = sha256_hex($password);
	
	my $query = $dbh -> prepare("SELECT * FROM users WHERE username = ? AND password = ?");
	$query -> execute($username, $hashed_password) or die $query -> errstr;
	
	if ($query -> rows == 0)
	{
		$query -> finish;
		$dbh -> disconnect;
		return 0;
	}
	else
	{
		$query -> finish;
		$dbh -> disconnect;
		return 1;
	}
}

sub session_regenerate
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
	
	my $q = CGI -> new;
	my $auth = $q -> cookie("auth");
	
	my $sessid = sha1_hex(rand());
	my $time = `date +%s`;
	$time += 36000;
	
	my $query = $dbh -> prepare("UPDATE sessions SET sessid = ?, expire = ?, description = ?, size = ? WHERE id = ?");
	$query -> execute($sessid, $time, "NULL", "NULL", $auth) || die $query -> errstr;
	
	my $cookie = $q -> cookie(-name => "SESSID", -value => $sessid, -expires => "+10h", -path => "/cgi-bin", -httponly => 1);
	
	return $cookie;
	
	
}