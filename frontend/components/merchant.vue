<template>
  <div class="merchant-data">
    <div v-for="(value, name, index) in invoice_data.merchant" class="data-row" :key="index">
      <div class="data-label text-capitalize">{{ name }}:</div>
      <div class="data">{{ value }}</div>
    </div>
  </div>
</template>

<script>
export default {
  props:{
        invoice_data: Object
    },
  methods: {}
};
</script>

<style lang="scss">
.merchant-data {
  text-align: right;
  font-size: 20px;
  line-height: 30px;
  color: #1b3049;

  .data-row {
    overflow: hidden;
  }
  .data-label {
    text-align: left;
    float: left;
    min-width: 140px;
    margin-right: 5px;
    font-weight: 600;
    letter-spacing: -1px;
  }
  .data {
    overflow: hidden;
  }

  @media (max-width: 576px) {
    font-size: 12px;
    line-height: 1.5;
    .data-label {
      text-align: left;
      min-width: 0;
    }
  }
}
</style>
