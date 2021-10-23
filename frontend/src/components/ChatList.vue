<template>
  <div class="chat-list">
    <div class="chat-scroller">
      <div v-for="item in chatList" :key="item.message">
        <ChatLine :msg="item.message" :isBot="item.isBot"></ChatLine>
      </div>
    </div>
    
    <div class="input-container">
      <el-input v-model="input" placeholder="Please input" v-on:change="sendMessage" />
    </div>
  </div>
</template>

<script>
import { nextTick } from 'vue'
import ChatLine from './ChatLine.vue'
import { postMsg } from '../api/api.js'

export default {
  name: 'ChatList',
  props: {
  },
  data() {
    return {
      input: '',
      chatList: [{
        message: 'Welcome to your song! May I recommend some music for you? Please input your favourite genre.\
          \n R&B\n Underground Rap\n Dark Trap\n Hip Hop\n trance\n trap\n',
        isBot: true
      }, {
        message: 'R&B',
        isBot: false
      }]
    };
  },
  components: {
    ChatLine
  },
  methods: {
    sendMessage(msg) {
      this.chatList.push({
        message: msg,
        isBot: false
      })
      this.scrollToBottom()
      this.input = ''
      
      // 发送给后端
      postMsg(msg).then((data) => {
        const response = data.response
        this.chatList.push({
          message: 'Bot: ' + response,
          isBot: true
        })
        this.scrollToBottom()
      })
      
    },
    scrollToBottom() {
      nextTick(() => {
        const scroller = document.getElementsByClassName('chat-scroller')[0]
        scroller.scrollTop = scroller.scrollHeight;
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
a {
  color: #42b983;
}
.input-container {
  position: fixed;
  bottom: 80px;
  width: calc(100vw - 60px);
  margin-left: 20px;
}
.chat-scroller {
  overflow: scroll;
  max-height: calc(100vh - 400px);
}
</style>
