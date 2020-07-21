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

:root {
    --dark-font-color: #5F5F5F;
}

* {
    outline: none;
    max-width: 100%;
    box-sizing: border-box;
    font-family: 'Roboto';
    color: var(--dark-font-color);
}

button:hover {
  cursor: pointer;
}

.text-button {
  text-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
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
