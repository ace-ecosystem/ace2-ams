/* eslint-disable @typescript-eslint/no-var-requires */
const CircularDependencyPlugin = require("circular-dependency-plugin");
const SpeedMeasurePlugin = require("speed-measure-webpack-plugin");
const smp = new SpeedMeasurePlugin();

module.exports = {
  devServer: {
    proxy: {
      "^/api/": {
        target: "http://localhost:8888",
        ws: true,
        changeOrigin: true,
      },
    },
    watchOptions: {
      ignored: ["/node_modules/"],
      aggregateTimeout: 300,
      poll: 300,
    },
  },
  configureWebpack: smp.wrap({
    plugins: [
      new CircularDependencyPlugin({
        // exclude detection of files based on a RegExp
        exclude: /node_modules/,
        // add errors to webpack instead of warnings
        failOnError: true,
        // allow import cycles that include an asyncronous import,
        // e.g. via import(/* webpackMode: "weak" */ './file.js')
        allowAsyncCycles: false,
        // set the current working directory for displaying module paths
        cwd: process.cwd(),
      }),
    ],
  }),
};
