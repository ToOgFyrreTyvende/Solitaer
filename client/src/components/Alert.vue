<template>
  <div>
    <b-alert variant="success" show>{{'memes ' +  message }}</b-alert>
    <br>
  </div>
</template>

<script>
export default {
  props: {
    message: String,
  },
};
</script>
