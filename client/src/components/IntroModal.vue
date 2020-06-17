<template>
  <b-modal ref="modal" id="modal" size="xl" title="Introduction" hide-backdrop>
    Welcome to our Solitaire hinting app!
    In order to use this program, we have a couple of requirements:
    <ul>
      <li>English playing cards. E.g. K, Q, J, A instead of K, D, Kn, Es.</li>
      <li>A dark background for the picture.</li>
      <li>Please allow time after taking a picture for the results to come in!</li>
    </ul>And please make use of the guide lines to seperate the pile, foundations and tableaus!
    <template
      v-slot:modal-footer="{ ok, hide }"
    >
      <b-button size="lg" variant="outline-secondary" @click="hide()">Skip tour</b-button>
      <b-button size="lg" variant="primary" @click="start_tour(ok)">Start tour</b-button>
    </template>
  </b-modal>
</template>

<style scoped>
h3 {
  margin: 40px 0 0;
}
</style>


<script>
export default {
  name: "IntroModal",
  data: {
    callback: null
  },
  methods: {
    show(callback) {
      this.callback = callback;
      this.$refs.modal.show();
    },
    start_tour(ok) {
      ok();
      this.callback();
    }
  }
};
</script>

