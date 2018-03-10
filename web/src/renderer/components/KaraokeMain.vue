<template>
  <div id="wrapper">
    <main>
      <!--<Jutan    v-if="currentType == 'jutan'"></Jutan>
      <Jutan2   v-if="currentType == 'jutan2'"></Jutan2>
      <Kirakira v-if="currentType == 'kirakira'"></Kirakira>-->
      <MyAutomata></MyAutomata>
    </main>
  </div>
</template>

<script>
  // 歌うことで誕生日を迎えて人工生命体が育つ
  import Kirakira from './Kirakira'
  import Jutan from './Jutan'
  import Jutan2 from './Jutan2'
  import MyAutomata from './MyAutomata'
  import _ from 'lodash'
  export default {
    name: 'karaoke-main',
    components: { Kirakira, Jutan, Jutan2, MyAutomata },
    data: function () {
      return {
        scenario: [],
        framecount: 0,
        currentSceneIndex: -1,
        currentType: '',
        frameleft: 0 // remaining frame to change scene
      }
    },
    methods: {
      run: function () {
        // screen management func
        this.framecount++
        if (this.frameleft === 0) {
          this.currentSceneIndex++
          const scene = this.scenario[this.currentSceneIndex % this.scenario.length]
          this.currentType = scene.type
          this.frameleft = scene.length
        } else {
          this.frameleft--
        }
        requestAnimationFrame(this.run)
      }
    },
    mounted: function () {
      // create scenario for this time
      for (let i = 0; i < 100; i++) {
        this.scenario[i] = {
          length: _.random(4, 40),
          type: _.sample(['jutan', 'jutan2', 'kirakira'])
        }
      }
      // run
      this.run()
    }
  }
</script>

<style>
  body {
    margin: 0;
    background: #222222;
    overflow: hidden;
  }
</style>
