import Vue from "vue";
import test  from "./components/payment.vue";

import antd from 'ant-design-vue';
import axios from 'axios'
import VueAxios from 'vue-axios'
 
Vue.use(VueAxios, axios);

Vue.use(antd.Carousel);
Vue.use(antd.Button);
Vue.use(antd.Progress);
Vue.use(antd.Card);
Vue.use(antd.Tooltip);
Vue.use(antd.Icon);
Vue.use(antd.Spin);


new Vue(test).$mount("#app");