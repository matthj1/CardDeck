<script lang="ts">
    import CornerBox from "../ui_components/CornerBox.svelte";
</script>

<CornerBox error={true}>
    <h1>AUTHENTICATION ERROR</h1>
    <h2>One or more endpoints returned 403: Permission Denied. Check API token.</h2>
</CornerBox>

<style>
    h1{
        font-size: 50px;
    }
    h2{
        font-size: 35px;
    }
</style>