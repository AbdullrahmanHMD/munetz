const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/index.js', // Your entry point, typically src/index.js
  output: {
    path: path.resolve(__dirname, 'dist'), // Adjust if necessary to point to your 'Axiona Bot/dist'
    filename: 'react_bundle.js',
    clean: true, // Cleans the output directory before each build
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/, // Transform all js and jsx files
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'] // Presets used for transpiling
          }
        }
      },
      {
        test: /\.css$/, // Enables importing CSS in your JS/React components
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i, // Asset Loader
        type: 'asset/resource',
      },
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html' // Adjust as necessary
    })
  ],
  resolve: {
    extensions: ['.js', '.jsx'], // Automatically resolve certain extensions
  },
  devtool: 'source-map', // Include source maps
  mode: 'development', // Use 'production' for production builds
};
