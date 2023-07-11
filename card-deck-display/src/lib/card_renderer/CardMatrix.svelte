<script type="ts">
    import type {ICardItem, ICardArray} from "../../interfaces"
    import CardWrapper from "./CardWrapper.svelte";
    import {fade} from "svelte/transition"
    import LoadingLogo from "../ui_components/LoadingLogo.svelte";
    import { onMount } from "svelte";

    export let cards: ICardItem[];
    export let historySize: number;
    let height:number;
    let width:number;
    let displayNumberSlots: number = 1;
    let displayDimension: number = 1;
    let prevCardHistory: number[] = Array();
    let cardArray: ICardArray;
    let freeSlots: [number, number][] = [];
    let loading: HTMLDivElement;

    $: {
        cards;
        updateHistory();
        [displayNumberSlots, displayDimension] = calculateNumberOfSlots(prevCardHistory, displayNumberSlots);
        cardArray =  arrayToPosition(cards, cardArray);
    }


    // Calculate how many slots to create


    function updateHistory():void{
        if(prevCardHistory.length < historySize){
            prevCardHistory.push(cards.length)
        }
        else{
            prevCardHistory.shift()
            prevCardHistory.push(cards.length)
        }
    }

    function calculateNumberOfSlots(prevCardHistory:number[], currentNumberCards):number[]{
        const increase = candidateIncrease(prevCardHistory);
        const decrease = candidateDecrease(prevCardHistory, currentNumberCards, cards);
        if (increase > currentNumberCards){
            return [increase, Math.sqrt(increase)]
        }
        else if(decrease < currentNumberCards){
            return [decrease, Math.sqrt(decrease)];
        }
        return [currentNumberCards, Math.sqrt(currentNumberCards)];
    }

    function candidateIncrease(prevCardHistory:number[]):number{
        let largest = cards.length
        if (prevCardHistory.length){
            largest = Math.max(...prevCardHistory)
        }
        return nextLargerSquare(largest)
    }

    function candidateDecrease(prevCardHistory:number[], displayedNumberSlots:number, cards:ICardItem[]):number{
        if(!prevCardHistory.length){
            return displayedNumberSlots
        }
        if(prevCardHistory.every(n => n <= nextSmallerSquare(displayedNumberSlots))){
            return nextSmallerSquare(displayedNumberSlots)
        }
        return displayedNumberSlots
    }
    
    function nextLargerSquare(num:number):number{
        const sqrt = Math.ceil(Math.sqrt(num))
        return sqrt*sqrt
    }

    function nextSmallerSquare(num:number):number{
        const sqrt = Math.floor(Math.sqrt(num - 1))
        return sqrt*sqrt
    }


    // Populating the array


    function arrayToPosition(cards:ICardItem[], existing:ICardArray = []):ICardArray{
        let existingIDs = existing.map(p => p.id)
        let newIDs = cards.map(p => p.id)
        let cardsToRemove = existingIDs.filter(id => !newIDs.includes(id))
        let cardsToUpdate = existingIDs.filter(id => newIDs.includes(id))
        let cardsToAdd = newIDs.filter(id => !existingIDs.includes(id))

        // remove cards that aren't in the new array
        for(const cardToRemove of cardsToRemove){
            existing = existing.filter(p => p.id !== cardToRemove)
        }

        // update existing cards, preserving position
        for(const cardToUpdate of cardsToUpdate){
            const newCard = cards.find(p => p.id === cardToUpdate)
            const cardIndex = existing.findIndex(p => p.id === cardToUpdate)
            const existingCard = existing[cardIndex] as ICardItem
            const position = existingCard.position
            existing[cardIndex] = {...newCard, position: position}
        }

        calculateFreeSlots(existing, displayDimension)
        existing = clump(existing, displayDimension)

        // add new cards

        for(const cardToAdd of cardsToAdd){
            const newCard = cards.find(p => p.id === cardToAdd)
            const position = randomFreeSlot()
            calculateFreeSlots(existing, displayDimension)
            existing.push({...newCard, position: randomFreeSlot()})
        }

        return existing
    }

    function randomFreeSlot(){
        const index = Math.floor(Math.random() * freeSlots.length)
        return freeSlots[index]
    }

    function calculateFreeSlots(cardArray:ICardItem[], dimension:number):void{
        const takenSlots = cardArray.map(p => p.position)
        freeSlots = []
        for(let x = 0; x < dimension; x++){
            for(let y = 0; y < dimension; y++){
                const candidate:[number, number] = [x, y]
                const exists = takenSlots.find(slot => arrayIsEqual(slot, candidate))
                if(!exists){
                    freeSlots.push(candidate)
                }
            }
        }
    }

    function arrayIsEqual(arr1:any[], arr2:any[]):boolean{
        if(arr1.length === arr2.length){
            if(arr1.every((value, index) => arr2[index] === value)){
                return true
            }
        }
        return false
    }

    function clump(cardArray:ICardArray, displayDimension:number):ICardArray{
        for(let x = 0; x < cardArray.length; x++){
            const card = cardArray[x]
            // check if it's out of bounds
            if(card.position[0] >= displayDimension || card.position[1] >= displayDimension){
                // find the closest free slot by euclidian distance
                calculateFreeSlots(cardArray, displayDimension)
                const distances = freeSlots.map(slot => {
                    return {
                        coords: slot,
                        distance: Math.sqrt(Math.pow(card.position[0] - slot[0], 2) + Math.pow(card.position[1] - slot[1], 2))
                    }
                }
                )
                distances.sort((a, b) => a.distance - b.distance)[0].coords
                const closest = distances[0].coords
                card.position = closest
            }
        }
        return cardArray
    }


    // Display dimension and layout calculations


    function largest169Box(width:number, height:number):[number, number]{
        const targetRatio = 16/9;
        const screenRatio = width/height;
        const isTaller = screenRatio < targetRatio
        if(isTaller){
            const ratioUnit = width/16
            return [width, ratioUnit * 9]
        }
        else{
            const ratioUnit = height/9
            return [ratioUnit * 16, height]
        }
    }

    function calculateOffsets(screenWidth:number, screenHeight:number, targetWidth:number, targetHeight:number, dimension:number):{width:number, height:number, widthMultiplier:number, heightMultiplier:number}{
        let widthTotalOffset = screenWidth - targetWidth
        let heightTotalOffset = screenHeight - targetHeight
        return {
            width: widthTotalOffset === 0 ? 0:widthTotalOffset/2,
            height: heightTotalOffset === 0 ? 0 : heightTotalOffset/2,
            widthMultiplier: targetWidth/dimension,
            heightMultiplier: targetHeight/dimension
        }
    }

    function coordsToAbsolutePosition(coords:[number, number], dimension:number, screenWidth:number, screenHeight:number):{top: number, left:number, scale:number}{
        let [row, column] = coords
        let [targetWidth, targetHeight] = largest169Box(width, height);
        let offsets = calculateOffsets(screenWidth, screenHeight, targetWidth, targetHeight, dimension)
        return {
            top: (row * offsets.heightMultiplier) + offsets.height,
            left: (column * offsets.widthMultiplier) + offsets.width,
            scale: targetWidth / (dimension * 960)
        }
    }

    function hideAfterAnimation(element:HTMLElement){
        console.log("hiding stuff...")
        element.style.display = "none";
    }

</script>

<svelte:window bind:innerWidth={width} bind:innerHeight={height}/>

{#if cardArray}
<div bind:this={loading} class="placeholder-center fade-immediately" on:animationend={()=>hideAfterAnimation(loading)}>
    <LoadingLogo/>
</div>
{/if}
{#each cardArray as card (card.id)}
    <CardWrapper status={card.status} {card} {...coordsToAbsolutePosition(card.position, displayDimension, width, height)}></CardWrapper>
{:else}
    <div out:fade={{duration: 2000}} class="placeholder-center">
        <LoadingLogo message={"no cards to display"}/>
    </div>
{/each}


<style>
    .placeholder-center{
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        flex-direction: column;
        gap: 30px;
    }

    .fade-immediately{
        animation: fade 2000ms;
        opacity: 0;
    }
    @keyframes fade{
        0%{
            opacity: 1;
        }
        50%{
            opacity: 1;
        }
        100%{
            opacity: 0;
        }
    }
</style>