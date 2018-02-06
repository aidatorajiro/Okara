<template>
  <canvas style="width: 100%;"></canvas>
</template>

<script>
export default {
  name: 'my-automata',
  props: {
    'rows': Number,
    'columns': Number
  },
  data: function () {
    return { map: undefined }
  },
  methods: {
    init: function () {
      for (let i = 0; i < this.rows; i++) {
        this.map.push([])
        for (let j = 0; j < this.columns; j++) {
          this.map[i][j] = 0
        }
      }
    },
    animate: function () {

    }
  },
  beforeMounted: function () {
    this.init()
  },
  mounted: function () {
    this.animate()
  }
}
</script>