<template>
    <div>
        <input type="text" placeholder="Name your debt" class="nameInput" v-model="nameInput">
        <input type="text" placeholder="Balance" class="balanceInput" v-model="balanceInput">
        <input type="text" placeholder="Min pmnt" class="minInput" v-model="minPaymentInput">
        <input type="text" placeholder="APR" class="aprInput" v-model="aprInput">
    </div>
</template>

<script>

import {store} from './PayOffDateCalculator.vue';

    export default {
        name: 'DebtInfo',
        props: {
            id: Number,
        },
        data: function () {
            return {
                nameInput: null,
                balanceInput: null,
                aprInput: null,
                minPaymentInput: null,
            };
        },
        computed: {
            debtInfo() {
                return store.getters.debtInfos.find(di => di.id == this.id);
            }
        },
        watch: {
            nameInput(val){
                this.debtInfo.name = val;
            },
            balanceInput(val) {
                this.debtInfo.balance = parseFloat(val);
            },
            aprInput(val) {
                this.debtInfo.apr = parseFloat(val);
            },
            minPaymentInput(val) {
                this.debtInfo.minPayment = parseFloat(val);
            }
        },
    }
</script>

<style scoped>
    .nameInput {
        width: 200px !important;
    }
    .balanceInput {
        width: 50px !important;
    }
    .minInput {
        width: 50px !important;
    }
    .aprInput {
        width: 50px !important;
    }
</style>