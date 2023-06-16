<script type="ts">
    import type { StatusChoices } from "../../interfaces";
    import ColorInvertHeader from "../ui_components/ColorInvertHeader.svelte";
    import CornerBox from "../ui_components/CornerBox.svelte";
    import DotHeader from "../ui_components/Header.svelte";

    export let status:StatusChoices;
    export let leftHeader:any;
    export let rightHeader:any;
</script>

<CornerBox status={status}>
    <div class="flex-split">
        <ColorInvertHeader status={status}>{leftHeader}</ColorInvertHeader>
        <DotHeader status={status}>{rightHeader}</DotHeader>
    </div>

    <div class="flex-inline">
        <slot name="middle"></slot>
    </div>

    <hr>

    <slot name="bottom"></slot>
</CornerBox>

<style>
    .flex-split{
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }

    hr{
        border: none;
        border-top: 3px solid var(--running-light);
        margin-bottom: 20px;
    }
</style>