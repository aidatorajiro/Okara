<template>
  <span ref="marker"></span>
</template>

<script>
import terra from 'terra'

export default {
  name: 'terra-automata',
  props: {
    preset: String,
    rows: Number,
    columns: Number,
    periodic: Boolean,
    neighborhood: String,
    trails: Boolean,
    background: String,
    length: Number // length of the animation
  },
  methods: {
    restart: function () {
      if (this.automata !== undefined) {
        this.automata.stop()
        this.automata.destroy()
      }

      var automata = new terra.Terrarium(this.rows, this.columns, {
        insertAfter: this.$refs.marker,
        periodic: this.periodic,
        neighborhood: this.neighborhood,
        trails: this.trails,
        background: this.background
      })
      this.automata = automata

      automata.canvas.style = 'width:100%;'

      automata.grid = automata.makeGrid(this.preset)

      automata.animate(this.length)
    }
  },
  mounted: function () {
    this.restart()
  },
  watch: {
    preset: function () {
      this.restart()
    },
    rows: function () {
      this.restart()
    },
    columns: function () {
      this.restart()
    }
  },
  beforeDestroy: function () {
    this.automata.stop()
    this.automata.destroy()
  }
}
</script>