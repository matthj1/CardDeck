<script lang='ts'>
    import { getContext } from "svelte";
    import type { Writable } from "svelte/store";
    import { StatusChoices } from "../../interfaces";    
    export let width:number;
    export let message:string

    const status:Writable<StatusChoices> = getContext("status");
</script>

<div class="progress-container">
    <div class="progress-outer" class:warning = {$status === StatusChoices.WARNING}>
        <div class="progress-inner" style="width: {width}%;"></div>
        <div class="status-center upper">{message}</div>
    </div>
</div>

<style>
    .progress-container{
        margin-bottom: 40px;
    }

    .status-center{
        width: 100%;
        text-align: center;
        position: absolute;
        font-size: 16px;
        top: 8px;
        mix-blend-mode: difference;
    }

    .progress-outer{
        width: 100%;
        height: 40px;
        border: 1px solid #00f49f;
        position: relative;
    }

    .progress-inner{
        height: 100%;
        background-color: #00f49f;
        transition: width 3s linear;
        width: 0;
    }

    .warning.progress-outer{
        border: 1px solid #ff9843;
    }
    .warning .progress-inner{
        background-color: #ff9843 !important;
    }
    .warning .status-center{
        color: #a9f0ff;
    }
</style>