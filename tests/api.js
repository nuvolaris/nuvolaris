const openwhisk = require('openwhisk');

function main(args) {
    var ow = openwhisk();
    //return { "body": "boh"}
    return ow.actions.list()
    .then(l => ({body: {result: l}}))
    .catch(e => ({body: {error: e}}))
    
}

exports.main = main