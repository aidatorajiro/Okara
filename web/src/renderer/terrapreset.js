import terra from 'terra'

terra.registerCA({
  type: 'cyclic',
  colors: ['255,0,0,1', '255,96,0,1', '255,191,0,1', '223,255,0,1', '128,255,0,1', '32,255,0,1', '0,255,64,1', '0,255,159,1', '0,255,255,1', '0,159,255,1', '0,64,255,1', '32,0,255,1', '127,0,255,1', '223,0,255,1', '255,0,191,1', '255,0,96,1'],
  colorFn: function () { return this.colors[this.state] },
  process: function (neighbors, x, y) {
    var next = (this.state + 1) % 16
    var changing = neighbors.some(function (spot) {
      return spot.creature.state === next
    })
    if (changing) this.state = next
    return true
  }
})

terra.registerCA({
  type: 'GoL',
  colorFn: function () { return this.alive ? '213,191,167,1' : '32,30,22,0.5' },
  process: function (neighbors, x, y) {
    var surrounding = neighbors.filter(function (spot) {
      return spot.creature.alive
    }).length
    this.alive = surrounding === 3 || (surrounding === 2 && this.alive)
    return true
  }
})

terra.registerCA({
  type: 'persian',
  colorFn: function () { return this.alive ? '213,251,200,1' : '20,10,9,1' },
  process: function (neighbors, x, y) {
    if (this.alive) {
      this.alive = false
      return true
    }
    var surrounding = neighbors.filter(function (spot) {
      return spot.creature.alive
    }).length
    this.alive = surrounding === 2 || surrounding === 3 || surrounding === 4
    return true
  }
})
