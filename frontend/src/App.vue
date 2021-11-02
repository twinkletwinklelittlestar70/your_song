<template>
  <img class="app-logo" alt="Your song logo" src="./assets/banner.jpg">
  <h1>Welcome to Your Song</h1>
  <ChatList />
</template>

<script>
import ChatList from './components/ChatList.vue'

export default {
  name: 'App',
  components: {
    ChatList
  }
}
</script>

<style>
body {
  background: #f6f6f6;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 25px;
  
  position: fixed;
  overflow: hidden;
  width: 100vw;
  height: 100vh;
}
::-webkit-scrollbar {
    width: 0px !important;
    height: 0px !important;
}
img.app-logo {
    width: 30%;
}
ul,ol {
  margin: 0;
}
</style>
