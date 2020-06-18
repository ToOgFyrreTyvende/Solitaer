<!-- https://codepen.io/zFunx/pen/bRqRmJ -->
<template>
  <div class="diagram">
    <template v-if="kind == 'stock'">
      <div class="card-group">
        <img :src="getImage('back')" />
        <div class="hint">
          <b-icon-arrow-counterclockwise style="width: 5rem; height: 5rem;">></b-icon-arrow-counterclockwise>
          <h3>Flip a stock card.</h3>
        </div>
        <div class="dummy"></div>
      </div>
    </template>

    <template v-if="kind == 'foundation'">
      <div class="card-group">
        <img :src="getImage(move.from)" />
        <div class="hint">
          <b-icon-arrow-right style="width: 5rem; height: 5rem;">></b-icon-arrow-right>
          <br />
          <h3>Move {{ move.from }} to foundation {{ move.to }}</h3>
        </div>
        <img :src="getImage(move.to)" />
      </div>
    </template>

    <template v-if="kind == 'tableau'">
      <div class="card-group">
        <img :src="getImage(move.from)" />
        <div class="hint">
          <b-icon-arrow-right style="width: 5rem; height: 5rem;">></b-icon-arrow-right>
          <br />
          <h3>Move card {{ move.from }} to {{ move.to }}</h3>
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
