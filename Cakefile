{exec} = require 'child_process'
task 'build', 'Installs the compiled coffeescript files into static/js.', ->
  exec 'coffee --compile --output static/js/ coffee/', (err, stdout, stderr) ->
    throw err if err
    console.log stdout + stderr
