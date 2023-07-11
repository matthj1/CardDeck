<script type="ts">
    import type {IAgentProps} from "../../interfaces";
    import BatteryIndicator from "../ui_components/BatteryIndicator.svelte";
    import KvBox from "../ui_components/KVBox.svelte";
    import ScrollingList from "../ui_components/ScrollingList.svelte";
    import GenericCard from "./GenericCard.svelte";

    export let item:IAgentProps;

</script>

<GenericCard status={item.status} leftHeader={`AGENT ${item.online?"ONLINE":"OFFLINE"}`} rightHeader={item.hospital}>
    <svelte:fragment slot="middle">
        <KvBox key="agent status" value={item.full_status} status={item.status}/>
        <KvBox key="agent id" value={item.agent_id} status={item.status}/>
    </svelte:fragment>

    <div class="floated-bottom" slot="bottom">
        <div class="top">
            <ScrollingList title={"Associated instances:"} items={item.assigned_instances}></ScrollingList>
        </div>
        {#if item.is_endpoint}
        <div class="bottom">
            <h2>Remote battery level:</h2>
            <BatteryIndicator battery_level={item.battery_level}></BatteryIndicator>
        </div>
        {/if}
    </div>
</GenericCard>

<style>
    h2{
        font-size: 18px;
        font-weight: 300;
        text-transform: uppercase;
    }
    .top{
        height: 150px;
    }
</style>