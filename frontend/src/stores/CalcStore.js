import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
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
            var debt = state.debts.find(debt => debt.id === id);
            var index = state.debts.indexOf(debt);
            if (index >= 0) {
                state.debts.splice(index, 1);
            }
        },
        setDebts(state, debts) {
            state.debts = debts
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
        setDebts(state, debts) {
            state.commit("setDebts", debts)
        }
    },
});