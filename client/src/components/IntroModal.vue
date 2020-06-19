<template>
  <b-modal ref="intro_modal" id="intro_modal" size="xl" title="Introduction" hide-backdrop>
    Welcome to our Solitaire hinting app!
    In order to use this program, we have a couple of requirements:
    <ul>
      <li>English playing cards. E.g. K, Q, J, A instead of K, D, Kn, Es.</li>
      <li>A dark background for the picture.</li>
      <li>Please allow time after taking a picture for the results to come in!</li>
    </ul>And please make use of the guide lines to seperate the pile, foundations and tableaus!
    <p>
      Each new hint requires you to take a new picture of the updated playing board.
      The hints come back to the website in the following form:
    </p>
    <card-diagram id="example_diagram" :kind="card_diagram_move_kind" :move="card_diagram_move"></card-diagram>
    <p>You can take a tour of the UI by clicking "Start tour", otherwise if you're ready to play, press skip!</p>

    <template v-slot:modal-footer="{ ok, hide }">
      <b-button size="lg" variant="outline-secondary" @click="hide()">Skip</b-button>
      <b-button size="lg" variant="primary" @click="start_tour(ok)">Start tour</b-button>
    </template>
  </b-modal>
</template>

<style scoped>
</style>


<script>
import CardDiagram from "./CardDiagram.vue";

export default {
  name: "IntroModal",
  components: {
    "card-diagram": CardDiagram
  },
  data() {
    return {
      callback: null,
      card_diagram_move_kind: "TT",
      card_diagram_move: { from: "Qs", to: "Kh" }
    };
  },
  methods: {
    show(callback) {
      this.callback = callback;
      this.$refs.intro_modal.show();
    },
    start_tour(ok) {
      ok();
      this.callback();
    },
    hint_img() {
      return Images.hint;
    }
  }
};
</script>

