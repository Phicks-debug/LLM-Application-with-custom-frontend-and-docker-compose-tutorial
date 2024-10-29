const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  return {
    setupMiddlewares: (middlewares, devServer) => {
      if (!devServer) {
        throw new Error('webpack-dev-server is not defined');
      }

      middlewares.unshift(
        createProxyMiddleware('/api', {
          target: 'http://api:5000',
          changeOrigin: true,
        })
      );

      middlewares.unshift((req, res, next) => {
        res.header('Access-Control-Allow-Origin', '*');
        next();
      });

      return middlewares;
    },
  };
};