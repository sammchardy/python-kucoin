import fs from 'fs'

const SOURSE_FILE_NAME = './kucoin/client.py'
const TARGET_FILE_NAME = './kucoin/async_methods.py'
const METHOD_DEFINITION_MATCH = /def\s(\w+)/
const METHOD_CALL_MATCH = /self\.(\w+)\(/
const DEFINITION_PREFIX = 'def'
const ASYNC_DEFINITION_PREFIX = 'async def'
const CALL_PREFIX = 'self.'
const ASYNC_CALL_PREFIX = 'await self.'
const SPECIAL_REPLACEMENTS = {} // Add special replacements here
const SPECIAL_REPLACEMENTS_KEYS = Object.keys (SPECIAL_REPLACEMENTS)

function replaceKeywords (data) {
    const lines = data.split ('\n')
    const asyncClient = [ ] as any
    for (let line of lines) {
        let specialMatch = false
        for (let key of SPECIAL_REPLACEMENTS_KEYS) {
            if (line.includes (key)) {
                asyncClient.push (line.replace (key, SPECIAL_REPLACEMENTS[key]))
                delete SPECIAL_REPLACEMENTS[key]
                specialMatch = true
                break
            }
        }
        if (specialMatch) {
            continue
        }
        if (line.startsWith('class Client(BaseClient):')) {
            asyncClient.push ('class AsyncClient(AsyncClientBase):')
            continue
        }
        if (line.startsWith('from base_client import BaseClient')) {
            asyncClient.push ('from async_client import AsyncClientBase')
            continue
        }
        const methodDefinition = line.match (METHOD_DEFINITION_MATCH)
        const methodCall = line.match (METHOD_CALL_MATCH)
        const match = methodDefinition || methodCall
        if (match) {
            const methodName = match[1]
            let replacementRequired = true
            if (methodName.startsWith ('_')) {
                replacementRequired = false
            }
            if (replacementRequired) {
                if (methodDefinition) {
                    line = line.replace (DEFINITION_PREFIX, ASYNC_DEFINITION_PREFIX)
                } else if (methodCall) {
                    line = line.replace (CALL_PREFIX, ASYNC_CALL_PREFIX)
                }
            }
        }
        asyncClient.push (line)
    }
    return asyncClient.join ('\n')
}

function main () {
    fs.readFile (SOURSE_FILE_NAME, 'utf8', (err, data) => {
        if (err) {
            console.error (err)
            return
        }
        const asyncClient = replaceKeywords (data)
        fs.writeFile (TARGET_FILE_NAME, asyncClient, (err) => {
            if (err) {
                console.error (err)
                return
            }
            console.log (TARGET_FILE_NAME + ' file is generated')})
        })
}

main ()
