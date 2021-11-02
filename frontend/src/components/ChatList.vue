<template>
  <div class="chat-list">
    <div class="chat-scroller">
      <div v-for="item in chatList" :key="item.message">
        <ChatLine :msg="item.message" :isBot="item.isBot" :rawHtml="item.rawHtml"></ChatLine>
      </div>
    </div>
    <div class="input-container">
      <el-input v-model="input" placeholder="Let's start the music journery~ (>^ω^<)" v-on:change="sendMessage" />
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
        message: 'Hi! I am Yoyo, your music assitant. What can I do for you?',
        rawHtml: "",
        isBot: true
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
        rawHtml: '',
        isBot: false
      })
      this.scrollToBottom()
      this.input = ''
      
      // 发送给后端
      postMsg(msg).then((data) => {
        const response = data.response
        const recommendList = data.recommend_list || []
        let rawHtml = ''
        if (recommendList.length > 0) {
          rawHtml = '<br/><ol>'
          for (let i=0, len=recommendList.length; i<len; i++) {
            let songName = recommendList[i]['name']
            let url = recommendList[i]['url']
            rawHtml += '<li><a style="color: #39c5d9;text-decoration: none;" href=' + url + '>' + songName + '</a></li>'
          }
          rawHtml += '</ol><br/>'
        }
        
        this.chatList.push({
          message: response,
          rawHtml,
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
  bottom: 30px;
  width: calc(100vw - 60px);
  margin-left: 20px;
}
.chat-scroller {
  overflow: scroll;
  max-height: calc(100vh - 460px);
}
</style>
