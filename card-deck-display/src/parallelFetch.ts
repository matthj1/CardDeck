import {StatusChoices} from "./interfaces"
import type {IParrallelFetchData, IInputData} from "./interfaces"

let cache = {};

export async function parallelFetch<Type>(sources:{url: string, options?: RequestInit}[]):Promise<IParrallelFetchData<Type>[]>{
    let output = [];
    const responses = await Promise.allSettled(
        sources.map(source => fetchTimeout(source.url, source.options).then(async res => {
            if(res.status === 200){
                return {url: source.url, status: 200, data: await res.json()};
            }
            else if(res.status === 403){
                return {url: source.url, status: 403, data: []};
            }
            else{
                throw new Error("Not 2XX status code");
            }
        }))
    );
    for(const [index, response] of responses.entries()){
        if(response.status === "fulfilled"){
            // add to output and cache result
            output = [...output, response.value];
            cache[response.value.url] = response.value;
        }
        else{
            // use cached result if any, set status to stale
            if(sources[index].url in cache){
                const cachedData = cache[sources[index].url].data as IInputData[];
                const chachedWithStatus = cachedData.map(sd => {return {...sd, status: StatusChoices.STALE}});
                const obj = {url: sources[index].url, status: undefined, data: chachedWithStatus};
                output = [...output, obj]
            }
        }
    }
    return output as IParrallelFetchData<Type>[]
}


async function fetchTimeout(url:string, options?:RequestInit, timeout:number = 2000){

    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);
    const response = await fetch(url, {
      ...options,
      signal: controller.signal
    });
    clearTimeout(id);
    return response;
}
