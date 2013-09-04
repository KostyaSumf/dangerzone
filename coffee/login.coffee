$.fn.serializeObject = ->
  o = {}
  a = @serializeArray()
  $.each a, ->
    if o[@name] isnt `undefined`
      o[@name] = [o[@name]]  unless o[@name].push
      o[@name].push @value or ""
    else
      o[@name] = @value or ""

  o

$ ->
  $("loginform").submit ->
    words = JSON.stringify($("loginform").serializeObject())
    $.post '/api/account/login', words, (->
      window.location.replace "/play"
    ), 'application/json'