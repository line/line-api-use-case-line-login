<template>
    <v-app class="wrap" v-show="loggedIn && showed">
        <v-app-bar app fixed class="elevation-1" style="background-color:#fff; opacity:0.9;">
            <v-row>
                <v-col cols="2" class="pa-0" align-self="center">
                    <a v-bind:href="lineUrl">
                        <v-img class="logo" v-bind:src="logo" alt="LINE" />
                    </a>
                </v-col>
                <v-col cols="10" class="pa-0 text-right" align-self="center">
                    <v-menu offset-y transition="slide-y-transition" v-bind:close-on-content-click="true" v-model="menued" ref="menu_list">
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn width="auto" outlined class="pl-2" style="text-transform:none; border-color:transparent; color:#00ba00;" v-on="on" v-bind="attrs">
                                <v-avatar size="30px" style="margin:auto;">
                                    <v-img v-bind:src="lineUser ? lineUser.image : null"></v-img>
                                </v-avatar>
                                <span class="pl-2">{{ lineUser ? lineUser.name : null }}</span>
                            </v-btn>
                        </template>
                        <v-list shaped style="background-color:#fff;">
                            <v-divider></v-divider> 
                            <v-list-item style="font-size:0.9em;" dense>
                                <a class="logout mt-2" v-on:click="logout">
                                    <v-icon small class="mt-0">fas fa-sign-out-alt</v-icon><span class="ml-2">Logout</span>
                                </a>
                            </v-list-item>
                        </v-list>
                    </v-menu>
                </v-col>
            </v-row>
        </v-app-bar>
        <!-- Nuxt Page -->
        <nuxt />
    </v-app>
</template>

<script>
import "~/assets/css/style.css";
import "~/assets/sass/app.scss";

export default {
    middleware: [
       "initialize"
    ],
    data() {
        return {
            loggedIn: false,
            showed: false,
            logo: require("~/assets/img/line.png"),
            lineUser: null,
            menued: false,
        }
    },
    computed: {
        lineUrl() {
            return `https://line.me/${this.$store.state.locale}/`;
        }
    },
    created() {
        this.$nuxt.$on("v-show", this.show);
        this.$nuxt.$on("user", this.user)
    },
    mounted() {
        liff.ready.then(() => {
            this.loggedIn = liff.isLoggedIn();
        });
    },
    methods: {
        /**
         * 画面表示処理
         * 
         * @param {boolean} showed 表示フラグ
         */
        show(showed) {
            this.showed = showed;
        },

        /**
         * LINEユーザー情報設定
         * 
         * @param {Object} lineUser LINEユーザー情報
         */
        user(lineUser) {
            this.lineUser = lineUser;
        },

        /**
         * ログアウト処理
         * 
         */
        logout() {
            liff.logout();
            this.$store.commit("clear");
            this.loggedIn = false;
            if (process.env.COGNITED == true) { 
                this.$amplify.Auth.signOut(); 
                setTimeout(()=>{
                    location.href =  process.env.LOGOUT_URL;
                }, 0);
            } else {
                location.href =  process.env.LOGOUT_URL;
            }
        }
    }
}
</script>

<style scoped>
h2 {
    text-align: center;
    margin: 3px;
}
.liff-title {
    margin: auto 0;
    font-weight: bold;
    color: #fff;
}
.logo {
    width: 3.2em;
    margin: 0.1em;
}
.logout {
    margin: auto 6px;
    color: #000;
    font-size: 1.2em;
    text-align: right;
}
</style>
