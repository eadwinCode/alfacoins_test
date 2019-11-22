<template>
  <div class="container pt-5">
    <div class="row justify-content-md-center">
      <div class="col-lg-9 col-sm-12">
        <a-card size="small" class="card">
          <div slot="title" class="header">
            <h4>
              Invoice:
              <span class="text-muted" style="font-size: 15px"
                ># {{invoice_data.code}}</span
              >
            </h4>
          </div>
          <div slot="extra">
            <h5
              class="font-weight-bold border border-light bg-light p-1 rounded"
            >
              <img :src="btc_icon" alt="btc" />
              <span class="text-uppercase pl-2">btc</span>
            </h5>
          </div>
          <spiner v-if="isloading"></spiner>
          <div v-else>
            <component :is="get_template.type" v-bind="get_template.propsData"></component>
          </div>
        </a-card>
      </div>
    </div>
  </div>
</template>

<script>
import timedpayment from "./timedpayment.vue";
import expiredpayment from "./expiredpayment.vue";
import successpayment from "./successfulpayment.vue";
import completedpayment from "./completed.vue";
import spiner from "./spiner.vue";

export default {
  data() {
    return {
      btc_icon: "https://cryptoicons.org/api/color/btc/18/ffc107",
      isloading: true,
      url: 'https://api.coindesk.com/v1/bpi/currentprice.json',
      status: "expired",
      invoice_data: {
        expired: false,
        code: 'ADEJJIDSKLSASSAEDSVDSVAXS',
        address: "33JfbrEFPwf7rABv6LFwJhTPpkoQCHTDSD",
        btc_rate: 8754,
        coin_amount: 0.00356700,
        timeout: 900,
        qrcode_url: 'https://chart.googleapis.com/chart?cht=qr&chl=bitcoin:33JfbrEFPwf7rABv6LFwJhTPpkoQCHTDSD?amount=0.00356700&choe=UTF-8&chs=180x180&chld=L|1',
        merchant: {
          company: 'theConcept',
          description: 'some descrption',
          payer: 'Some Name',
          Email: 'Some Email'
        }
      }
    };
  },
  computed:{
    get_template(){
      switch(this.status){
        case 'completed':
          return {
            type: 'completedpayment', propsData: {}
          }
        case 'paid':
          return {
            type: 'successpayment', propsData: {}
          }
        case 'new':
          return {
            type: 'timedpayment',
            propsData: {
              invoice_data: this.invoice_data,
               btc_icon: "https://cryptoicons.org/api/color/btc/18/ffc107",
              btc_icon2: "https://cryptoicons.org/api/color/btc/32/ffc107",
            }
          }
        case 'expired':
          return {
            type: 'expiredpayment', propsData: {invoice_data: this.invoice_data}
          }
      }
    }
  },
  components: {
    timedpayment,
    expiredpayment,
    successpayment,
    completedpayment,
    spiner
  },
  methods: {
    set_data_to_props(data){
      if(status !== data.status){
        status = data.status
      }
      this.invoice_data = data
    }
  },
  mounted: function(){
    var interval = null;
    interval = setInterval(()=> {
      this.isloading = false;
      this.axios.get(window.data_url).then(response => (console.log(response)));
      clearInterval(interval);
    },5000)
  }
};
</script>

<style lang="scss">
.card {
  border: 2px solid lightgray;
  border-radius: 4px;
  h5 {
    margin-bottom: 0px;
    font-size: 1rem;
  }
}
</style>
