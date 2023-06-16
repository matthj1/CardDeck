<script type="ts">
    import type {IAgentProps} from "../../interfaces";
    import KvBox from "../ui_components/KVBox.svelte";
    import GenericCard from "./GenericCard.svelte";

    export let item:IAgentProps;

</script>

<GenericCard status={item.status} leftHeader={`AGENT ${item.online?"ONLINE":"OFFLINE"}`} rightHeader={item.hospital}>
    <svelte:fragment slot="middle">
        <KvBox key="agent status" value={item.full_status} />
        <KvBox key="agent id" value={item.agent_id} />
    </svelte:fragment>

    <svelte:fragment slot="bottom">
        <h2>Associated instances:</h2>
        <ul>
            {#each item.assigned_instances as instance}
            <li>{instance}</li>
            {/each}
        </ul>
    </svelte:fragment>
</GenericCard>

<style>
    h2{
        font-size: 18px;
        font-weight: 300;
        text-transform: uppercase;
    }

    ul{
        list-style: none;
        font-weight: 500;
        font-size: 25px;
        vertical-align: middle;
        color: var(--running-light);
        text-transform: uppercase;
    }
</style>