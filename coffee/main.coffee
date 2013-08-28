window.onload = ->

  console.log('Initalizing.')

  init = ->

    canvas = document.getElementById("mainCanvas")
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
      w: width*4
      h: width*4
    )
    basesheet.color = "#009fea"

    sheetengine.calc.calculateChangedSheets()
    sheetengine.drawing.drawScene true

    setInterval(->
      # calculate sheets and draw scene
      sheetengine.calc.calculateChangedSheets()
      sheetengine.drawing.drawScene()
    , 30)


  init()
