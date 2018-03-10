<template>
  <TerraAutomata preset="persian" :rows=200 :columns=200 :periodic=true ref="terra" />
</template>

<script>
  import TerraAutomata from './TerraAutomata'
  import _ from 'lodash'
  export default {
    name: 'jutan',
    components: { TerraAutomata },
    mounted: function () {
      this.automata = this.$refs.terra.automata
      const x = _.random(0, 100)
      const y = _.random(0, 100)
      this.automata.grid[x][y].alive = true
      this.automata.grid[x][y + 1].alive = true
      this.automata.grid[x + 1][y].alive = true
      this.automata.grid[x + 1][y + 1].alive = true
    }
  }
</script>