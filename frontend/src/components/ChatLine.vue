<template>
    <div class="bot-chat-line" v-if="isBot">
        <div class="avator-container">
            <img class="avator-icon" src="../assets/bot.png">
        </div>
        <div class="message-container">
            <span>{{ msg }}</span>
        </div>
    </div>
    <div class="me-chat-line" v-else>
      <div class="avator-container">
            <img class="avator-icon" src="../assets/profile.png">
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
    isBot: Boolean
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
    border: 1px solid #189ce2;
    border-radius: 50%;
}
.message-container {
    text-align: left;
    display: flex;
    align-items: center;
    white-space: pre-line;
}
.bot-chat-line .message-container {
    padding-left: 30px;
}
.me-chat-line .message-container {
    padding-right: 30px;
}

</style>
