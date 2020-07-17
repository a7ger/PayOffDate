<template>
    <div>
        <div id="calc-background">
            <div id="debt-list-div">
                <DebtInfo v-for="debt in debts" :key="debt.id" :id="debt.id"></DebtInfo>
                <button id="add-debtInfo-button" @click="addDebtInfo">+</button>
            </div>
            <div id="bottom-half-div">
                <div id="controls-div">
                    <div id="variables-div">
                        <div id="desired-months-div">
                            <div id="desired-months-label-div" class="variable-label-div">
                                <label for="desired-months-input">Payoff in # months</label>
                            </div>
                            <div id="desired-months-input-div">
                                <input type="text" id="desired-months-input" class="variable-input">
                            </div>
                        </div>
                        <div id="variable-or-div">
                            or
                        </div>
                        <div id="desired-extra-payment-div">
                            <div id="desired-extra-payment-label-div" class="variable-label-div">
                                <label for="desired-extra-payment-input">Extra $ per month</label>
                            </div>
                            <div id="desired-extra-payment-input-div">
                                <input type="text" id="desired-extra-payment-input" class="variable-input">
                            </div>
                        </div>
                    </div>
                    <div id="calculate-button-div">
                        <button id="calculate-button">Calculate</button>
                    </div>
                </div>
                <div id="results-div">
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

* {
    font-family: "Roboto";
}

.variable-label-div {
    display: flex;
    justify-content: center;
}

#dumb {
    background-color: black;
}

.variable-input {
    height: 35px;
    border-radius: 5px;
    border-style: none;
    margin-top: 4px;
}

label {
    font-size: 12px;
    color: #BDBDBD;
    justify-self: center;
}

#calculate-button {
    margin-top: 12px;
    background-color: #00A3FF;
    border-radius: .3125rem;
    outline: none;
    border: none;
    height: 2.1875rem;
    width: 100%;
}

#bottom-half-div {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    margin-top: 20px;
}

.is-hover {
    cursor: pointer;
}

#results-div {
    border-radius: .3125rem;
    background-color: white;
    width: 57%;
    display: flex;
    justify-self: right;
}

#calc-background {
    background-color: #454753;
    padding: 1.25rem;
    border-radius: 1rem;
    width: 50rem;
}

#add-debtInfo-button {
    background-color: transparent;
    color: #BDBDBD;
    font-weight: bold;
    font-size: 30px;
    border-style: none;
    outline: none;
    border-radius: 50%;
    margin-left: -6px;
}

#add-debtInfo-button:active {
    text-shadow: .04rem .04rem #ffffff;
}

#controls-div {
    margin-right: 1.25rem;
    flex: 1;
}

#desired-months-div {
    width: 7.5rem;
}

#desired-extra-payment-div {
    width: 7.5rem;
}

#variables-div {
    display: flex;
}

#variable-or-div {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: flex-end;
    color: #BDBDBD;
    padding-bottom: 11px;
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
        debts: [],
    },
    mutations: {
        addDebtInfo(state) {
            state.debts.push({
                id: state.debts.length + 1,
                name: null,
                balance: null,
                minPayment: null,
                apr: null,
            });
        },
        clearDebts(state) {
            state.debts = [];
        },
        removeDebt(state, id) {
            console.log(id);
            var debt = state.debts.find(debt => debt.id === id);
            console.log("item found: " + JSON.stringify(debt));
            var index = state.debts.indexOf(debt);
            console.log("index: " + index);
            console.log("array before: " + JSON.stringify(this.state.debts));
            if (index >= 0) {
                state.debts.splice(index, 1);
            }
            console.log("array after: " + JSON.stringify(this.state.debts));
        },
    },
    getters: {
        debts(state) {
            return state.debts;
        },
    },
    actions: {
        addDebtInfo(state) {
            state.commit("addDebtInfo");
        },
        clearDebts(state) {
            state.commit("clearDebts");
        },
        removeDebt(state, id) {
            state.commit("removeDebt", id);
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
            var maxExtra = this.sumOfBalances(this.debts) - this.sumOfMinPayments(this.debts);
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
            var sortedDebtsCopy = lodash.cloneDeep(this.debts).sort(function(a,b) {
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
            var debtsCopy = lodash.cloneDeep(this.debts);
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
            this.addDebtInfo();
            this.debts[0].name = "stu";
            this.debts[0].balance = 54000;
            this.debts[0].apr = .065;
            this.debts[0].minPayment = 400;
            this.addDebtInfo();
            this.debts[1].name = "cc";
            this.debts[1].balance = 4500;
            this.debts[1].apr = .2299;
            this.debts[1].minPayment = 125;
            this.addDebtInfo();
            this.debts[2].name = "car";
            this.debts[2].balance = 4000;
            this.debts[2].apr = .0299;
            this.debts[2].minPayment = 300;
        },
        parametersChanged() {
            this.showResults = false;
        },
    },
    computed: {
        debts() {
            return store.getters.debts;
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
        //this.createTestData();
    },
}
</script>
