<script lang='ts'>
    import { StatusChoices } from "../../interfaces";

    export let status: StatusChoices;
    $: error = status == StatusChoices.ERROR;
    $: warning = status == StatusChoices.WARNING;

</script>

<h1 class:error class:warning class="upper">
<slot></slot>
</h1>

<style>    
    h1{
        font-size: 28px;
        font-weight: 500;
        padding: 10px;
        text-transform: uppercase;
        text-align: center;
        flex-basis: 480px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-shadow: 1px 1px 10px #136375;
    }

    .error{
        color: var(--error-primary);
        text-shadow: 1px 1px 10px #662019;
    }

    .warning{
        color: var(--warning-primary);
        text-shadow: 1px 1px 10px #664219;
    }
</style>