<template>
  <div id="app">
    <Authenticator></Authenticator>
    <button @click="saveDebtsButtonClicked" class="action-button">Save Debts</button>
    <PayOffDateCalculator id="calc"></PayOffDateCalculator>
    <!-- <todo></todo> -->
  </div>
</template>


<script>
  import PayOffDateCalculator from './components/PayOffDateCalculator.vue'
  import Authenticator from './components/Authenticator.vue'
  import Axios from 'axios';
  import store from '@/stores/CalcStore.js';

  export default {
    name: 'App',
    components: {
      PayOffDateCalculator,
      Authenticator,
    },
    methods: {
      saveDebtsButtonClicked: function() {
        Axios.post('http://157.245.163.181:5000/save-debts', {
          email: store.getters.loggedInEmail,
          debts: store.getters.debts,
        })
      },
    }
  }
</script>

<style scoped>
  #app {
    display: flex;
    align-content: center;
    align-items: center;
    justify-content: center;
    justify-items: center;
    flex-direction: column;
  }
</style>

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
  }

  button:hover {
    cursor: pointer;
  }

  .action-button {
    background-color: #00A3FF;
    border-radius: .3125rem;
    outline: none;
    border: none;        
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
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
