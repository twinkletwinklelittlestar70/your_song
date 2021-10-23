<template>
  <img class="app-logo" alt="Your song logo" src="./assets/music-bot-icon.jpg">
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
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  
  position: fixed;
  overflow: hidden;
  width: 100vw;
  height: 100vh;
}
img.app-logo {
    height: 100px;
    width: 100px;
}
</style>
