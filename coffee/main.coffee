$(document).ready ->

  console.log('Initalizing.')

  init = ->

    canvas = document.getElementById("cvs")
    canvas.width = document.body.clientWidth
    canvas.height = document.body.clientHeight
    width = document.body.clientWidth
    height = document.body.clientHeight

    sheetengine.scene.init canvas,
      w: width*2
      h: height*2

    sheetengine.scene.tilewidth = 200
    basesheet = new sheetengine.BaseSheet(
      x: 0
      y: 0
      z: 0
    ,
      alphaD: 90
      betaD: 0
      gammaD: 0
    ,
      w: width
      h: width
    )
    basesheet.color = "#009fea"

    sheetengine.calc.calculateChangedSheets()
    sheetengine.drawing.drawScene true

    $('#cvs').click((e) ->
      console.log 'click ' + e.pageX + ' ' + e.pageY
      sheetengine.scene.setCenter(
        x: e.pageX
        y: e.pageY
        z: 0
      )
    )

    setInterval(->
      # calculate sheets and draw scene
      sheetengine.calc.calculateChangedSheets()
      sheetengine.drawing.drawScene()
    , 30)


  init()
