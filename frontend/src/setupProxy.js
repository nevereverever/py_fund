const createProxyMiddleware = require('http-proxy-middleware');

module.exports = function (app) {
    // 若目标站点不提供跨域方法，则可以在调试时使用 http 代理中间件实现跨域
    // app.use(createProxyMiddleware('/api',
    //     {
    //         target: 'https://fundgz.1234567.com.cn',
    //         pathRewrite: {
    //             '^/api': '',
    //         },
    //         changeOrigin: true,
    //         secure: false, // 是否验证证书
    //         ws: true, // 启用websocket
    //     }
    // ));
};