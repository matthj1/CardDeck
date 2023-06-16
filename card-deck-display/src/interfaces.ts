import type { SvelteComponent } from "svelte";

export interface ICardItem{
    type: string;
    id: number|string;
    status: StatusChoices;
    position?: [number, number];
    component: typeof SvelteComponent;
    props: any;
}

export type ICardArray = ICardItem[]

export interface IInputData{
    id: number|string;
    status: StatusChoices;
    type: string;
}

export enum StatusChoices{
    STALE = "STALE",
    WARNING = "WARN",
    ERROR = "ERROR",
    RUNNING = "RUN"
}

export interface IParrallelFetchData<T>{
    url:string;
    status: number;
    data: T[];
}

// --------------------------

export interface ITransferPropsBase extends IInputData{
    query_id: string;
    hospital: string;
    gateway: string;
    gateway_id: number;
    response: any;
    elapsed: string;
    transfer_type: "RETRIEVE_STUDY"|"RETRIEVE_SCAN";
}

export type ITransferProps = ITransferPropsNew | ITransferPropsQueued | ITransferPropsRunning | ITransferPropsError | ITransferPropsFinished

export enum QueryStatus {
    NEW = "NEW",
    QUEUED = "QUE",
    RUNNING = "RUN",
    FINISHED = "FIN",
    ERROR = "ERR",
}

export interface ITransferPropsNew extends ITransferPropsBase{
    query_status: QueryStatus.NEW;
}

export interface ITransferPropsQueued extends ITransferPropsBase{
    query_status: QueryStatus.QUEUED;
}

export interface ITransferPropsRunning extends ITransferPropsBase{
    query_status: QueryStatus.RUNNING;
    response: IPACSRetrievingZipping|IPACSRunningResponse;
}

export interface ITransferPropsFinished extends ITransferPropsBase{
    query_status: QueryStatus.FINISHED;
    response: IPACSFinishedResponse;
}

export interface ITransferPropsError extends ITransferPropsBase{
    query_status: QueryStatus.ERROR;
    response: IPACSErrorResponse;
}


export enum PACSRunningStatus{
    started = "started",
    retrieving = "retrieving",
    waiting_silo = "waiting_silo",
    collecting = "collecting",
    zipping = "zipping",
    uploading = "uploading",
    upload_transfer_complete = "upload_transfer_complete",
    finished = "finished"
}

export interface IPACSRunningResponse{
    status: PACSRunningStatus.collecting | PACSRunningStatus.upload_transfer_complete | PACSRunningStatus.started | PACSRunningStatus.waiting_silo;
}

export interface IPACSRetrievingZipping{
    status: PACSRunningStatus.retrieving|PACSRunningStatus.zipping|PACSRunningStatus.uploading;
    completed: number;
    total: number;
}

export interface IPACSFinishedResponse{
    status: PACSRunningStatus.finished;
    response: {redirect:string};
}

export interface IPACSErrorResponse{
    name: string;
    message: string;
}

export interface IAgentProps extends IInputData{
    hospital: string;
    online: boolean;
    full_status: string;
    agent_id: number;
    assigned_instances: string[];
}