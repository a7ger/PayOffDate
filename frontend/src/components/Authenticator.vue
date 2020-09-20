<template>
    <div id="body">
        <div v-if="isLoggedIn">
            logged in as: {{loggedInUser.firstName}}
        </div>
        <div id="button-div" v-else>
            <input type="text" placeholder="email" v-model="inputs.email">
            <input type="password" placeholder="password" v-model="inputs.password">
            <button class="action-button local-button" @click="signInClicked">Sign In</button>
        </div>
    </div>
</template>

<style scoped>
    
    .local-button{
        color: black;
        height: 100%;
        width: 100px;
    }

    #body {
        height: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

</style>>

<script>
    import axios from 'axios';
    import store from '@/stores/CalcStore.js';

    export default {
        name: 'authenticator',
        props: {
            // add props to be passed in on construction here
        },
        data: function () {
            return {
                inputs: {
                    email: "",
                    password: "",
                },
                isLoggedIn: false,
                loggedInUser: {
                    firstName: "",
                    debts: [],
                }
            };
        },
        methods: {
            signInClicked: function () {
                var that = this
                axios.post('http://localhost:5000/sign_in', this.inputs).then(function (res) {
                    that.loggedInUser.firstName = res.data.firstName
                    that.isLoggedIn = true
                    // console.log(res.data.debts)
                    store.dispatch('setDebts', res.data.debts)
                })
            },
        },
        watch: {
            data: function (val) {
                console.log(val)
            }
        }
    }
</script>