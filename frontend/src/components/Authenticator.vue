<template>
    <div>
        {{str}}
    </div>
</template>

<style scoped>
    div {
        color: red;
    }
</style>>

<script>
    import axios from 'axios';
    //import store from '@/stores/CalcStore.js';

    export default {
        name: 'authenticator',
        props: {
            // add props to be passed in on construction here
        },
        data: function () {
            return {
                str: "didn't work.",
            };
        },
        methods: {
            test: function () {
                var that = this
                axios.get('http://localhost:5000/hello_world').then(function (res) {
                    console.log(res)
                    that.str = res.data
                    console.log('passed')
                })
            },
        },
        computed: {
        },
        created() {
            this.str = this.test()
        },
    }
</script>