<template>
  <div class="container" ref="container">
    <loader v-show="loading" type="1"></loader>

    <div
      class="fullscreenContainer"
      ref="fullscreenToggler"
      @click="fullscreenToggle()"
      v-show="!in_pwa"
    >
      <b-icon
        :icon="fullscreen ? 'fullscreen-exit' : 'fullscreen'"
        style="width: 27px; height: 27px;"
        variant="white"
      ></b-icon>
    </div>

    <div
      data-v-step="0"
      class="menuToggleContainer"
      v-bind:class="{change: show_side_menu}"
      ref="menuToggler"
      @click="menuToggle()"
    >
      <div class="bar1"></div>
      <div class="bar2"></div>
      <div class="bar3"></div>
    </div>

    <div id="side-nav" v-bind:class="{opened: show_side_menu}" class="sidenav">
      <span>Choose camera here:</span>
      <select v-model="camera">
        <option>-- Select Device --</option>
        <option
          v-for="device in devices"
          :key="device.deviceId"
          :value="device.deviceId"
        >{{ device.label }}</option>
      </select>
      <b-button @click="guideOpen()">Show guide</b-button>
    </div>

    <b-modal static="true" ref="modal" id="modal" size="xl" title="Hint" hide-footer hide-backdrop>
      <diagram v-bind:kind="move_kind" v-bind:move="move"></diagram>
      <img class="img-fluid" v-bind:src="return_img" v-show="return_img != null" />
      <br />
      {{cards}}
    </b-modal>

    <vue-web-cam
      id="cam"
      ref="webcam"
      :device-id="deviceId"
      width="100%"
      height="100%"
      v-bind:resolution="{height: 720, width: 1280 }"
      @click.native="hideScreenElements()"
      @started="onStarted"
      @stopped="onStopped"
      @error="onError"
      @cameras="onCameras"
      @camera-change="onCameraChange"
    />
    <div class="guide-line" data-v-step="1"></div>

    <div ref="flashing_bg" class="flashing-bg"></div>

    <button
      data-v-step="2"
      ref="take_picture"
      id="take-picture"
      v-bind:class="{change: show_side_menu}"
      @click="analyzePicture()"
    ></button>

    <intro-modal ref="intro_modal"></intro-modal>
    <v-tour name="intro_tour" :steps="steps"></v-tour>
  </div>
</template>

<style>
@import "../assets/styles/animations.css";

.container {
  padding: 0;
  margin: 0;
  width: 100vw;
  height: 100vh;
}

.flashing-bg {
  pointer-events: none;
  z-index: 1;
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
}

.fullscreenContainer {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 3;
  cursor: pointer;
  display: inline-block;
  transition: 0.3s;
  background-color: rgba(33, 33, 33, 0.9);
  padding: 0.8rem;
}

.menuToggleContainer {
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 3;
  cursor: pointer;
  display: inline-block;
  transition: 0.3s;
  background-color: rgba(33, 33, 33, 0.9);
  padding: 0.8rem;
}
.bar1,
.bar2,
.bar3 {
  width: 27px;
  height: 5px;
  background-color: #f8f8f8;
  transition: 0.4s;
}
.bar1 {
  margin: 0 0 6px 0;
}
.bar2 {
  margin: 6px 0;
}
.bar3 {
  margin: 6px 0 0 0;
}

.change .menuToggleContainer {
  background: none;
}
.change .bar1 {
  -webkit-transform: rotate(-45deg) translate(-9px, 6px);
  transform: rotate(-45deg) translate(-9px, 6px);
  background-color: #f8f8ff;
}
.change .bar2 {
  opacity: 0;
}
.change .bar3 {
  -webkit-transform: rotate(45deg) translate(-8px, -8px);
  transform: rotate(45deg) translate(-8px, -8px);
  background-color: #f8f8ff;
  border-top: 1px solid #313133;
}

.sidenav {
  height: 100%;
  width: 0;
  position: fixed;
  z-index: 2;
  top: 0;
  left: 0;
  background-color: rgba(33, 33, 33, 0.9);
  overflow-x: hidden;
  padding-top: 80px;
  transition: 0.3s;
  color: #f8f8ff;
}
.sidenav * {
  z-index: inherit;
}
.sidenav a {
  padding: 8px 8px 8px 32px;
  text-decoration: none;
  font-size: 25px;
  color: #818181;
  display: block;
  transition: 0.2s;
}
.sidenav a:hover {
  color: #f1f1f1;
}
.opened {
  width: 250px;
  padding-left: 1rem;
  padding-right: 1rem;
}

.sidenav > * {
  margin-bottom: 1rem;
}

.guide-line {
  z-index: 1;
  position: fixed;
  top: 35%;
  left: 0;
  height: 1px;
  background-color: rgba(255, 255, 255, 0.6);
  width: 100%;
}

.guide-line::after {
  content: "";
  z-index: 1;
  position: fixed;
  top: 0;
  left: 35%;
  height: 35%;
  width: 1px;
  background-color: rgba(255, 255, 255, 0.6);
}

#cam {
  object-fit: cover;
  position: fixed;
  width: 100%;
  height: 100%;
}

#take-picture {
  z-index: 2;
  position: fixed;
  bottom: 35px;
  right: 50%;
  transform: translateX(50%);

  display: block;
  border-radius: 50%;
  border: 0;
  background-color: crimson;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 5px solid rgba(255, 255, 255, 0.95);
  outline: 0;
}
#take-picture:active {
  box-shadow: inset 0 0 8px 8px rgba(102, 102, 102, 0.5);
}
.flex-container {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
}

@media only screen and (orientation: landscape) {
  #take-picture {
    z-index: 2;
    position: fixed;
    bottom: 50%;
    right: 35px;
    transform: translateY(50%);
  }
}
</style>

<script>
import axios from "axios";
import { WebCam } from "vue-web-cam";
import Loader from "./Loader.vue";
import CardDiagram from "./CardDiagram.vue";
import Images from "./Images";
import IntroModal from "./IntroModal.vue";

export default {
  name: "Cam",
  components: {
    "vue-web-cam": WebCam,
    loader: Loader,
    diagram: CardDiagram,
    "intro-modal": IntroModal
  },
  data() {
    return {
      camera: null,
      deviceId: null,
      devices: [],
      loading: false,
      return_img: null,
      show_side_menu: false,
      cards: "",
      move_kind: "",
      move: {
        from: null,
        to: null
      },
      fullscreen: false,
      in_pwa: false,
      steps: [
        {
          target: '[data-v-step="0"]',
          header: {
            title: "Welcome!"
          },
          content: `Set camera specific settings and browse options here.`
        },
        {
          target: '[data-v-step="1"]',
          header: {
            title: "Guide line"
          },
          content: `Make sure your stock, pile and foundations are above this guide line.
          <br>
          <img class="img-fluid" src="${Images.intro_example}" />`
        },
        {
          target: '[data-v-step="2"]',
          header: {
            title: "Analyze the board"
          },
          content: `Press here when you're ready to analyze your board!`
        }
      ]
    };
  },
  mounted() {
    const pwaModeEnabled =
      window.navigator.standAlone || // Safari
      window.fullScreen || // FireFox
      (!window.screenTop && !window.screenY); // Chrome

    this.in_pwa = pwaModeEnabled;

    if (localStorage.intro != "true") {
      localStorage.intro = true;
      this.guideOpen();
    }
  },
  computed: {
    device() {
      return this.devices.find(n => n.deviceId === this.deviceId);
    }
  },
  watch: {
    camera(id) {
      this.deviceId = id;
    },
    devices() {
      // Once we have a list select the first one
      // const [first, ...rest] = this.devices;
      const first = this.devices[0];
      if (first) {
        this.camera = first.deviceId;
        this.deviceId = first.deviceId;
      }
    }
  },
  methods: {
    menuToggle() {
      this.show_side_menu = !this.show_side_menu;
    },
    guideOpen() {
      if (this.show_side_menu) this.show_side_menu = false;
      let _this = this;
      this.$refs.intro_modal.show(() => {
        _this.$tours["intro_tour"].start();
      });
    },
    hideScreenElements() {
      if (this.show_side_menu) this.show_side_menu = false;
    },
    getMessage() {
      const path = "http://localhost:5000/ping";
      axios
        .get(path)
        .then(res => {
          this.msg = res.data;
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onCameras(cameras) {
      let renamed_cams = cameras.map((x, i) => {
        if (x.label == "") {
          return {
            deviceId: x.deviceId,
            label: i == 0 ? "Back facing" : "Front facing"
          };
        } else {
          return x;
        }
      });
      this.devices = renamed_cams;
      console.log("On Cameras Event", cameras);
    },
    sendPicture() {
      this.img = this.$refs.webcam.capture();
    },
    flashAndFade() {
      this.$refs.flashing_bg.classList.remove("flash-bg");
      this.$refs.flashing_bg.classList.add("flash-bg");

      this.$refs.take_picture.classList.remove("fade-out");
      this.$refs.take_picture.classList.add("fade-out");

      this.loading = true;
    },
    stopLoading() {
      this.$refs.flashing_bg.classList.remove("flash-bg");
      this.$refs.take_picture.classList.remove("fade-out");

      this.loading = false;
    },
    analyzePicture() {
      this.hideScreenElements();
      this.flashAndFade();

      this.sendPicture();
      let _this = this;
      axios
        .post("/api/getMove", { data: this.img })
        .then(({ data }) => {
          //_this.return_img = "data:image/png;base64," + data.img_data;
          _this.move_kind = data.kind;
          _this.move = data.move;
          _this.$refs.modal.show();
          _this.stopLoading();
        })
        .catch(error => {
          console.log(error);
        });
    },
    onStarted(stream) {
      console.log("On Started Event", stream);
    },
    onStopped(stream) {
      console.log("On Stopped Event", stream);
    },
    onStop() {
      this.$refs.webcam.stop();
    },
    onStart() {
      this.$refs.webcam.start();
    },
    onError(error) {
      console.log("On Error Event", error);
    },
    onCameraChange(deviceId) {
      this.deviceId = deviceId;
      this.camera = deviceId;
      console.log("On Camera Change Event", deviceId);
    },
    fullscreenToggle() {
      if (this.fullscreen) {
        this.stopFullscreen();
      } else {
        this.startFullscreen();
      }
      this.fullscreen = !this.fullscreen;
    },
    startFullscreen() {
      if (this.$refs.container.requestFullscreen) {
        this.$refs.container.requestFullscreen();
      } else if (this.$refs.container.mozRequestFullScreen) {
        /* Firefox */
        this.$refs.container.mozRequestFullScreen();
      } else if (this.$refs.container.webkitRequestFullscreen) {
        /* Chrome, Safari and Opera */
        this.$refs.container.webkitRequestFullscreen();
      } else if (this.$refs.container.msRequestFullscreen) {
        /* IE/Edge */
        this.$refs.container.msRequestFullscreen();
      }
    },
    stopFullscreen() {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.mozCancelFullScreen) {
        /* Firefox */
        document.mozCancelFullScreen();
      } else if (document.webkitExitFullscreen) {
        /* Chrome, Safari and Opera */
        document.webkitExitFullscreen();
      } else if (document.msExitFullscreen) {
        /* IE/Edge */
        document.msExitFullscreen();
      }
    }
  }
};
</script>
