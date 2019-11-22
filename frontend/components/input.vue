<template>
  <div class="c_input">
    <label for="basic-url">{{ label }}</label>
    <div class="input-group">
      <div class="input-group-prepend">
        <span class="input-group-text" id="basic-addon3">
          <a-tooltip placement="topLeft" :title="copy_text">
            <a-button @click="copy">
              <span style="font-size: 1.5em; color: #376097;">
                <i class="fa fa-copy" />
              </span>
            </a-button>
          </a-tooltip>
        </span>
      </div>
      <input
        type="text"
        :value="value"
        disabled
        class="form-control"
        id="basic-url"
        aria-describedby="basic-addon3"
      />
    </div>
    <input type="hidden" :id="selector" :value="value" />
  </div>
</template>

<script>
var intval = undefined;
export default {
  props: {
    label: String,
    value: String | Number,
    selector: String
  },
  data() {
    return {
      copy_text: "Copy"
    };
  },
  methods: {
    copy() {
      let CodeToCopy = document.querySelector(`#${this.selector}`);
      CodeToCopy.setAttribute("type", "text");
      CodeToCopy.select();

      try {
        var successful = document.execCommand("copy");
        this.copy_text = "Copied";
      } catch (err) {
        this.copy_text = "Unable to copied";
      }
      CodeToCopy.setAttribute("type", "hidden");
      window.getSelection().removeAllRanges();

      intval = setInterval(() => {
        this.copy_text = "Copy";
        clearInterval(intval);
      }, 4000);
    }
  }
};
</script>

<style lang="scss">
.c_input {
  font-size: 12px;
  label {
    margin-bottom: 1px;
  }
  .input-group-text {
    padding: 1px;
    border-radius: 0px;
    background-color: whitesmoke;
    button {
      background: transparent;
      border: 0px;
      padding: 2px 5px;
    }
  }
  .form-control {
    font-size: 15px;
    font-weight: 700;
  }
}
</style>
