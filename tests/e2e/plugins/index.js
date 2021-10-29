/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable @typescript-eslint/no-var-requires */
/* eslint-disable arrow-body-style */

const { startDevServer } = require("@cypress/webpack-dev-server");
const webpackConfig = require("@vue/cli-service/webpack.config");

module.exports = (on, config) => {
  on("dev-server:start", (options) => {
    return startDevServer({
      options,
      webpackConfig,
    });
  });
};
