<template>
    <div>
        <div v-for="debtInfo of debtInfos" :key="debtInfo.id">
            <DebtInfo :id="debtInfo.id"></DebtInfo>   
        </div>
        <div id="addDebtButon">
            <img src="../../public/plus-sign_64.jpg" alt="plus sign button" @mouseover="addDebtButtonHover = true" 
                @mouseleave="addDebtButtonHover = false" :class="{isHover:addDebtButtonHover}" @click="addDebtInfo">
        </div>
        <div>
            <input type="text" v-model="extraMonthlyFundsInput">
        </div>
        <div @click="calculatePayoffDate">
            <button>Calculate Number of months until you're debt free.</button>
            <div v-if="showNumberOfMonthsTilldebtFree">
                {{numberOfMonthsTillDebtFree}}
            </div>
        </div>
    </div>
</template>

<script>

import DebtInfo from './DebtInfo.vue';
import Vue from 'vue';
import Vuex from 'vuex';
import lodash from 'lodash';

Vue.use(Vuex);

export const store = new Vuex.Store({
    state: {
        debtInfos: [],
    },
    mutations: {
        addDebtInfo(state) {
            state.debtInfos.push({
                id: state.debtInfos.length + 1,
                name: null,
                balance: null,
                minPayment: null,
                apr: null,
            });
        }
    },
    getters: {
        debtInfos(state) {
            return state.debtInfos;
        },
        // sortedDebts(state) {
        //     var res = lodash.cloneDeep(state.debtInfos).sort(function(a,b) {
        //         return a.balance - b.balance;
        //     });
        //     return res;
        // },
    },
    actions: {
        addDebtInfo(state) {
            state.commit("addDebtInfo");
        },
    },
});

export default {
    name: 'PayOffDateCalculator',
    components: {
        DebtInfo,
    },
    data: function() {
        return {
            addDebtButtonHover: false,
            extraMonthlyFundsInput: null,
            extraMonthlyFunds: 0,
            numberOfMonthsTillDebtFree: null,
            showNumberOfMonthsTilldebtFree: false,
        }
    },
    methods: {
        addDebtInfo: function () {
            store.dispatch("addDebtInfo");
        },
        calculatePayoffDate: function () {
            var sortedDebtsCopy = lodash.cloneDeep(this.debtInfos).sort(function(a,b) {
                return parseInt(a.balance) - parseInt(b.balance);
            });
            var numMonths = 0;
            var monthlyFunds = this.sumOfMinPayments(sortedDebtsCopy) + this.extraMonthlyFunds;

            while (this.sumOfBalances(sortedDebtsCopy) > 0) {
                numMonths++;
                var monthlyFundsCopy = monthlyFunds;
                
                // calc new balances after 1 month interest and pay min payments
                for (var debt of sortedDebtsCopy) {
                    if (debt.balance > 0){
                        debt.balance = this.addOneMonthInterest(debt.balance, debt.apr) - debt.minPayment;
                        monthlyFundsCopy -= debt.minPayment;
                    }
                }

                // distribute remaining funds starting at the lowest balance debt
                while (monthlyFundsCopy > 0 && this.sumOfBalances(sortedDebtsCopy) > 0) {
                    for (var debt_ of sortedDebtsCopy) {
                        if (debt_.balance > 0){
                            var creditAmount = Math.min(debt_.balance, monthlyFundsCopy);
                            debt_.balance -= creditAmount;
                            monthlyFundsCopy -= creditAmount;
                        }
                    }
                }
            }
            this.numberOfMonthsTillDebtFree = numMonths;
            this.showNumberOfMonthsTilldebtFree = true;
        },
        sumOfMinPayments: function(debts) {
            var sum = 0;
            for (var debt of debts) {
                sum += debt.minPayment;
            }
            return sum;
        },
        sumOfBalances: function (debts) {
            var sum = 0;
            for (var debt of debts) {
                sum += debt.balance;
            }
            return sum;
        },
        addOneMonthInterest: function (balance, apr) {
            /* continuos compounding interest formula.
            12 is for 12 months in a year */
            return balance * Math.exp(apr/12);
        },
        createTestData() {
            this.addDebtInfo();
            this.addDebtInfo();
            this.debtInfos[0].name = "stu";
            this.debtInfos[0].balance = 54000;
            this.debtInfos[0].apr = .065;
            this.debtInfos[0].minPayment = 400;
            this.debtInfos[1].name = "cc";
            this.debtInfos[1].balance = 4500;
            this.debtInfos[1].apr = .2299;
            this.debtInfos[1].minPayment = 125;
            this.debtInfos[2].name = "car";
            this.debtInfos[2].balance = 4000;
            this.debtInfos[2].apr = .0299;
            this.debtInfos[2].minPayment = 300;
        }
    },
    computed: {
        debtInfos() {
            return store.getters.debtInfos;
        },
    },
    watch: {
        extraMonthlyFundsInput(val) {
            this.extraMonthlyFunds = parseFloat(val);
        },
    },
    created() {
        this.addDebtInfo();
        this.createTestData();
    },
}
</script>

<style scoped>

.isHover{
    cursor: pointer;
}

</style>