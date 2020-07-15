<template>
    <div @input="parametersChanged">
        <div id="calcBackground">
            <button @click="createTestData">Fill with test data</button>
            <div v-for="debtInfo of debtInfos" :key="debtInfo.id">
                <DebtInfo :id="debtInfo.id"></DebtInfo>   
            </div>
            <div id="addDebtButon">
                <img src="../../public/plus-sign_64.jpg" alt="plus sign button" @mouseover="addDebtButtonHover = true" 
                @mouseleave="addDebtButtonHover = false" :class="{isHover:addDebtButtonHover}" @click="addDebtInfo">
            </div>
            <div>
                <div>
                    <label for="extraMonltyFundsInput">Pay Extra per Month</label>
                    <input type="text" v-model="extraMonthlyFundsInput" id="extraMonthlyFundsInput" @input="numMonthsDesiredInput = null">
                </div>
                or<br />
                <div>
                    <label for="numMonthsDesiredInput">Get debt free in how many months</label>
                    <input type="text" v-model="numMonthsDesiredInput" id="numMonthsDesiredInput" @input="extraMonthlyFundsInput = null">
                </div>
            </div>
            
            <div @click="goClicked">
                <button>GO!</button>
                <div v-if="showResults">
                    Fade out Min payments: {{payOffDateMinPayments}}<br />
                    Snow Ball min payments: {{payOffDateSnowBallNoExtra}}<br />
                    <div v-if="payOffDateSnowBallWithExtra != null">
                        Snow Ball with extra: {{payOffDateSnowBallWithExtra}}
                    </div>
                </div>
                <div v-if="extraPaymentNeeded != null">
                    Extra payment per month needed: {{extraPaymentNeeded}}
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

.isHover {
    cursor: pointer;
}

#calcBackground {
    background-color: #454753;
    padding: 1.25rem;
    border-radius: 1rem;
}

</style>

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
        },
        clearDebts(state) {
            state.debtInfos = [];
        },
    },
    getters: {
        debtInfos(state) {
            return state.debtInfos;
        },
    },
    actions: {
        addDebtInfo(state) {
            state.commit("addDebtInfo");
        },
        clearDebts(state) {
            state.commit("clearDebts");
        }
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
            payOffDateMinPayments: null,
            showResults: false,
            payOffDateSnowBallNoExtra: null,
            payOffDateSnowBallWithExtra: null,
            numMonthsDesiredInput: null,
            numMonthsDesired: null,
            extraPaymentNeeded: null,
        }
    },
    methods: {
        addDebtInfo: function () {
            store.dispatch("addDebtInfo");
        },
        clearDebts() {
            store.dispatch("clearDebts");
        },
        goClicked() {
            if (this.numMonthsDesired != null) {
                this.extraPaymentNeeded = Math.ceil(this.calculateExtraPaymentNeeded(this.numMonthsDesired));
            } else {
                this.calculatePayOffDates();
            }
        },
        calculatePayOffDates() {
            this.payOffDateMinPayments = this.convertMonthsToDate(this.calculateNuMonthsMinPayments());
            this.payOffDateSnowBallNoExtra = this.convertMonthsToDate(this.calculateNumMonthsSnowball(0));
            if (this.extraMonthlyFunds != null && this.extraMonthlyFunds > 0) {
                this.payOffDateSnowBallWithExtra = this.convertMonthsToDate(this.calculateNumMonthsSnowball(this.extraMonthlyFunds));
            } else {
                this.payOffDateSnowBallWithExtra = null;
            }
            this.showResults = true;
        },
        convertMonthsToDate(months){
            // todo
            return months;
        },
        calculateExtraPaymentNeeded(targetMonths) {
            if (targetMonths <= 0) {
                alert("You must choose a number of months of 1 or more!");
            }
            var maxExtra = this.sumOfBalances(this.debtInfos) - this.sumOfMinPayments(this.debtInfos);
            var minExtra = 0;
            var curMonths = this.calculateNumMonthsSnowball(0);

            if (targetMonths > curMonths) {
                alert("If you just pay your minimum payments you will beat your goal and be debt free in " + curMonths + "!");
                return;
            }
            
            var curExtra = this.calcCurExtra(maxExtra, minExtra);
            
            while((curMonths = this.calculateNumMonthsSnowball(curExtra)) != targetMonths) {
                if (curMonths > targetMonths) {
                    minExtra = curExtra;
                    curExtra = this.calcCurExtra(minExtra, maxExtra);
                } else {
                    maxExtra = curExtra;
                    curExtra = this.calcCurExtra(minExtra, maxExtra);
                }
            }
            return curExtra;
        },
        calcCurExtra(minExtra, maxExtra) {
            return (minExtra + maxExtra) / 2;
        },
        calculateNumMonthsSnowball(extraMonthlyFunds) {
            var sortedDebtsCopy = lodash.cloneDeep(this.debtInfos).sort(function(a,b) {
                return parseInt(a.balance) - parseInt(b.balance);
            });
            var numMonths = 0;
            var monthlyFunds = this.sumOfMinPayments(sortedDebtsCopy) + extraMonthlyFunds;

            while (this.sumOfBalances(sortedDebtsCopy) > 0) {
                numMonths++;
                var monthlyFundsCopy = monthlyFunds;
                
                // calc new balances after 1 month interest and pay min payments
                for (var debt of sortedDebtsCopy) {
                    if (debt.balance > 0){
                        var paymentAmount = Math.min(debt.balance, debt.minPayment);
                        debt.balance = this.addOneMonthInterest(debt.balance, debt.apr) - paymentAmount;
                        monthlyFundsCopy -= paymentAmount;
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
            return numMonths;
        },
        calculateNuMonthsMinPayments: function () {
            var debtsCopy = lodash.cloneDeep(this.debtInfos);
            var numMonths = 0;

            while (this.sumOfBalances(debtsCopy) > 0) {
                numMonths++;
                
                // calc new balances after 1 month interest and min payments
                for (var debt of debtsCopy) {
                    if (debt.balance > 0){
                        debt.balance = this.addOneMonthInterest(debt.balance, debt.apr) - Math.min(debt.balance, debt.minPayment);
                    }
                }
            }
            return numMonths;
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
            this.clearDebts();
            this.addDebtInfo();
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
        },
        parametersChanged() {
            this.showResults = false;
        },
    },
    computed: {
        debtInfos() {
            return store.getters.debtInfos;
        },
    },
    watch: {
        extraMonthlyFundsInput(val) {
            if (val == ""){
                this.extraMonthlyFunds = null;
            } else {
                this.extraMonthlyFunds = parseFloat(val);
            }
        },
        numMonthsDesiredInput(val) {
            if (val != "" && val != null){
                this.numMonthsDesired = Math.floor(parseFloat(val));
            } else {
                this.numMonthsDesired = null;
            }
        }
    },
    created() {
        //this.addDebtInfo();
    },
}
</script>
