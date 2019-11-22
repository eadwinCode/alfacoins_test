<template>
  <div>
    <div class="content">
      <div class="row justify-content-center align-items-center text-center">
        <div class="col-12 "><span class="d-block " style="font-size: 8em; color: #f4661e"><i class="fa fa-exclamation-triangle"></i></span></div>
        <h4 class="col-12 text-muted font-weight-bolder">Sorry, this invoice has expired</h4>
      </div>
      <hr>
      <countdown :expired="true" ref="countdown"></countdown>
    </div>
  </div>
</template>

<script>
import countdown  from "./countdown.vue";

export default {
    props:{
        invoice_data: Object
    },
    components: {
        countdown
    }
}
</script>

<style scoped>

</style>