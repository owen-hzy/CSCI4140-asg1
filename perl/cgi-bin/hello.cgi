#! /usr/bin/perl 

print "Content-type:text/html\r\n\r\n";
foreach (sort keys %ENV)
{
	print "<b>$_</b>: $ENV{$_}<br />\n";
}


