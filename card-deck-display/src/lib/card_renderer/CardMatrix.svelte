<script type="ts">
    import type {ICardItem, ICardArray} from "../../interfaces"
    import CardWrapper from "./CardWrapper.svelte";
    import {fade} from "svelte/transition"
    import LoadingLogo from "../ui_components/LoadingLogo.svelte";

    export let cards: ICardItem[];
    export let historySize: number;
    let height:number;
    let width:number;
    let displayNumberSlots: number = 1;
    let displayDimension: number = 1;
    let prevCardHistory: number[] = Array();
    let cardArray: ICardArray;
    let freeSlots: [number, number][] = [];

    $: {
        cards;
        updateHistory();
        [displayNumberSlots, displayDimension] = calculateNumberOfSlots(prevCardHistory, displayNumberSlots);
        cardArray =  arrayToPosition(cards, cardArray);
    }


    // Poor man's FIFO Queue
    function updateHistory():void{
        if(prevCardHistory.length < historySize){
            prevCardHistory.push(cards.length);
        }
        else{
            prevCardHistory.shift();
            prevCardHistory.push(cards.length);
        }
    }

    // Calculate how many slots to create for cards, in square numbers
    function calculateNumberOfSlots(prevCardHistory:number[], currentNumberCards: number):number[]{
        const increase = candidateIncrease(prevCardHistory);
        const decrease = candidateDecrease(prevCardHistory, currentNumberCards);
        if (increase > currentNumberCards){
            return [increase, Math.sqrt(increase)];
        }
        else if(decrease < currentNumberCards){
            return [decrease, Math.sqrt(decrease)];
        }
        return [currentNumberCards, Math.sqrt(currentNumberCards)];
    }

    function candidateIncrease(prevCardHistory:number[]):number{
        let largest = cards.length;
        if (prevCardHistory.length){
            largest = Math.max(...prevCardHistory);
        }
        return nextLargerSquare(largest);
    }

    // Calculate the first number which is lower than number of cards, who's square root is an integer
    // Example, 7 cards would return 4
    // Then, check that every item in the history is less than or equal to that
    // This causes the number of slots to only decrease if there's been less cards than slots for the length of history
    function candidateDecrease(prevCardHistory:number[], displayedNumberSlots:number):number{
        if(!prevCardHistory.length){
            return displayedNumberSlots;
        }
        if(prevCardHistory.every(n => n <= nextSmallerSquare(displayedNumberSlots))){
            return nextSmallerSquare(displayedNumberSlots);
        }
        return displayedNumberSlots;
    }
    
    function nextLargerSquare(num:number):number{
        const sqrt = Math.ceil(Math.sqrt(num));
        return sqrt*sqrt;
    }

    function nextSmallerSquare(num:number):number{
        const sqrt = Math.floor(Math.sqrt(num - 1));
        return sqrt*sqrt;
    }


    // Find a position for each card
    // Example, 0, 0 would be the top left card
    function arrayToPosition(cards:ICardItem[], existing:ICardArray = []):ICardArray{
        const existingIDs = existing.map(p => p.id);
        const newIDs = cards.map(p => p.id);
        const cardsToRemove = existingIDs.filter(id => !newIDs.includes(id));
        const cardsToUpdate = existingIDs.filter(id => newIDs.includes(id));
        const cardsToAdd = newIDs.filter(id => !existingIDs.includes(id));

        // remove cards that aren't in the new array
        for(const cardToRemove of cardsToRemove){
            existing = existing.filter(p => p.id !== cardToRemove);
        }

        // update existing cards, preserving position
        for(const cardToUpdate of cardsToUpdate){
            const newCard = cards.find(p => p.id === cardToUpdate);
            const cardIndex = existing.findIndex(p => p.id === cardToUpdate);
            const existingCard = existing[cardIndex] as ICardItem;
            const position = existingCard.position;
            existing[cardIndex] = {...newCard, position: position};
        }

        // work out which slots are free
        calculateFreeSlots(existing, displayDimension);
        // move the existing cards to a free slot
        existing = clump(existing, displayDimension);

        // add new cards
        for(const cardToAdd of cardsToAdd){
            const newCard = cards.find(p => p.id === cardToAdd);
            calculateFreeSlots(existing, displayDimension);
            existing.push({...newCard, position: randomFreeSlot()});
        }

        return existing;
    }

    function randomFreeSlot(){
        const index = Math.floor(Math.random() * freeSlots.length);
        return freeSlots[index];
    }

    // populate the freeSlots array
    function calculateFreeSlots(cardArray:ICardItem[], dimension:number):void{
        const takenSlots = cardArray.map(p => p.position);
        freeSlots = [];
        for(let x = 0; x < dimension; x++){
            for(let y = 0; y < dimension; y++){
                const candidate:[number, number] = [x, y];
                const exists = takenSlots.find(slot => arrayIsEqual(slot, candidate));
                if(!exists){
                    freeSlots.push(candidate);
                }
            }
        }
    }

    // checks for array item equality such that [0, 0] == [0, 0]
    function arrayIsEqual(arr1:any[], arr2:any[]):boolean{
        if(arr1.length === arr2.length){
            if(arr1.every((value, index) => arr2[index] === value)){
                return true;
            }
        }
        return false;
    }

    // move cards into the nearest free slot when the number of slots decreases
    function clump(cardArray:ICardArray, displayDimension:number):ICardArray{
        for(const card of cardArray){
            // check if it's out of bounds
            if(card.position[0] >= displayDimension || card.position[1] >= displayDimension){
                // find the closest free slot by euclidian distance
                calculateFreeSlots(cardArray, displayDimension);
                const distances = freeSlots.map(slot => {
                    return {
                        coords: slot,
                        distance: Math.sqrt(Math.pow(card.position[0] - slot[0], 2) + Math.pow(card.position[1] - slot[1], 2))
                    };
                }
                )
                distances.sort((a, b) => a.distance - b.distance)[0].coords;
                const closest = distances[0].coords;
                card.position = closest;
            }
        }
        return cardArray;
    }


    // Display dimension and layout calculations

    // Calculations are based on the display area having a 16:9 aspect ratio
    // If the screen isn't 16:9, find the largest 16:9 dimensions that will fit
    function largest169Box(width:number, height:number):[number, number]{
        const targetRatio = 16/9;
        const screenRatio = width/height;
        const isTaller = screenRatio < targetRatio;
        if(isTaller){
            const ratioUnit = width/16;
            return [width, ratioUnit * 9];
        }
        else{
            const ratioUnit = height/9;
            return [ratioUnit * 16, height];
        }
    }

    // Calculate the change in position required to fit everything into the largest 16:9 box
    function calculateOffsets(screenWidth:number, screenHeight:number, targetWidth:number, targetHeight:number, dimension:number):{width:number, height:number, widthMultiplier:number, heightMultiplier:number}{
        const widthTotalOffset = screenWidth - targetWidth;
        const heightTotalOffset = screenHeight - targetHeight;
        return {
            width: widthTotalOffset === 0 ? 0 : widthTotalOffset/2,
            height: heightTotalOffset === 0 ? 0 : heightTotalOffset/2,
            widthMultiplier: targetWidth/dimension,
            heightMultiplier: targetHeight/dimension
        };
    }

    // Transform the position array to an absolute position and scale
    // CardWrapper uses results to position each card
    function positionToAbsolutePosition(coords:[number, number], dimension:number, screenWidth:number, screenHeight:number):{top: number, left:number, scale:number}{
        const [row, column] = coords;
        const [targetWidth, targetHeight] = largest169Box(width, height);
        const offsets = calculateOffsets(screenWidth, screenHeight, targetWidth, targetHeight, dimension);
        return {
            top: (row * offsets.heightMultiplier) + offsets.height,
            left: (column * offsets.widthMultiplier) + offsets.width,
            scale: targetWidth / (dimension * 960)
        };
    }

</script>

<svelte:window bind:innerWidth={width} bind:innerHeight={height}/>

{#each cardArray as card (card.id)}
    <CardWrapper status={card.status} {card} {...positionToAbsolutePosition(card.position, displayDimension, width, height)}></CardWrapper>
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
</style>