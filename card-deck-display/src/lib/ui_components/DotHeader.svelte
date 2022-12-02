<script lang='ts'>
    import { getContext } from "svelte";
    import type { Writable } from "svelte/store";
    import { StatusChoices } from "../../interfaces";
    export let text:string;

    const status:Writable<StatusChoices> = getContext("status");
</script>

<h1 class="upper"
class:running={$status === StatusChoices.RUNNING || $status === StatusChoices.STALE}
class:error={$status === StatusChoices.ERROR}
class:warning={$status === StatusChoices.WARNING}>. : {text} : .</h1>

<style>
    .error{
        color: var(--error-primary);
        text-shadow: 1px 1px 10px #662019;
    }

    .warning{
        color: var(--warning-primary);
        text-shadow: 1px 1px 10px #664219;
    }

    .running{
        text-shadow: 1px 1px 10px #136375;
    }

    h1{
        font-size: 28px;
        font-weight: 500;
        padding: 10px;
        text-transform: uppercase;
    }
</style>