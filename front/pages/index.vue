<template>
    <v-app class="font-size">
        <h1 class="message mb-1">Welcome to LINE!</h1>
        <v-container class="mb-10">
            <v-row justify="center" style="margin:0 auto; width:98%; "> 
                <p style="font-size:0.8em; padding:6px;">{{ $t("login.msg001") }}</p>
                <div style="max-width:800px;">
                    <div style="width:100%; text-align:left; font-size:0.8em;">【{{ $t("login.msg002") }}】</div>
                    <table style="width:98%;">
                        <tr>
                            <td style="width:40%;">{{ $t("login.msg003") }}</td>
                            <td style="width:60%;">{{ lineUser ? lineUser.name : null }}</td>
                        </tr>
                        <tr>
                            <td>{{ $t("login.msg004") }}</td>
                            <td>
                                <div v-if="lineUser && lineUser.image">
                                <v-img max-width="100" v-bind:src="lineUser ? lineUser.image : null" />
                                </div>
                                <div v-else>
                                <span style="font-size:0.5em;">{{ $t("login.msg005") }}</span>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>{{ $t("login.msg006") }}</td>
                            <td>{{ lineUser ? lineUser.userId : null }}</td>
                        </tr>
                    </table>
                    <p style="color:red; font-size:0.6em; padding:6px;">{{ $t("login.msg007") }}</p>
                </div>
            </v-row>
        </v-container>
        <!-- ボタン -->
        <v-footer fixed class="pa-0" height="60px">
            <v-btn class="text-h5 font-weight-bold" color="#00B900" v-on:click="back" style="color:#fff; width:100%; height:100%;">
                <span style="text-transform:none; letter-spacing:0.06em;" v-html="$t('login.msg008')"></span>
            </v-btn>
        </v-footer>
    </v-app>
</template>

<script>
export default {
    layout: "login",
    async asyncData(context) {

        return {
            stage: context.env.APIGATEWAY_STAGE,
        }
    },
    async fetch(context) {

    },
    head() {
        return {
            title: this.$t("title")
        }
    },
    data() {
        return {
            lineUser: null,
            stage: null,
        }
    },
    created() {

    },
    mounted() {
        this.$nextTick(()=>{
            // LIFF Initialize Ready
            liff.ready.then(async() => {
                this.$nuxt.$emit("v-show", true);
                // LIFF Get Profile
                this.lineUser = await this.getProfile();
                this.$nuxt.$emit("user", this.lineUser);

                // Lambda Access
                this.$axios.post(`/${this.stage}/line_login`, { idToken: this.lineUser.idToken, locale: this.$store.state.locale })
                .then((response) => {
                    console.log(response);
                })
                .catch((error) => {
                    console.log(error);
                });
            });
        });
    },
    methods: {
        /**
         * プロフィール取得
         * 
         * @returns {Object} プロフィール情報
         */
        async getProfile() {
            return await this.$liff.getLiffProfile();
        },

        /**
         * サイトへ戻る処理
         * 
         */
        back() {
            liff.openWindow({
                url: `https://lineapiusecase.com/${this.$store.state.locale}/api/login.html`,
                external: true
            });
        },
    }
}
</script>

<style scoped>
.message {
    margin: 72px auto;
    color: #00ba00;
    text-shadow: 2px 3px 3px #fff;
}
.name {
    font-size: 1.6em;
    text-align: center;
    color: black;
    text-shadow: 2px 3px 3px #fff;
}
.font-size {
    font-size: 24px;
}
@media screen and (max-width:540px) {
    .font-size {
        font-size: 18px;
    }
}
/* テーブル */
table, th, td {
    table-layout: fixed;
    border-collapse: collapse;
    border: 1px solid #ccc;
    line-height: 1.5;
}
table th {
    width: 150px;
    padding: 10px;
    font-weight: bold;
    vertical-align: top;
    background: #3f3f3f;
    color: #ffffff;
}
table td {
    padding: 10px;
    vertical-align: top;
    word-break: break-all;
}
</style>
