const { match } = require('assert');
const fs = require('fs');

const SOURSE_FILE_NAME = './kucoin/client.py'
const TARGET_FILE_NAME = './tests/test_private_requests_generated.py'
const METHOD_DEFINITION_MATCH = /def\s(\w+)/
const METHOD_CALL_MATCH = /self\.(\w+)\(/
const REQUEST_METHODS = ['_get', '_post', '_put', '_delete']
const METHOD_NAME_MATCH = /(\w+)\(/
const ARGUMENTS_MATCH = /\((.*)\)/
const REST_API_URL = 'https://api.kucoin.com'
const REST_FUTURES_API_URL = 'https://api-futures.kucoin.com'
const API_VERSIONS = {
    'API_VERSION': 'v1',
    'API_VERSION2': 'v2',
    'API_VERSION3': 'v3'
}

const MANDATORY_ARGS = [ // could be a dictionary with specific values
    'sub_user_id',
    'include_base_ammount',
    'sub_name',
    'passphrase',
    'remark',
    'api_key',
    'account_id',
    'account_type',
    'currency',
    'type',
    'client_oid',
    'amount',
    'from_account_type',
    'to_account_type',
    'pay_account_type',
    'withdrawal_id',
    'symbols',
    'symbol',
    'side',
    'order_list',
    'order_id',
    'cancel_size',
    'timeout',
    'stop_price',
    'size',
    'price',
    'limit_price',
    'orders_data',
    'trade_type',
    'interest_rate',
    'purchase_order_no'
]

function getPrivateMethodsArgumentsAndRequests (data) {
    const lines = data.split ('\n')
    lines.push('\n')
    const methods = {}
    let metodName = ''
    let methodArgs = []
    let lastMethodDefinition = ''
    for (let i = 0; i < lines.length; i++) {
        let line = lines[i]
        const methodDefinition = line.match (METHOD_DEFINITION_MATCH)
        const methodCall = line.match (METHOD_CALL_MATCH)
        if (methodDefinition) { // if line is method definition
            while (!line.includes (':')) {
                i++
                line += lines[i].trim()
            }
            lastMethodDefinition = line.replace ('def ', '')
                                        .replaceAll (' ', '')
                                        .replaceAll (',)', ')')
                                        .replace (':', '')
            continue // we need to check if this is private method
        } else if (methodCall) {
            let name = methodCall[1]
            if (!REQUEST_METHODS.includes (name)) { // if this is not request method just skip
                continue
            }
            if (line.endsWith ('(')) { // if request method is called not in one line
                i++
                let nextLine = lines[i].trim()
                while (nextLine !== ')') {
                    line += nextLine
                    i++
                    nextLine = lines[i].trim()
                }
                line += nextLine
            }
            if (line.match (/[^,]+, True/)) { // if request method is called with second argument True
                if (line.indexOf ('path') !== -1) {
                    continue // skip methods with path argument
                }
                [ metodName, methodArgs ] = getNameAndArgs (lastMethodDefinition)
                methods[metodName] = {
                    args: methodArgs,
                    request: getParamsFromRequestCall (line.trim ().replace ('return self._', '').replaceAll ("'", '"'))
                }
            }
        }
    }
    return methods
}

function getNameAndArgs (line) {
    let name = line.match (METHOD_NAME_MATCH)[1]
    let args = line.match (ARGUMENTS_MATCH)[1].trim().split (',').filter (arg => (arg !== 'self' && arg !== '**params'))
    return [ name, args ]
}

function getParamsFromRequestCall (line) {
    const matchMethodAndEndpointPattern = /(\w+)\("([^"]*)"/
    const matchFuturePattern = /is_futures=(\w+)/
    const matchVersionPattern = /version=self.(\w+)/
    const matchFormatPattern = /.format\((\w+)\)/
    const matchMethodAndEndpoint = line.match (matchMethodAndEndpointPattern)
    const matchFuture = line.match (matchFuturePattern)
    const matchVersion = line.match (matchVersionPattern)
    const isFutures = (matchFuture && matchFuture[1] === 'True') ? true : false
    const baseUrl = isFutures ? REST_FUTURES_API_URL : REST_API_URL
    const version = matchVersion ? API_VERSIONS[matchVersion[1]] : API_VERSIONS.API_VERSION
    let endpoint = matchMethodAndEndpoint[2]
    const matchFormat = line.match (matchFormatPattern)
    if (matchFormat) {
        endpoint = endpoint.replace (matchFormat[0], '').replace ('{}', '{' + matchFormat[1] + '}')
    }
    const url = baseUrl + '/api/' + version + '/' + endpoint
    return {
        full: line,
        url: url,
        method: matchMethodAndEndpoint[1],
        endpoint: endpoint,
        isFutures: isFutures,
    }
}

function generateTests (methods) {
    const tests = [
        'import requests_mock',
        'import pytest',
        'from aioresponses import aioresponses',
        '\n'
    ]
    const methodNames = Object.keys (methods)
    for (let methodName of methodNames) {
        const method = methods[methodName]
        let mandatoryArgs = generateMandatoryArgs (method)
        let functionArgs = ''
        for (let arg of mandatoryArgs) {
            functionArgs += '"' + arg + '", '
        }
        functionArgs = functionArgs.slice (0, -2)
        const request = method.request
        let url = request.url
        const paramInParth = url.match (/{(\w+)}/)
        if (paramInParth) {
            const param = paramInParth[1]
            mandatoryArgs = mandatoryArgs.filter (arg => arg !== param)
            url = url.replace (paramInParth[0], param)
        }

        const test = [
            'def test_' + methodName + '(client):',
            '    with requests_mock.mock() as m:',
            '        url = "' + url + '"',
            '        m.' + request.method + '(url, json={}, status_code=200)',
            '        client.' + methodName + '('+ functionArgs + ')',
        ]
        if (mandatoryArgs.length > 0) {
            if (request.method !== 'post' && request.method !== 'put') { // for methods without body
                for (let arg of mandatoryArgs) {
                    test.push ('        url = m.last_request._request.url')
                    test.push ('        assert "' + arg + '" in url')
                }
            } else {
                test.push ('        body = m.last_request._request.body')
                for (let arg of mandatoryArgs) {
                    test.push ('        assert "' + arg + '" in body')
                }
            }
        }
        const skipTest = methodName.indexOf ('futures_cancel_orders') !== -1 ||
                            (methodName.indexOf('order') !== -1 && (methodName.indexOf ('create') !== -1) || (methodName.indexOf ('modify') !== -1))
        test.push ('')
        if (skipTest) {
            // test for order creation must be commented for now
            console.log (methodName)
            test.unshift ('todo: update test for order creation/modification')
            for (let i = 0; i < test.length; i++) {
                test[i] = '# ' + test[i]
            }
        }
        tests.push (...test)
    }
    return tests.join ('\n')
}

function generateMandatoryArgs (method) {
    const args = method.args
    return args.filter (arg => arg.indexOf ('=') === -1)
}

function main () {
    fs.readFile (SOURSE_FILE_NAME, 'utf8', (err, data) => {
        if (err) {
            console.error (err)
            return
        }
        const privateMethodsArgumentsAndRequests = getPrivateMethodsArgumentsAndRequests (data)
        const tests = generateTests (privateMethodsArgumentsAndRequests)
        fs.writeFile (TARGET_FILE_NAME, tests, (err) => {
            if (err) {
                console.error (err)
                return
            }
            console.log (TARGET_FILE_NAME + ' file is generated')
        })
    })
}

main ()
