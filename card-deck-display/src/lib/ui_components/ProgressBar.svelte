<script lang='ts'>
    export let width:number;
    export let message:string
    import { StatusChoices } from "../../interfaces";

    export let status: StatusChoices;
    $: warning = status == StatusChoices.WARNING;
</script>

<div class="progress-container">
    <div class="progress-outer" class:warning>
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
        position: relative;
        background-color: rgb(33, 36, 36);
    }

    .progress-inner{
        height: 100%;
        background-color: var(--neon-green);
        transition: width 3s linear;
        width: 0;
    }

    .warning .progress-inner{
        background-color: var(--warning-primary) !important;
    }
    .warning .status-center{
        color: var(--running-light);
    }
</style>