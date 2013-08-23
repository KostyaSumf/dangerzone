window.onload = ->
  Crafty.init()
  Crafty.sprite 128, "/static/images/sprite.png",
    grass: [0, 0, 1, 1]
    stone: [1, 0, 1, 1]

  iso = Crafty.isometric.size(128)
  z = 0
  i = 20

  while i >= 0
    y = 0

    while y < 20
      which = Crafty.math.randomInt(0, 1)

      #destroy on right click
      #right click seems not work in Mac OS
      #delete it

      #if(e.button === 2)
      tile = Crafty.e("2D, DOM, " + ((if not which then "grass" else "stone")) + ", Mouse").attr("z", i + 1 * y + 1).areaMap([64, 0], [128, 32], [128, 96], [64, 128], [0, 96], [0, 32]).bind("Click", (e) ->
        console.log e.button
        @destroy()
      ).bind("MouseOver", ->
        if @has("grass")
          @sprite 0, 1, 1, 1
        else
          @sprite 1, 1, 1, 1
      ).bind("MouseOut", ->
        if @has("grass")
          @sprite 0, 0, 1, 1
        else
          @sprite 1, 0, 1, 1
      )
      iso.place i, y, 0, tile
      y++
    i--
  Crafty.addEvent this, Crafty.stage.elem, "mousedown", (e) ->
    scroll = (e) ->
      dx = base.x - e.clientX
      dy = base.y - e.clientY
      base =
        x: e.clientX
        y: e.clientY

      Crafty.viewport.x -= dx
      Crafty.viewport.y -= dy
    return  if e.button > 1
    base =
      x: e.clientX
      y: e.clientY

    Crafty.addEvent this, Crafty.stage.elem, "mousemove", scroll
    Crafty.addEvent this, Crafty.stage.elem, "mouseup", ->
      Crafty.removeEvent this, Crafty.stage.elem, "mousemove", scroll

