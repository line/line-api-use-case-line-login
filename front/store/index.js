export const state = ()=>({
    started: null,
    locales: ['ja'],
    locale: 'ja',
    sessionId: null,
    lineUser: null,
});

export const mutations = {
    clear(state) {
        state.started = null;
        state.locale = 'ja';
        state.sessionId = null;
        state.lineUser = null;
    },
    started(state, started) {
        state.started = started;
    },
    locale(state, locale) {
        if (state.locales.includes(locale)) {
            state.locale = locale;
        }
    },
    session(state, sessionId) {
        state.sessionId = sessionId;
    },
    lineUser(state, lineUser) {
        state.lineUser = lineUser;
    },
};
