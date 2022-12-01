<script type="ts">
    import ColorInvertHeader from "../ui_components/ColorInvertHeader.svelte";
    import CornerBox from "../ui_components/CornerBox.svelte";
    import type { ITransferProps, IPACSRetrievingZipping, IPACSRunningResponse, IPACSFinishedResponse } from "../../interfaces";
    import {PACSRunningStatus, QueryStatus, StatusChoices} from "../../interfaces";
    import KvBox from "../ui_components/KVBox.svelte";
    import Spinner from "../ui_components/Spinner.svelte";
    import DotHeader from "../ui_components/DotHeader.svelte";
    import ProgressBar from "../ui_components/ProgressBar.svelte";
    import { setContext } from "svelte";
    import { writable } from "svelte/store";

    export let transfer: ITransferProps;    

    let status = writable<StatusChoices>(transfer.status)
    setContext("status", status)

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

<CornerBox error={transfer.status === StatusChoices.ERROR} warning={transfer.status === StatusChoices.WARNING}>
    <div class="flex-split">
        <ColorInvertHeader text={`${transfer.status===StatusChoices.ERROR?"ERROR ":""}${transfer.transfer_type === "RETRIEVE_SCAN"?"RETRIEVING SCAN":"RETRIEVING STUDY"}`}/>
        <DotHeader text={transfer.hospital}></DotHeader>
    </div>
    <div class="flex-inline">
        <KvBox key={"gateway"} value={transfer.gateway}/>
        <KvBox key={"gateway id"} value={transfer.gateway_id}/>
    </div>

    <hr>
    {#if transfer.query_status !== QueryStatus.ERROR}

    <div class="flex-inline">
        <Spinner size={22}/>
        <p class:warning={transfer.status===StatusChoices.WARNING} class="bolder upper">{getPACSMessage(transfer)}</p>
    </div>

    <ProgressBar width={calculateProgress(transfer.query_status, transfer.response)} message={getPACSMessage(transfer, true)}/>

    <KvBox key={"elapsed time"} value={transfer.elapsed}/>

    {:else}

    <p class="bigger bolder">{transfer.response.name}</p>
    <p>{transfer.response.message}</p>

    {/if}

</CornerBox>

<style>
    .flex-inline{
        display: flex;
        margin-bottom: 20px;
        gap: 20px;
        font-size: 22px;
        align-items: center;
    }

    .flex-split{
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }

    .bolder{
        font-weight: 500;
    }

    hr{
        border-top: 2px solid #a9f0ff;
        margin-bottom: 20px;
    }

    p{
        margin-top: 10px;
        margin-bottom: 10px;
        font-size: 18px;
    }
    
    .bigger{
        font-size: 25px;
        vertical-align: middle;
        color: #a9f0ff;
    }

    .warning{
        color: #ff9843;
    }
</style>