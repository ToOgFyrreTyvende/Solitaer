<template>
  <div class="container">
    <div
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
    </div>

    <div id="overlay" v-show="show_overlay">
      <button type="button" class="close" @click="hideScreenElements()">&times;</button>

      <h4>Response:</h4>
      <img class="fit-img" v-bind:src="return_img" v-show="return_img != null" />
      <br />
      {{cards}}
    </div>

    <vue-web-cam
      id="cam"
      ref="webcam"
      :device-id="deviceId"
      width="100%"
      height="100%"
      v-bind:resolution="{height: 2160, width: 4096}"
      @click.native="hideScreenElements()"
      @started="onStarted"
      @stopped="onStopped"
      @error="onError"
      @cameras="onCameras"
      @camera-change="onCameraChange"
    />
    <button id="take-picture" v-bind:class="{change: show_side_menu}" @click="analyzePicture()"></button>
  </div>
</template>

<style>
.container {
  padding: 0;
  margin: 0;
  width: 100vw;
  height: 100vh;
}
.menuToggleContainer {
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 2;
  cursor: pointer;
  display: inline-block;
  transition: 0.3s;
}
.bar1,
.bar2,
.bar3 {
  width: 35px;
  height: 5px;
  background-color: #333;
  margin: 6px 0;
  transition: 0.4s;
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
  z-index: 1;
  top: 0;
  left: 0;
  background-color: #111;
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

#cam {
  object-fit: cover;
  position: fixed;
  width: 100%;
  height: 100%;
}

#overlay {
  z-index: 3;
  position: fixed;
  top: 0;
  left: 0;
  width: calc(100% - 2rem);
  height: calc(100% - 2rem);
  margin: 1rem;
  background-color: #f8f8ff;
  border-radius: 15px;
  padding: 1rem;
}
.close {
  position: fixed;
  top: 1.5rem;
  right: 1.5rem;
  font-size: 2rem;
}
.fit-img {
  max-width: 95%;
  margin: 0 auto;
}

#take-picture {
  position: fixed;
  bottom: 35px;
  left: 50%;
  transform: translateX(-50%);

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

@media screen and (orientation: landscape) {
  #overlay {
    bottom: 15px;
  }
}
</style>


<script>
import axios from "axios";
import { WebCam } from "vue-web-cam";

export default {
  name: "Cam",
  components: {
    "vue-web-cam": WebCam
  },
  data() {
    return {
      msg: "tewtwehts",
      camera: null,
      deviceId: null,
      devices: [],
      return_img: null,
      show_side_menu: false,
      show_overlay: false,
      cards: ""
    };
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
    hideScreenElements() {
      if (this.show_side_menu) this.show_side_menu = false;
      if (this.show_overlay) this.show_overlay = false;
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
    analyzePicture() {
      this.sendPicture();
      let _this = this;
      axios
        .post("http://127.0.0.1:5000/boardAnalyse", { data: this.img })
        .then(({ data }) => {
          _this.return_img = "data:image/png;base64," + data.img_data;
          _this.show_overlay = true;
          _this.cards = data.cards;
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
    }
  }
};
</script>
