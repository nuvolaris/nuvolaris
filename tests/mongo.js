//node --experimental-repl-await
const {MongoClient} = require('mongodb');

async function main(args) {
    const client = new MongoClient(args.dburi);
    await client.connect()
    const data = client.db().collection("data")
    await data.insertOne({"hello":"world"})        
    let res = []
    await data.find().forEach(x => res.push(x))
    await data.deleteMany({})
    return {
        "body": res
    }
}
