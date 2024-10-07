<script lang="ts">
    import { StatusChoices } from "../../interfaces";
    
    export let key:string;
    export let value:string|number;
    export let status:StatusChoices;
    $: error = status == StatusChoices.ERROR;
    $: warning = status == StatusChoices.WARNING;
</script>

<p>
    <span class:error class:warning class="key">{key}: </span>
    <span class="value">{value}</span>
</p>

<style>
    p{
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .key{
        font-size: 18px;
        font-weight: 300;
        text-transform: uppercase;
    }
    .value{
        font-weight: 500;
        font-size: 24px;
        vertical-align: middle;
        color: var(--running-light);
        text-transform: uppercase;
        display: inline-block;
        max-width: 350px;
    }
    .error{
        color: var(--error-primary);
    }
    .warning{
        color: var(--warning-primary);
    }
</style>