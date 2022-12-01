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
        background-image: linear-gradient(135deg, rgb(48, 207, 247), rgb(20, 236, 172));
        color: rgb(19, 20, 20);
    }

    .error{
        background-image: linear-gradient(135deg, #ff5443, rgb(207, 36, 36));
        color:rgb(19, 20, 20);
        /* box-shadow: 0px 0px 14px 10px #662019; */
        animation: box-glow-error 600ms linear 0s infinite alternate;
    }

    .warning{
        background-image: linear-gradient(135deg, #ff9843, rgb(230, 47, 62));
        color:rgb(19, 20, 20);
        /* box-shadow: 0px 0px 14px 10px #664219; */
        animation: box-glow-warning 600ms linear 0s infinite alternate;
    }

</style>