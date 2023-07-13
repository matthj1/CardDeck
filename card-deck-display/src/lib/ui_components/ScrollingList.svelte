<script lang="ts">
    import { onMount } from "svelte";

    export let title:string;
    export let items:string[];
    let listBody:HTMLUListElement;

    function isScrollable(element:HTMLElement){
        return element.scrollHeight > element.clientHeight
    }

    function scroll(){
        // check if you can scroll up, if so do it, else, scroll down
        if(listBody.scrollTop > 0){
            listBody.scrollTop = 0;
        }
        else{
            listBody.scrollTop = 100;
        }
        window.setTimeout(scroll, 5000);
    }

    onMount(()=>{
        if(isScrollable(listBody)){
            scroll()
        }
    })
</script>

<h2>{title}</h2>
<ul bind:this={listBody}>
    {#each items as item}
    <li>{item}</li>
    {/each}
</ul>

<style>
    h2{
        font-size: 18px;
        font-weight: 300;
        text-transform: uppercase;
        }
    ul{
        max-height: 100px;
        overflow: hidden;
        scroll-behavior: smooth;
        list-style: none;
        font-weight: 500;
        font-size: 24px;
        vertical-align: middle;
        color: var(--running-light);
        text-transform: uppercase;
        margin: 0;
    }
</style>
