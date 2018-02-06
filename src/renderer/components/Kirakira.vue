<template>
  <TerraAutomata preset="cyclic" :rows=200 :columns=200 :periodic=true ref="terra" />
</template>

<script>
  import TerraAutomata from './TerraAutomata'
  export default {
    name: 'kirakira',
    components: { TerraAutomata },
    mounted: function () {
      this.automata = this.$refs.terra.automata
      for (let arr of this.automata.grid) {
        for (let cell of arr) {
          cell.state = Math.floor(Math.random() * 16)
        }
      }
    }
  }
</script>