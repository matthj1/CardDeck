<script lang="ts">
    export let error:boolean = false;
    export let warning:boolean = false;
</script>

<div class="corner-container" class:error={error} class:warning={warning}>
    <div class="top left"></div>
    <div class="top right"></div>
    <div class="bottom right"></div>
    <div class="bottom left"></div>
    <slot></slot>
</div>

<style>
    .corner-container {
        position: relative;
        padding: 50px;
        width: 100%;
        height: 100%;
        background-color: #131414;
        border: 2px solid #1f2020;
    }

    .top, .bottom {
        position: absolute;
        width: 30px;
        height: 30px;
        background-color: transparent;
        opacity: 0.4;
    }

    .error .top, .error .bottom{
        border-color: var(--error-primary) !important;
    }

    .warning .top, .warning .bottom{
        border-color: var(--warning-primary) !important;
    }

    .top {
        top: 5px;
        border-top: 4px solid rgb(88, 88, 88);
    }

    .bottom {
        bottom: 5px;
        border-bottom: 4px solid rgb(88, 88, 88);
    }

    .left {
        left: 5px;
        border-left: 4px solid rgb(88, 88, 88);
    }

    .right {
        right: 5px;
        border-right: 4px solid rgb(88, 88, 88);
    }
</style>