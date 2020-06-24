module.exports = {
    publicPath: process.env.NODE_ENV === 'prod'
        ? '/'
        : '/',
    devServer: {
        disableHostCheck: true
    }
}