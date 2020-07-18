<template>
    <div>
        <div class="row">
            <div class="row-input-section">
                <div class="label-input-div">
                    <label for="nameInput" class="nameInputLabel">Name</label>
                    <input type="text" class="nameInput" v-model="nameInput">
                </div>
                <div class="label-input-div">
                    <label for="balanceInput" class="balanceInputLabel">Balance</label>
                    <input type="text" class="balanceInput" v-model="balanceInput">
                </div>
                <div class="label-input-div">
                    <label for="aprInput" class="aprInputLabel">APR</label>
                    <input type="text" class="aprInput" v-model="aprInput">
                    <div class="aprPercentSignDiv">
                        %
                    </div>
                </div>
                <div class="label-input-div">
                    <label for="minPaymentInput" class="minPaymentInputLabel">Min Pmnt</label>
                    <input type="text" class="minPaymentInput" v-model="minPaymentInput">
                </div>
            </div>
            <div class="remove-button-div">
                <button class="remove-button" @click="removeDebt">✖</button>
            </div>
        </div>
    </div>
</template>

<style scoped>

    .aprPercentSignDiv {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        margin-left: -30px;
        margin-right: 19px;
    }

    .nameInputLabel {
        width: 55px;
    }

    .balanceInputLabel {
        width: 60px;
    }

    .aprInputLabel {
        width: 41px;
    }

    .minPaymentInputLabel {
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

    .remove-button {
        background-color: transparent;
        border-style: none;
        font-size: 12px;
        font-weight: bold;
    }

    .remove-button-div {
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
        text-align: center;
    }

    .nameInput {
        width: 138px;
    }
    .balanceInput {
        width: 133px;
    }

    .aprInput {
        width: 85px;
        padding-right: 16px;
    }

    .minPaymentInput {
        width: 115px;
        margin-right: 0px;
    }

</style>

<script>

import store from '@/stores/CalcStore.js';

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
                this.debtInfo.apr = parseFloat(val)/100.00; // divide by 100 to convert from percentage to decimal
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
