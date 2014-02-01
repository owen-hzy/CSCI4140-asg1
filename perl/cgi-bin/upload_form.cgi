#! /usr/bin/perl -w

use strict;
use CGI;

my $q = CGI -> new;

print $q -> header();
print $q -> start_html(-title=>"UPLOAD", -meta=>{"http-equiv"=>"content-type", "content"=>"text/html; charset=UTF-8"});

if (defined $q -> url_param("fnv"))
{
	print $q -> h3("Filetype is not valid!");
}
elsif (defined $q -> url_param("now"))
{
	print $q -> h3("Please choose another photo!");
}

print <<"MAIN_BODY";
<section>

<form enctype="multipart/form-data" action="upload.cgi" method="POST">
    <label for="pic">Choose an image (.jpg .gif .png):</label>
    <input type="file" id="pic" name="pic" accept="image/gif, image/jpeg, image/png" required="true" />
    <br />
    <label for="desc">Description (50 bytes max)</label>
    <input type="text" id="desc" name="desc" maxlength="50" />
    <br />
    <input type="submit" value="Upload" />
</form>

</section>
MAIN_BODY

print $q -> end_html;
