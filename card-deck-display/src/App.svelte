<script lang="ts">
  import CardMatrix from "./lib/card_renderer/CardMatrix.svelte";
  import TransferCard from "./lib/cards/TransferCard.svelte"
  import type {IInputData, ICardItem} from "./interfaces"
  import {StatusChoices} from "./interfaces"
  import { parallelFetch } from "./parallelFetch";
  import LoadingLogo from "./lib/ui_components/LoadingLogo.svelte";

  let data: IInputData[] = [];
  let cards: ICardItem[] = [];
  let auth_failure = false

  const cardTypeToComponent = {
    "PACS_TRANSFER": TransferCard,
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
      auth_failure = true;
      return [];
    }
    return flattenedData;
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
{#if !auth_token}
  <LoadingLogo status={StatusChoices.ERROR} message="No API token"/>
{:else if auth_failure}
  <LoadingLogo status={StatusChoices.ERROR} message="One or more endpoints returned 403. Please try a different token"/>
{:else}
  <CardMatrix historySize={3} cards={cards}></CardMatrix>
{/if}
</main>

<style>
  main{
    height: 100%;
  }
</style>