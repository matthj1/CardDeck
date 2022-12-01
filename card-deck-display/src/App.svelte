<script lang="ts">
  import CardMatrix from "./lib/card_renderer/CardMatrix.svelte";
  import TransferCard from "./lib/cards/TransferCard.svelte"
  import ErrorCard from "./lib/cards/ErrorCard.svelte";
  import type {IInputData, ICardItem} from "./interfaces"
  import {StatusChoices} from "./interfaces"
  import { parallelFetch } from "./parallelFetch";

  let data: IInputData[] = [];
  let cards: ICardItem[] = [];

  const cardTypeToComponent = {
    "PACS_TRANSFER": TransferCard,
    "ERROR": ErrorCard
  }

  $: {
    cards = data.map(p => {
      return {
        type: p.type,
        id: p.id,
        component: cardTypeToComponent[p.type],
        props: {transfer: p}
      }
    })
  }

  const search = window.location.search
  const params = new URLSearchParams(search)
  const urls = params.getAll("url")
  const auth_token = params.get("token")

  async function getData(sources:string[], token:string):Promise<IInputData[]>{
    const sourcesWithOptions = sources.map(s => {return {url:s, options: {headers: {Authorization: `bearer ${token}`}}}})
    let allData = await parallelFetch<IInputData>(sourcesWithOptions)
    let flattenedData = allData.map(a => a.data).flat(1) 
    let allStatuses = allData.map(a => a.status)
    if(allStatuses.includes(403)){
      return [{
        type: "ERROR",
        id: 9999999999999,
        status: StatusChoices.ERROR
      }]
    }
    return flattenedData
  }

  async function poll(){
    if(auth_token){
      data = await getData(urls, auth_token)
    }
    setTimeout(poll, 3000)
  }

  poll()

</script>

<main>
<CardMatrix historySize={3} cards={cards}></CardMatrix>
</main>

<style>
  main{
    height: 100%;
  }
</style>