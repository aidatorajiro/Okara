<template>
  <canvas ref="canvas" width=200 height=200></canvas>
</template>

<script>
export default {
  name: 'my-automata',
  data () {
    return {n: 200, m: 200}
  },
  methods: {
    init_map () {
      this.map = []
      for (let i = 0; i < this.n; i++) {
        this.map.push([])
        for (let j = 0; j < this.m; j++) {
          this.map[i].push(0)
        }
      }
    },
    nextgeneration () {
      const copy = v.slice()
      for (let i = 1; i < this.n - 1; i++) {
        for (let j = 1; j < this.m - 1; j++) {
          const a = this.map[i - 1][j - 1]
          const b = this.map[i][j - 1]
          const c = this.map[i + 1][j - 1]
          const d = this.map[i - 1][j]
          const e = this.map[i + 1][j]
          const f = this.map[i - 1][j + 1]
          const g = this.map[i][j + 1]
          const h = this.map[i + 1][j + 1]
          const s = a + b + c + d + e + f + g + h
          if (s > 0) {
            // this.map[i][j] = 1
          }
        }
      }
    },
    draw () {
      const ctx = this.$refs.canvas.getContext('2d')
      ctx.beginPath()
      ctx.fillStyle = 'rgb(155, 187, 89)'
      for (let i = 0; i < this.n; i++) {
        for (let j = 0; j < this.m; j++) {
          if (this.map[i][j] === 1) {
            ctx.fillRect(i, j, 1, 1)
          }
        }
      }
    }
  },
  created () {
    this.init_map()
    this.map[20][20] = 1
    this.nextgeneration()
    this.nextgeneration()
    this.nextgeneration()
    this.nextgeneration()
  },
  mounted () {
    this.draw()
  }
}
</script>