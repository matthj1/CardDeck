<script lang="ts">
    export let battery_level: 0 | 1 | 2 | 3;
</script>

{#if battery_level == 0}
    <div class="inline-battery empty">
        <i class="fa-solid fa-battery-empty"></i>Empty
    </div>
{:else if battery_level == 1}
    <div class="inline-battery low">
        <i class="fa-solid fa-battery-quarter"></i>Low
    </div>
{:else if battery_level == 2}
    <div class="inline-battery">
        <i class="fa-solid fa-battery-three-quarters"></i>Medium
    </div>
{:else if battery_level == 3}
    <div class="inline-battery">
        <i class="fa-solid fa-battery-full"></i>High
    </div>
{/if}

<style>
    i{
        font-size: 48px;
        margin-left: 40px;
        margin-right: 20px;
    }
    
    .inline-battery{
        display: flex;
        align-items: center;
        color: var(--running-light);
        text-transform: uppercase;
        font-size: 24px;
        font-weight: 500;
    }

    .low{
        color: var(--warning-primary);
    }

    .empty{
        color: var(--error-primary)
    }
</style>