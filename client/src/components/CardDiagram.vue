<!-- https://codepen.io/zFunx/pen/bRqRmJ -->
<template>
  <div class="diagram">
    <template v-if="kind == 'ERROR'">
      <div class="card-group">
        <img :src="getImage('error')" />
        <div class="hint">
          <b-icon-x-circle style="width: 5rem; height: 5rem;">></b-icon-x-circle>
          <h3>Could not find any moves</h3>
        </div>
        <div class="dummy"></div>
      </div>
    </template>

    <template v-else-if="kind == 'DRAW'">
      <div class="card-group">
        <img :src="getImage('back')" />
        <div class="hint">
          <b-icon-arrow-counterclockwise style="width: 5rem; height: 5rem;">></b-icon-arrow-counterclockwise>
          <h3>Draw a card</h3>
        </div>
        <div class="dummy"></div>
      </div>
    </template>

    <template v-else-if="kind == 'TF'">
      <div class="card-group">
        <img :src="getImage(move.from)" />
        <div class="hint">
          <b-icon-arrow-right style="width: 5rem; height: 5rem;">></b-icon-arrow-right>
          <br />
          <h3 v-if="move.to != null">Move from tableau to foundation</h3>
          <h3 v-else>Move from tableau to empty foundation</h3>
        </div>
        <img :src="getImage(move.to)" />
      </div>
    </template>

    <template v-else-if="kind == 'TT'">
      <div class="card-group">
        <img :src="getImage(move.from)" />
        <div class="hint">
          <b-icon-arrow-right style="width: 5rem; height: 5rem;">></b-icon-arrow-right>
          <br />
          <h3>Move from tableau to tableau</h3>
        </div>
        <img :src="getImage(move.to)" />
      </div>
    </template>

    <template v-else-if="kind == 'PF'">
      <div class="card-group">
        <img :src="getImage(move.from)" />
        <div class="hint">
          <b-icon-arrow-right style="width: 5rem; height: 5rem;">></b-icon-arrow-right>
          <br />
          <h3 v-if="move.to != null">Move from pile to foundation</h3>
          <h3 v-else>Move from pile to empty foundation</h3>
        </div>
        <img :src="getImage(move.to)" />
      </div>
    </template>

    <template v-else-if="kind == 'PT'">
      <div class="card-group">
        <img :src="getImage(move.from)" />
        <div class="hint">
          <b-icon-arrow-right style="width: 5rem; height: 5rem;">></b-icon-arrow-right>
          <br />
          <h3 v-if="move.to != null">Move from pile to tableau</h3>
          <h3 v-else>Move from pile to empty tableau</h3>
        </div>
        <img :src="getImage(move.to)" />
      </div>
    </template>
  </div>
</template>

<style scoped>
img {
  max-width: 32%;
  height: auto;
}
.diagram {
  padding: 1.5rem;
}
.card-group {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.hint {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 30%;
}

.hint h3 {
  font-size: 2rem;
  font-size: 2vw;
  text-align: center;
}
</style>

<script>
import ImageLookup from "./ImageLookup.js";
import { BIconArrowRight } from "bootstrap-vue";

export default {
  components: { BIconArrowRight },
  props: {
    kind: {
      type: String,
      required: true
    },
    move: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      styleType: { "0": "", "1": "swirlOut", "2": "swirlIn" }
    };
  },
  methods: {
    getImage(str) {
      return ImageLookup[str];
    }
  }
};
</script>

