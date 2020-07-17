<template>
  <div id="app">
    <PayOffDateCalculator id="calc"></PayOffDateCalculator>
    <!-- <todo></todo> -->
  </div>
</template>


<script>
import PayOffDateCalculator from './components/PayOffDateCalculator.vue'
// import todo from './components/todo.vue'
export default {
  name: 'App',
  components: {
    PayOffDateCalculator
    // todo,
  },
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Roboto');

* {
    outline: none;
    max-width: 100%;
    box-sizing: border-box;
}
</style>

<style scoped>
#app {
  display: flex;
  justify-content: center;
}

#calc {
  margin-top: 25px;
}
</style>
