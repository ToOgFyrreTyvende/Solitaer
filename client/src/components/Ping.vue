<template>
  <div class="container">
    <button type="button" @click="getMessage()" class="btn btn-primary">{{ msg }}</button>
    <select v-model="camera">
      <option>-- Select Device --</option>
      <option
        v-for="device in devices"
        :key="device.deviceId"
        :value="device.deviceId"
      >{{ device.label }}</option>
    </select>
    <vue-web-cam
      ref="webcam"
      :device-id="deviceId"
      width="100%"
      @started="onStarted"
      @stopped="onStopped"
      @error="onError"
      @cameras="onCameras"
      @camera-change="onCameraChange"
    />
  </div>
</template>

<script>
import axios from "axios";
import { WebCam } from "vue-web-cam";

export default {
  name: "Ping",
  components: {
    "vue-web-cam": WebCam
  },
  data() {
    return {
      msg: "tewtwehts",
      camera: null,
      deviceId: null,
      devices: []
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
      this.devices = cameras;
      console.log("On Cameras Event", cameras);
    },
    onCapture() {
      this.img = this.$refs.webcam.capture();
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
