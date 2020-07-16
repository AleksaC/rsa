const path = require("path");
const merge = require("webpack-merge");
const common = require("./webpack.common.js");

const apiHost = process.env.API_HOST || "http://localhost:5000";

module.exports = merge(common, {
  mode: "development",
  devServer: {
    contentBase: path.resolve("./public"),
    proxy: {
      "/api": {
        target: apiHost,
        pathRewrite: { "^/api": "" },
      },
    },
    publicPath: "/",
    host: "0.0.0.0",
    port: 3000,
    hot: true,
  },
});
