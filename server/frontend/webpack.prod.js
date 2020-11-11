const path = require("path")
const common = require("./webpack.common")

const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const HtmlWebpackPlugin = require("html-webpack-plugin")

const {merge} = require("webpack-merge")
const {CleanWebpackPlugin} = require("clean-webpack-plugin")

module.exports = merge(common, {
    mode: "production",
    output: {
        filename: '[name]-bundle.js',
        path: path.resolve(__dirname, "./static/frontend"),
        publicPath: "/frontend/static/frontend/"     
    },
    optimization: {
        minimize: false,
        splitChunks: {
            chunks: "all",
        }
    },
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",
                    "sass-loader",
                ],
            },
        ],
    },
    plugins : [
        new MiniCssExtractPlugin({
            filename: "[name].css",
        }),
        new CleanWebpackPlugin(),
    ],
})