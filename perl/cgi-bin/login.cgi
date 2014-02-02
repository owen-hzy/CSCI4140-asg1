#! /usr/bin/perl -w

use strict;
use CGI;

my $q = CGI -> new;
my $e = $q -> url_param("e") || 0;

print $q -> header();
print <<"HEADER";
<!DOCTYPE html>
<html>
<head>
<title>LOGIN</title>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
</head>
<body>
HEADER

if ($e == 1)
{
	print $q -> h3("Login Failed!");
}
elsif ($e == 2)
{
	print $q -> h3("Thanks for visiting!");
}
elsif ($e == 3)
{
	print $q -> h3("Please Login!");
}

print <<"MAIN_BODY";
<section>
<fieldset>	
	<legend>User Login</legend>
	<form method="post" action="auth-process.cgi?action=login">
		<label for="username">Username:</label>
		<input type="text" name="username" maxlength="19" required="true" id="username" />
		
		<br />
		
		<label for="password">Password:</label>
		<input type="password" name="password" required="true" maxlength="30" id="password" />
		
		<br />
		
		<input type="submit" value="Log In" />
	</form>
</fieldset>
</section>

<br />
<section>
	<a href="view.cgi">View Album (read_only)</a>
</section>
MAIN_BODY

print $q -> end_html;
