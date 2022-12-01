<script lang="ts">
    import { getContext } from "svelte";
    import type { Writable } from "svelte/store";
    import { StatusChoices } from "../../interfaces";
    
    export let key:string;
    export let value:string|number;

    const status:Writable<StatusChoices> = getContext("status")
</script>

<p><span class:error={$status === StatusChoices.ERROR} class:warning={$status === StatusChoices.WARNING} class="key">{key}: </span><span class="value">{value}</span></p>

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
        font-size: 25px;
        vertical-align: middle;
        color: #a9f0ff;
        text-transform: uppercase;
    }
    .error{
        color: #ff5443;
    }
    .warning{
        color: #ff9843;
    }
</style>