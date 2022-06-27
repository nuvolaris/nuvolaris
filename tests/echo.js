function main(args) {
    return {
        body: { 
            env: process.env,
            args: args
        }
    }
}