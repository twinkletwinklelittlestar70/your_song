<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p v-for="item in chatList" :key="item.message">
      {{ item.message }}
    </p>
    <el-input v-model="input" placeholder="Please input" v-on:change="sendMessage" />
  </div>
</template>

<script>
import { postMsg } from '../api/api.js'

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data() {
    return {
      input: '',
      chatList: []
    };
  },
  components: {

  },
  methods: {
    sendMessage(msg) {
      this.chatList.push({
        message: msg
      })
      this.input = ''
      
      // 发送给后端
      postMsg(msg).then((data) => {
        const response = data.response
        this.chatList.push({
          message: 'Bot: ' + response
        })
      })
      
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
