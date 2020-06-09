<template>
  <div class="backdrop">
    <div class="swirl" v-bind:class="styleType[type]">
      <div></div>
      <div></div>
      <div></div>
    </div>
  </div>
</template>

<style>
.backdrop {
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background-color: #22222271;
  z-index: 2;
}
.swirl {
  width: 200px;
  height: 200px;
  position: fixed;
  top: calc(50% - 100px);
  left: calc(50% - 100px);
  z-index: 3;
  filter: blur(2px) brightness(0deg);
  margin: 20px;
  animation: swirlSpin 0.5s linear infinite;
  display: inline-block;
}

.swirl div {
  border: 9px solid crimson;
  border-width: 9px 0 0 0;
  border-radius: 50%;
  position: absolute;
  opacity: 0;
}

.swirl div:first-child {
  width: 200px;
  height: 200px;
  animation: swirlOpacityFirst 10s ease infinite;
}

.swirl div:nth-child(2) {
  width: 150px;
  height: 150px;
  top: 25px;
  left: 25px;
  transform: rotate(50deg);
  animation: swirlOpacitySecond 10s ease infinite;
}

.swirl div:nth-child(3) {
  width: 100px;
  height: 100px;
  top: 50px;
  left: 50px;
  transform: rotate(100deg);
  animation: swirlOpacityThird 10s ease infinite;
}

@keyframes swirlOpacityFirst {
  8%,
  24%,
  72%,
  88% {
    opacity: 1;
  }
  32%,
  64% {
    opacity: 0;
  }
}

@keyframes swirlOpacitySecond {
  8%,
  40%,
  56%,
  88% {
    opacity: 0;
  }
  16%,
  32%,
  64%,
  80% {
    opacity: 1;
  }
}

@keyframes swirlOpacityThird {
  24%,
  40%,
  56%,
  72% {
    opacity: 1;
  }
  16%,
  48%,
  80% {
    opacity: 0;
  }
}

.swirl.swirlIn div:first-child {
  animation: swirlInOpacityFirst 5s ease infinite;
}

.swirl.swirlIn div:nth-child(2) {
  animation: swirlInOpacitySecond 5s ease infinite;
}

.swirl.swirlIn div:nth-child(3) {
  animation: swirlInOpacityThird 5s ease infinite;
}

.swirl.swirlOut div:first-child {
  animation: swirlOutOpacityFirst 5s ease infinite;
}

.swirl.swirlOut div:nth-child(2) {
  animation: swirlOutOpacitySecond 5s ease infinite;
}

.swirl.swirlOut div:nth-child(3) {
  animation: swirlOutOpacityThird 5s ease infinite;
}

@keyframes swirlSpin {
  to {
    transform: rotate(360deg);
    filter: blur(2px) brightness(360deg);
  }
}

@keyframes swirlInOpacityFirst {
  10%,
  50% {
    opacity: 1;
  }
  70% {
    opacity: 0;
  }
}

@keyframes swirlInOpacitySecond {
  10%,
  90% {
    opacity: 0;
  }
  30%,
  70% {
    opacity: 1;
  }
}

@keyframes swirlInOpacityThird {
  30% {
    opacity: 0;
  }
  50%,
  90% {
    opacity: 1;
  }
}

@keyframes swirlOutOpacityThird {
  10%,
  50% {
    opacity: 1;
  }
  70% {
    opacity: 0;
  }
}

@keyframes swirlOutOpacitySecond {
  10%,
  90% {
    opacity: 0;
  }
  30%,
  70% {
    opacity: 1;
  }
}

@keyframes swirlOutOpacityFirst {
  30% {
    opacity: 0;
  }
  50%,
  90% {
    opacity: 1;
  }
}
</style>

<script>
export default {
  props: {
    type: String
  },
  data() {
    return {
      styleType: { "0": "", "1": "swirlOut", "2": "swirlIn" }
    };
  }
};
</script>
