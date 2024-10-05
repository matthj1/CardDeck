<script type="ts">
    import type { ITransferProps, IPACSRetrievingZipping, IPACSRunningResponse, IPACSFinishedResponse} from "../../interfaces";
    import {PACSRunningStatus, QueryStatus, StatusChoices} from "../../interfaces";
    import KvBox from "../ui_components/KVBox.svelte";
    import Spinner from "../ui_components/Spinner.svelte";
    import ProgressBar from "../ui_components/ProgressBar.svelte";
    import GenericCard from "./GenericCard.svelte";

    export let item: ITransferProps;

    export function getMessageAndProgress(query:ITransferProps): {message: string, progress: number, extra?: string}{
        let progressString:string;
        switch (query.query_status){
            case QueryStatus.NEW:
                return {
                    message: "Sending request...",
                    progress: 0
                };
            case QueryStatus.QUEUED:
                return {
                    message: "Waiting in the queue",
                    progress: 5
                };
            case QueryStatus.RUNNING:
                switch (query.response.status){
                    case PACSRunningStatus.started:
                        return {
                            message: "Initiating transfer",
                            progress: 10
                        };
                    case PACSRunningStatus.retrieving:
                        return {
                            message: "Importing from PACS",
                            progress: 10 + Math.floor((query.response.completed/query.response.total) * 40),
                            extra: `${query.response.completed} of ${query.response.total}`
                        };
                    case PACSRunningStatus.waiting_silo:
                        return {
                            message: "Waiting for further images",
                            progress: 55
                        };
                    case PACSRunningStatus.collecting:
                        return {
                            message: "Collecting images",
                            progress: 60
                        };
                        case PACSRunningStatus.zipping:
                        return {
                            message: "Packaging images",
                            progress: 60 + Math.floor((query.response.completed/query.response.total) * 10),
                            extra: `${query.response.completed} of ${query.response.total}`
                        };
                    case PACSRunningStatus.uploading:
                        return {
                            message: `Uploading to Cydar`,
                            progress: 70 + Math.floor((query.response.completed/query.response.total) * 30),
                            extra: `${query.response.completed} of ${query.response.total}`
                        };
                    case PACSRunningStatus.upload_transfer_complete:
                        return {
                            message: "Preparing study",
                            progress: 100
                        };
                    default:
                        return {
                            message: "",
                            progress: 100
                        };
                }
        }
        return {
            message: "",
            progress: 100
        }
    }

    $: progressReport = getMessageAndProgress(item);
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

        <div class="flex-inline fixed-height">
            <Spinner size={22}/>
            <p class:warning={item.status===StatusChoices.WARNING} class="bolder upper">{progressReport.message}</p>
        </div>
        <ProgressBar status={item.status} width={progressReport.progress} message={`${progressReport.message} ${progressReport.extra ? progressReport.extra : ""}`}/>
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

    .fixed-height{
        height: 30px;
    }
</style>