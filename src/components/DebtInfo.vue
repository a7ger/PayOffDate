<template>
    <div>
        <div class="row">
            <div class="idDiv">
                {{debtInfo.id}}.
            </div>
            <div class="row-input-section">
                <div class="label-input-div">
                    <label for="nameInput" id="nameInputLabel">Name</label>
                    <input type="text" id="nameInput" v-model="nameInput">
                </div>
                <div class="label-input-div">
                    <label for="balanceInput" id="balanceInputLabel">Balance</label>
                    <input type="text" id="balanceInput" v-model="balanceInput">
                </div>
                <div class="label-input-div">
                    <label for="aprInput" id="aprInputLabel">APR</label>
                    <input type="text" id="aprInput" v-model="minPaymentInput">
                </div>
                <div class="label-input-div">
                    <label for="minPaymentInput" id="minPaymentInputLabel">Min Pmnt</label>
                    <input type="text" id="minPaymentInput" v-model="aprInput">
                </div>
            </div>
            <div id="remove-button-div">
                <button id="remove-button" @click="removeDebt">✖</button>
            </div>
        </div>
    </div>
</template>

<style scoped>

    .idDiv {
        display: flex;
        flex-direction: row;
        align-items: center;
        color: #BDBDBD;
        height: 35px;
        width: 37px;
        font-weight: bold;
        font-size: 18px;
    }

    #nameInputLabel {
        width: 55px;
    }

    #balanceInputLabel {
        width: 60px;
    }

    #aprInputLabel {
        width: 41px;
    }

    #minPaymentInputLabel {
        width: 67px;
    }

    .row-input-section {
        display: flex;
        flex-direction: row;
    }

    label {
        font-size: 12px;
        color: black;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        border-radius: 5px 0px 0px 5px;
        background-color: #BAE5FD;
    }

    .label-input-div {
        display: flex;
        flex-direction: row;
    }

    #remove-button {
        background-color: transparent;
        color: #BDBDBD;
        border-style: none;
        font-size: 20px;
        font-weight: bold;
    }

    #remove-button-div {
        display: flex;
        align-items: flex-start;
        justify-content: center;
        flex-direction: column;
        flex: 1;
    }

    .row {
        display: flex;
        margin-bottom: 12px;
    }

    input {
        border-radius: 0px 5px 5px 0px;
        border-style: none;
        height: 35px;
        margin-right: 16px;
    }

    #nameInput {
        width: 138px;
    }
    #balanceInput {
        width: 117px;
    }

    #aprInput {
        width: 68px;
    }

    #minPaymentInput {
        width: 100px;
        margin-right: 0px;
    }

</style>

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
        methods: {
            removeDebt() {
                store.dispatch("removeDebt", this.id);
            },
        },
        computed: {
            debtInfo() {
                return store.getters.debts.find(di => di.id == this.id);
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
        created() {
            this.nameInput = this.debtInfo.name;
            this.balanceInput = this.debtInfo.balance;
            this.aprInput = this.debtInfo.apr;
            this.minPaymentInput = this.debtInfo.minPayment;
        },
    }
</script>
