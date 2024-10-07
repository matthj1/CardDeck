import TransferCard from "./TransferCard.svelte";
import { render, screen } from "@testing-library/svelte";
import { expect, test } from "vitest";
import { ITransferProps, QueryStatus, StatusChoices } from "../../interfaces";

const dataExamples: ITransferProps[] = [
        {
            id: "a",
            status: StatusChoices.RUNNING,
            type: "PACS_TRANSFER",
            query_id: "a",
            hospital: "Test Hospital",
            gateway: "a",
            gateway_id: 1,
            query_status: QueryStatus.QUEUED,
            response: {},
            elapsed: "00:00:01",
            started: "22:04GMT",
            transfer_type: "RETRIEVE_STUDY",
        },
        {
            id: "a",
            status: StatusChoices.ERROR,
            type: "PACS_TRANSFER",
            query_id: "a",
            hospital: "Test Hospital",
            gateway: "a",
            gateway_id: 1,
            query_status: QueryStatus.ERROR,
            response: {
                name: "Generic Error",
                message: "Something went wrong"
            },
            elapsed: "00:00:01",
            started: "22:04GMT",
            transfer_type: "RETRIEVE_STUDY",
        },
]

test("PACS transfer message is displayed on progress bar and status", ()=>{
    render(TransferCard, {props: {item: dataExamples[0]}})

    const messages = screen.queryAllByText("Waiting in the queue");

    expect(messages.length).toBe(2);
});

test("Header text correct with running status", ()=>{
    render(TransferCard, {props: {item: dataExamples[0]}})
    
    const headerText = screen.queryByText("RETRIEVING STUDY");

    expect(headerText).not.toBe(null);
});

test("Header text correct with error status", ()=>{
    render(TransferCard, {props: {item: dataExamples[1]}})
    
    const headerText = screen.queryByText("ERROR RETRIEVING STUDY");

    expect(headerText).not.toBe(null);
});

test("Error name is shown with error status", ()=>{
    render(TransferCard, {props: {item: dataExamples[1]}})
    
    const errorName = screen.queryByText("Generic Error");

    expect(errorName).not.toBe(null);
});

test("Error message is shown with error status", ()=>{
    render(TransferCard, {props: {item: dataExamples[1]}})
    
    const errorMessage = screen.queryByText("Something went wrong");

    expect(errorMessage).not.toBe(null);
});
