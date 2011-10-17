fs = require 'fs'
converter = new (require 'showdown').Showdown.converter()

contents = fs.readFileSync "entries/style", "UTF-8"
html = converter.makeHtml(contents)

console.log "
<!DOCTYPE HTML>

<html>
<head>
  <meta charset='utf-8'>

  <title>johnfn's blog @ GitHub</title>

  <link rel='stylesheet' type='text/css' href='fancy.css' />
</head>

<body>
  #{html}
</body>
"
