fs = require 'fs'
ck = require 'coffeekup'

converter = new (require 'showdown').Showdown.converter()

contents = fs.readFileSync "entries/style", "UTF-8"
template = fs.readFileSync "fancy-temp.coffee", "UTF-8"

html = converter.makeHtml(contents)

console.log ck.render(template, content: html)
