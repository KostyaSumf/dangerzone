window.onload = ->

  console.log('Initalizing.')

  init = ->

    canvas = document.getElementById("mainCanvas")
    sheetengine.scene.init canvas,
      w: 2000
      h: 1500

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
      w: 750
      h: 750
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
