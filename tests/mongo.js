/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

//node --experimental-repl-await
const {MongoClient} = require('mongodb');

async function main(args) {
    console.log(args.dburi)
    const client = new MongoClient(args.dburi);
    await client.connect()
    console.log("client.connect() passed")
    const data = client.db().collection("data")
    await data.insertOne({"hello":"world"})        
    let res = []
    await data.find().forEach(x => res.push(x))
    await data.deleteMany({})
    return {
        "body": res
    }
}
