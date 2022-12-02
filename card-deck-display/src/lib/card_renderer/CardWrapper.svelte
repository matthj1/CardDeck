<script lang="ts">
    import {StatusChoices } from "../../interfaces";
    import type {ICardItem} from "../../interfaces";

    export let card: ICardItem;
    export let top:number;
    export let left:number;
    export let scale:number;
    export let status: StatusChoices;

</script>

<div class="absolute-fixed-size"
class:stale={status === StatusChoices.STALE}
class:error={status === StatusChoices.ERROR}
class:warning={status === StatusChoices.WARNING}
style="top: {top}px; left: {left}px; transform: scale({scale};">

    <div class="glow"
    class:error-glow={status === StatusChoices.ERROR}
    class:normal-glow={status === StatusChoices.RUNNING || status === StatusChoices.STALE}
    class:warning-glow={status === StatusChoices.WARNING}>

        <svelte:component this={card.component} {...card.props}/>
    </div>

</div>

<style>
    .absolute-fixed-size {
        position: absolute;
        width: 960px;
        height: 540px;
        padding: 0;
        border: 1px solid rgb(31, 34, 34);
        transform-origin: 0 0;
        transition: top 2000ms, left 2000ms, transform 2000ms;
        opacity: 0;
        animation: delay-appearance 2000ms;
        animation-fill-mode: forwards;
    }
    .glow{
        width: 100%;
        height: 100%;
    }

    .error-glow{
        animation: error-glow 2000ms 2000ms;
    }
    .normal-glow{
        animation: glow 2000ms 2000ms;
    }

    .warning-glow{
        animation: warning-glow 2000ms 2000ms;
    }

    @keyframes delay-appearance {
        99% {opacity: 0;}
        100% {opacity: 1;}
    }

    .stale{
        filter: saturate(0);
    }

    .error{
        border: 2px solid #752720;
    }

    .warning{
        border: 2px solid #664219;
    }

    @keyframes glow{
        0%{
            box-shadow: 0px 0px 120px var(--running-glow);
        }
        100%{
            box-shadow: 0px 0px 0px var(--running-glow);
        }
    }

    @keyframes error-glow{
        0%{
            box-shadow: 0px 0px 120px var(--error-primary);
        }
        100%{
            box-shadow: 0px 0px 0px var(--error-primary);
        }
    }

    @keyframes warning-glow{
        0%{
            box-shadow: 0px 0px 120px var(--warning-primary);
        }
        100%{
            box-shadow: 0px 0px 0px var(--warning-primary);
        }
    }

</style>