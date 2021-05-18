/**
 * Axios拡張プラグイン
 *
 * @param {Object} $axios
 * @param {Object} store
 */
export default({ $axios, app, store, env }) => {
    /** @type {Object} ロケール */
    let _i18n = app.i18n.messages[store.state.locale];

    // リクエスト拡張
    $axios.onRequest((config)=>{

    });
    // レスポンス拡張
    $axios.onResponse((response)=>{

    });
    // エラー拡張
    $axios.onError((error)=>{
        // HTTP 403 Topへ画面遷移
        if (error.response && error.response.status == 403) {
            const errmsg = _i18n.login.msg009;
            window.alert(errmsg);
            store.commit("lineUser", null);
            if (liff) liff.logout();
            window.location = env.LOGOUT_URL;
            return true;
        }
    });
}
    