<script lang="ts">
    export let size:number;
    export let thin:boolean = false;
</script>

<div class="spinner" style="width: {size}px; height: {size}px; border-width: {thin ? Math.floor(size / 20) : Math.floor(size / 6)}px"></div>

<style>
    .spinner{
        border-radius: 50%;
        border: 3px solid #36d5f8;
        border-bottom-color: transparent;
        animation: spin 1s linear infinite;
    }
    @keyframes spin{
        0% {
            transform: rotate(0deg);
        }
        100%{
            transform: rotate(360deg);
        }
    }
</style>