<script type="ts">
    import type { ITransferProps, IPACSRetrievingZipping, IPACSRunningResponse, IPACSFinishedResponse} from "../../interfaces";
    import {PACSRunningStatus, QueryStatus, StatusChoices} from "../../interfaces";
    import KvBox from "../ui_components/KVBox.svelte";
    import Spinner from "../ui_components/Spinner.svelte";
    import ProgressBar from "../ui_components/ProgressBar.svelte";
    import GenericCard from "./GenericCard.svelte";

    export let item: ITransferProps;

    export function getPACSMessage(query:ITransferProps, showFraction:boolean = false):string{
        let progressString:string;
        switch (query.query_status){
            case QueryStatus.NEW:
                return "Sending request..."
            case QueryStatus.QUEUED:
                return "Waiting in the queue"
            case QueryStatus.RUNNING:
                switch (query.response.status){
                    case PACSRunningStatus.started:
                        return "Initiating transfer"
                    case PACSRunningStatus.retrieving:
                        progressString = `: ${query.response.completed} of ${query.response.total}`
                        return `Importing from PACS${showFraction ? progressString : ""}` 
                    case PACSRunningStatus.waiting_silo:
                        return "Waiting for further images"
                    case PACSRunningStatus.collecting:
                        return "Collecting images"
                        case PACSRunningStatus.zipping:
                        progressString = `: ${query.response.completed} of ${query.response.total}`
                        return `Packaging images${showFraction ? progressString : ""}`
                    case PACSRunningStatus.uploading:
                        progressString = `: ${query.response.completed} of ${query.response.total}`
                        return `Uploading to Cydar${showFraction ? progressString : ""}`
                    case PACSRunningStatus.upload_transfer_complete:
                        return "Preparing study"
                    default:
                        return ""
                }
        }
        return ""
    }

    export function calculateProgress(status:QueryStatus, response:IPACSRetrievingZipping|IPACSRunningResponse|IPACSFinishedResponse):number{
        switch(status){
            case QueryStatus.NEW:
                return 0;
            case QueryStatus.QUEUED:
                return 5;
            case QueryStatus.RUNNING:
                switch(response.status){
                    case PACSRunningStatus.started:
                        return 10;
                    case PACSRunningStatus.retrieving:
                        return 10 + Math.floor((response.completed/response.total) * 40); //up to 50% complete
                    case PACSRunningStatus.waiting_silo:
                        return 55;
                    case PACSRunningStatus.collecting:
                        return 60;
                    case PACSRunningStatus.zipping:
                        return 60 + Math.floor((response.completed/response.total) * 10); // up to 70%
                    case PACSRunningStatus.uploading:
                        return 70 + Math.floor((response.completed/response.total) * 30); // 70 to 100%
                    case PACSRunningStatus.upload_transfer_complete:
                        return 100;
                }
            case QueryStatus.FINISHED:
                return 100;
            default:
                return 0;
        }
    }
</script>

<GenericCard 
status={item.status} 
leftHeader={`${item.status===StatusChoices.ERROR?"ERROR ":""}${item.transfer_type === "RETRIEVE_SCAN"?"RETRIEVING SCAN":"RETRIEVING STUDY"}`}
rightHeader={item.hospital}>
    <svelte:fragment slot="middle">
        <KvBox key={"gateway"} value={item.gateway} status={item.status}/>
        <KvBox key={"gateway id"} value={item.gateway_id} status={item.status}/>
        <KvBox key={"transfer started"} value={item.started} status={item.status}/>
    </svelte:fragment>

    <svelte:fragment slot="bottom">
        {#if item.query_status !== QueryStatus.ERROR}

        <div class="flex-inline">
            <Spinner size={22}/>
            <p class:warning={item.status===StatusChoices.WARNING} class="bolder upper">{getPACSMessage(item)}</p>
        </div>
    
        <ProgressBar status={item.status} width={calculateProgress(item.query_status, item.response)} message={getPACSMessage(item, true)}/>
    
        <KvBox key={"elapsed time"} value={item.elapsed} status={item.status}/>
        {:else}
    
        <p class="bigger bolder">{item.response.name}</p>
        <p class="error">{item.response.message}</p>
    
        {/if}
    </svelte:fragment>

</GenericCard>

<style>
    .warning{
        color: var(--warning-primary);
    }

    .error{
        color: var(--error-primary)
    }
</style>