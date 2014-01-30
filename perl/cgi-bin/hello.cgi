use CGI;

print "Content-type:text\html\r\n\r\n"
print <<'HELLO_WORLD';
<html>
<head>
<title>Hello World - First CGI Program</title>
</head>

<body>
<h2>Hello World! This is my first CGI program</h2>;
</body>
</html>
HELLO_WORLD

