module.exports = {
    publicPath:'/',
    outputDir:'../wana_home_back/front',
    assetsDir:'assets',
    devServer: {
        host: '127.0.0.1',
        port: 8080,
        open: false,
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000',
            },
        }
    },
}
