// vue.config.js

/**
 * @type {import('@vue/cli-service').ProjectOptions}
 * @argument {https://cli.vuejs.org/zh/config/#vue-config-js}
 */
 module.exports = {
    // 选项...
    publicPath: './',
    devServer: {

      host: '0.0.0.0',
      https: false,
      /* 使用代理 */
      proxy: {
          '/api': {
              /* 目标代理服务器地址 */
              target: 'http://127.0.0.1:5000/',
              /* 允许跨域 */
              changeOrigin: true,
          },
      }
    }
  }