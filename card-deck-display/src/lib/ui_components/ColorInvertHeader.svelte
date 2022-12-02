<script lang="ts">
    import { getContext } from "svelte";
    import type { Writable } from "svelte/store";
    import { StatusChoices } from "../../interfaces";
    export let text:string;

    const status:Writable<StatusChoices> = getContext("status");
</script>

<div class="color-invert-header upper"
class:running={$status === StatusChoices.RUNNING || StatusChoices.STALE}
class:error={$status === StatusChoices.ERROR}
class:warning={$status === StatusChoices.WARNING}>{text}</div>

<style>
    .color-invert-header{
        font-size: 28px;
        font-weight: 700;
        padding: 10px;
        width: fit-content;
    }
    .running{
        background-image: linear-gradient(135deg, var(--running-primary), var(--neon-green));
        color: rgb(19, 20, 20);
    }

    .error{
        background-image: linear-gradient(135deg, var(--error-primary), rgb(207, 36, 36));
        color:rgb(19, 20, 20);
    }

    .warning{
        background-image: linear-gradient(135deg, var(--warning-primary), rgb(230, 68, 47));
        color:rgb(19, 20, 20);
    }

</style>