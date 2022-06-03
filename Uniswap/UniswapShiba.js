import {createClient} from 'urql'

const APIURL = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'

const tokensQuery = `{
    tokenDayDatas (where: {token: "0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce"})  {
      id
      date
          token {
        name
      }
      dailyTxns
    }
  }`


  const client = createClient({
    url: APIURL,
  })
  
  const data = await client.query(tokensQuery).toPromise()

  console.log(data);
