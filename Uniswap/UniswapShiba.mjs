import pkg from 'urql'
import * as fs from 'fs'
import 'isomorphic-unfetch'
const {createClient} = pkg;
const APIURL = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'

const client = createClient({
    url: APIURL,
  });
  var intervals = [1596067200, 1604880000, 1616198400, 1624838400, 1633478400, 1642118400]
  for (var i = 0; i < intervals.length; i++) {
    var tokensQuery = `{
        tokenDayDatas (where: {date_gt: ` + intervals[i].toString() + ` token: "0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce"})  {
          id
          date
              token {
            name
          }
          dailyTxns
        }
    }`
   const data = await client.query(tokensQuery).toPromise()
   for (const token of data.data.tokenDayDatas) {
       var writeLine = token["date"] + "," + token["dailyTxns"] + "\n";
       fs.writeFile('uniswapEther.csv', writeLine, { flag: 'a+' }, err => {});
   }
  }
  
  
  
