<script lang="ts">
    import { StatusChoices } from "../../interfaces";

    export let status: StatusChoices;
    $: error = status == StatusChoices.ERROR;
    $: warning = status == StatusChoices.WARNING;
</script>

<div class="color-invert-header upper" class:error class:warning>
<slot></slot>
</div>

<style>
    .color-invert-header{
        font-size: 28px;
        font-weight: 700;
        padding: 10px;
        width: fit-content;
        text-align: center;
        flex-basis: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 106px;
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