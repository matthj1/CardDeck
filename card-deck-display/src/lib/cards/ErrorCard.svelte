<script lang="ts">
    import CornerBox from "../ui_components/CornerBox.svelte";
    import ColorInvertHeader from "../ui_components/ColorInvertHeader.svelte";
    import DotHeader from "../ui_components/DotHeader.svelte";
    import { setContext } from "svelte";
    import { writable } from "svelte/store";
    import { StatusChoices } from "../../interfaces";

    let status = writable<StatusChoices>(StatusChoices.ERROR)
    setContext("status", status)
</script>

<CornerBox error={true}>
    <div class="flex-split">
        <ColorInvertHeader text={"Authentication Error"}/>
        <DotHeader text={"Cydar Card Deck Display"}></DotHeader>
    </div>

    <hr>

    <p class="error upper">Error authenticating 1 or more endpoints</p>
    <p class="error upper">Check token and try again</p>

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

    .error{
        color: var(--error-primary);
        font-size: 1.5rem;
    }

    .upper{
        text-transform: uppercase;
    }
</style>