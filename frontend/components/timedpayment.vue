<template>
  <div>
    <div class="address">
      <div class="row">
        <div class="col-lg-auto">
          <cinput label="Send this exact amount of:" selector="amount" :value="invoice_data.coin_amount"></cinput>
        </div>
        <div class="col ">
          <cinput label="to Bitcoin Address:" selector="address" :value="invoice_data.address"></cinput>
        </div>
      </div>
    </div>
    <hr>
    <div class="content">
      <div class="row justify-content-md-around align-items-center">
        <merchant :invoice_data="invoice_data" class="col-xl-9 col-lg-8 col-md-8"></merchant>
        <div class="col col-xl-3 col-lg-4 col-md-4 text-right">
          <div class="qrcode position-relative" style="width: 150px">
              <span class="position-absolute" style="top:44%; left:44%;">
              <img :src="btc_icon2" alt="btc" >
            </span>
          <img  :src="invoice_data.qrcode_url" alt="qrcode">
          </div>
        </div>
      </div>
      <hr>
      <countdown :expired="get_is_expired" 
      :count_down="invoice_data.timeout" ref="countdown"></countdown>
    </div>
  </div>
</template>

<script>
import merchant from "./merchant.vue";
import cinput from "./input.vue";
import countdown  from "./countdown.vue";

export default {
  props: {
    invoice_data: Object
  },
  computed:{
    get_is_expired(){
      return this.invoice_data != undefined && this.invoice_data.expired
    }
  },
  data() {
    return {
      btc_icon: "https://cryptoicons.org/api/color/btc/18/ffc107",
      btc_icon2: "https://cryptoicons.org/api/color/btc/32/ffc107"
    }
  },
  components: {
    merchant,
    cinput,
    countdown
  },
  mounted: function(){
    console.log(this.invoice_data);
  }
}
</script>

<style lang="scss" >
.adddress{
  border: 1px solid lightgrey;
}
.background-color {
  background-color: #376097;
}
.back-color {
  color: #376097;
}
.back-color-1 {
  color: #f4661e;
}
@media (max-width: 767px)
{
  .qrcode{
    display: none;
  }
}
</style>
