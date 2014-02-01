#! /usr/bin/perl -w

use CGI;
use DBI;

do "./include.cgi";

my $q = CGI -> new;
#Check the session information
session_check();
###

print $q -> header();
print $q -> start_html(-title => "DISPLAY", -meta => {"http-equiv"=>"content-type", "content"=>"text/html; charset=UTF-8"});

print <<"MAIN_BODY";
<section>
<ul>
<li><a href="view.cgi">View Album</a></li>
<li><a href="upload_form.cgi">Upload Photos</a></li>
<li><a href="auth-process.cgi?action=logout">Logout</a></li>
</ul>
</section>
MAIN_BODY

print $q -> end_html;