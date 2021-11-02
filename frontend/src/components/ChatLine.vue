<template>
    <div class="bot-chat-line" v-if="isBot">
        <div class="avator-container">
            <img class="avator-icon" src="../assets/bot.png">
        </div>
        <div class="message-container">
            <span>{{ msg }}</span>
            <div v-if="rawHtml" v-html="rawHtml"></div>
        </div>
    </div>
    <div class="me-chat-line" v-else>
      <div class="avator-container">
            <img class="avator-icon" src="../assets/profile.jpeg">
        </div>
        <div class="message-container">
            <span>{{ msg }}</span>
        </div>
    </div>
</template>

<script>

export default {
  name: 'ChatLine',
  props: {
    msg: String,
    isBot: Boolean,
    rawHtml: String
  },
  data() {
    return {
    };
  },
  components: {

  },
  methods: {
    
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.bot-chat-line, .me-chat-line {
    padding: 10px 30px;
    display: flex;
}
.bot-chat-line {
    flex-direction: row;
}
.me-chat-line {
    flex-direction: row-reverse;
}
.avator-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
}
.message-container {
    text-align: left;
    /* display: flex; */
    align-items: center;
    white-space: pre-line;
    background: #7ab1d724;
    border-radius: 15px;
    padding: 15px 15px;
    
}
.bot-chat-line .message-container {
    margin-left: 10px;
}
.me-chat-line .message-container {
    margin-right: 10px;
    background: #7ab1d7;
    color: white;
}

</style>
