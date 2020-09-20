<template>
    <div>
        <div id="calc-background">
            <div id="debt-list-div">
                <DebtInfo v-for="debt in debts" :key="debt.id" :id="debt.id" @input="resetResults" @delete="resetResults"></DebtInfo>
                <p v-if="debts.length <= 0">Add your first debt!</p>
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
                                <input type="text" id="desired-months-input" class="variable-input" v-model="numMonthsDesiredInput" @input="desiredMonthsInputChanged">
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
                                <input type="text" id="desired-extra-payment-input" class="variable-input" v-model="extraMonthlyFundsInput" @input="desiredExtraPmntInputChanged">
                            </div>
                        </div>
                    </div>
                    <div id="calculate-button-div">
                        <button id="calculate-button" class="action-button" @click="goClicked">Calculate</button>
                    </div>
                </div>
                <div id="results-div">
                    <div v-if="results.payOffDateMinPayments">
                        Fade out Min payments: {{results.payOffDateMinPayments}}<br />
                    </div>
                    <div v-if="results.payOffDateSnowBallNoExtra">
                        Snow Ball min payments: {{results.payOffDateSnowBallNoExtra}}<br />
                    </div>
                    <div v-if="results.payOffDateSnowBallWithExtra">
                        Snow Ball with extra: {{results.payOffDateSnowBallWithExtra}}
                    </div>
                    <div v-if="results.extraPaymentNeeded">
                        Extra payment per month needed: {{results.extraPaymentNeeded}}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

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

    input {
        text-align: center;
    }

    label {
        font-size: 12px;
        justify-self: center;
    }

    #calculate-button {
        margin-top: 12px;
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
        padding: 10px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    #calc-background {
        background-color: #EDEDED;
        padding: 1.25rem;
        border-radius: 1rem;
        width: 50rem;
    }

    #add-debtInfo-button {
        font-size: 30px;
        border-style: none;
        padding: 0px;
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
        padding-bottom: 11px;
    }
</style>


<script>

import DebtInfo from './DebtInfo.vue';
import lodash from 'lodash';
import store from '@/stores/CalcStore.js';
import Axios from 'axios';

export default {
    name: 'PayOffDateCalculator',
    components: {
        DebtInfo,
    },
    data() {
        return {
            results: {
                payOffDateMinPayments: null,
                payOffDateSnowBallNoExtra: null,
                payOffDateSnowBallWithExtra: null,
                extraPaymentNeeded: null,
            },
            addDebtButtonHover: false,
            extraMonthlyFundsInput: null,
            extraMonthlyFunds: 0,
            numMonthsDesiredInput: null,
            numMonthsDesired: null,
        }
    },
    methods: {
        addDebtInfo() {
            this.resetResults();
            store.dispatch("addDebtInfo");
        },
        clearDebts() {
            store.dispatch("clearDebts");
        },
        isValidDebts(debts) {
            if (!debts.every(debt => {
                if (!debt.name || !debt.balance) {
                    return false;
                }
                return true
            })) {
                return false;
            }

            var name = [];
            if (!this.debts.every(debt => this.isValidMinPmnt(debt, name)) && name.length > 0) {
                alert("The minimum paymnet for your debt named \"" + name[0] + "\" is too low. Your balance would increase monthly with that balance, apr and minimum payment combination.");
                return false;
            }
            return true;
        },
        goClicked() {
            if (!this.isValidDebts(this.debts)) {
                alert("Oops! Make sure you name all your debts and include their non-zero balances!")
                return;
            }

            Axios.post('http://localhost:5000/save-debts', {
                email: "zackalger@gmail.com",
                debts: this.debts,
            })

            this.resetResults();
            if (this.numMonthsDesired) {
                this.results.extraPaymentNeeded = Math.ceil(this.calculateExtraPaymentNeeded(this.numMonthsDesired));
            } else {
                this.calculatePayOffDates();
            }
        },
        calculatePayOffDates() {
            this.results.payOffDateMinPayments = this.convertMonthsToDate(this.calculateNumMonthsMinPayments());
            this.results.payOffDateSnowBallNoExtra = this.convertMonthsToDate(this.calculateNumMonthsSnowball(0));
            if (this.extraMonthlyFunds != null && this.extraMonthlyFunds > 0) {
                this.results.payOffDateSnowBallWithExtra = this.convertMonthsToDate(this.calculateNumMonthsSnowball(this.extraMonthlyFunds));
            } else {
                this.results.payOffDateSnowBallWithExtra = null;
            }
        },
        convertMonthsToDate(numMonths){
            if (!numMonths) {
                return null;
            }
            var today = new Date();
            var newDate = new Date();
            newDate.setMonth(today.getMonth() + numMonths);
            
            return newDate.toLocaleDateString();
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

            while (this.sumOfBalances(sortedDebtsCopy) >= 0.01) {
                numMonths++;
                var monthlyFundsCopy = monthlyFunds;
                
                // calc new balances after 1 month interest and pay min payments
                for (var debt of sortedDebtsCopy) {
                    if (debt.balance >= 0.01){
                        debt.balance = this.addOneMonthInterest(debt.balance, debt.apr);
                        if (debt.balance <= debt.minPayment) {
                            debt.balance = 0;
                            monthlyFundsCopy = this.roundToNumDecimals(monthlyFundsCopy - debt.balance, 3);
                        } else {
                            debt.balance = this.roundToNumDecimals(debt.balance - debt.minPayment, 3);
                            monthlyFundsCopy = this.roundToNumDecimals(monthlyFundsCopy - debt.minPayment, 3);
                        }
                    }
                }

                // distribute remaining funds starting at the lowest balance debt
                while (monthlyFundsCopy >= 0.01 && this.sumOfBalances(sortedDebtsCopy) >= 0.01) {
                    for (var debt_ of sortedDebtsCopy) {
                        if (debt_.balance >= 0.01){
                            if (debt_.balance <= monthlyFundsCopy) {
                                debt_.balance = 0;
                                monthlyFundsCopy = this.roundToNumDecimals(monthlyFundsCopy - debt_.balance, 3);
                            } else {
                                debt_.balance = this.roundToNumDecimals(debt_.balance - monthlyFundsCopy, 3);
                                monthlyFundsCopy = 0;
                            }
                        }
                    }
                }
            }
            return numMonths;
        },
        calculateNumMonthsMinPayments() {
            var debtsCopy = lodash.cloneDeep(this.debts);
            var numMonths = 0;

            while (this.sumOfBalances(debtsCopy) >= 0.01) {
                numMonths++;
                
                // calc new balances after 1 month interest and min payments
                for (var debt of debtsCopy) {
                    if (debt.balance > 0){
                        debt.balance = this.addOneMonthInterest(debt.balance, debt.apr);
                        if (debt.balance <= debt.minPayment){
                            debt.balance = 0;
                        } else {
                            debt.balance -= debt.minPayment;
                        }
                    }
                }
            }
            return numMonths;
        },
        sumOfMinPayments(debts) {
            var sum = 0;
            for (var debt of debts) {
                sum += debt.minPayment;
            }
            return sum;
        },
        sumOfBalances(debts) {
            var sum = 0;
            for (var debt of debts) {
                sum += debt.balance;
            }
            return sum;
        },
        addOneMonthInterest(balance, apr) {
            /* continuos compounding interest formula.
            12 is for 12 months in a year */
            apr = apr/100.00
            return this.roundToNumDecimals(balance * Math.exp(apr/12), 3);
        },
        roundToNumDecimals(val, numDecimals) {
            val *= Math.pow(10, numDecimals);
            val = Math.floor(val);
            return val / Math.pow(10, numDecimals);
        },
        resetResults() {
            //console.log("before: " + JSON.stringify(this.results));
            Object.keys(this.results).forEach(resultName => this.results[resultName] = null);
            //console.log("after: " + JSON.stringify(this.results));
        },
        desiredExtraPmntInputChanged() {
            this.numMonthsDesiredInput = null;
            this.resetResults();
        },
        desiredMonthsInputChanged() {
            this.extraMonthlyFundsInput = null;
            this.resetResults();
        },
        isValidMinPmnt(debt, name) {
            var newBalance = this.addOneMonthInterest(debt.balance, debt.apr);
            newBalance -= debt.minPayment;
            if (newBalance > debt.balance) {
                name.push(debt.name);
                return false;
            }
            return true;
        }
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
        },
    },
}
</script>
