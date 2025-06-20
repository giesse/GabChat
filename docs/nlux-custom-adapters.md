# Create Custom Adapters

If you're building your APIs and you would like to use `NLUX` as the UI for your own AI chatbot, you can do so by creating a custom adapter.

An adapter is a component that connects `NLUX` an API. It receives messages from `NLUX` and sends them to the API. It also receives responses from the API and sends them to `NLUX` in a format that can be displayed in the chat UI.

## Creating a Custom Adapter

There are 2 types of custom adapters that you can create:

*   Streaming Adapters — To stream generated responses in chunks.
*   Batch Adapters — To receive the response in a single request.

---

## Streaming Adapters

Streaming adapters are used when the API sends responses in a stream (e.g. WebSockets, or Server-Sent Events).

The advantage of using a streaming adapter is that **the chat UI will be updated in real-time while the LLM is still generating text**. This is particularly useful if the API takes a long time to process a request and sends responses in a stream. Most major LLM APIs (e.g. OpenAI, Anthropic) support streaming responses.

To implement a custom streaming adapter for `NLUX`, you need to implement the following interface:

```typescript
interface ChatAdapter {
    streamText: (
        message: string,
        observer: StreamingAdapterObserver,
        extras: AdapterExtras,
    ) => void;
}
```

> **Note**
> If you're using the React version of `NLUX`, you can use the `useStreamingAdapter` hook to create a streaming adapter as shown below:
>
> ```typescript
> const adapter: ChatAdapter = useStreamingAdapter(streamText, []);
> ```
>
> Which wraps the `streamText` method in a simple object and offers memoization parameters.

The `streamText` method takes 2 parameters:

*   `message` - The prompt message typed by the user, to be sent to the API.
*   `observer` - An observer that will receive the responses from the API and pass them to `NLUX`.

Below is the definition of the `StreamingAdapterObserver` interface:

```typescript
interface StreamingAdapterObserver {
    next: (partialResponse: string) => void;
    error: (error: Error) => void;
    complete: () => void;
}
```

You can call the `next` method of the observer as responses are received from the API. The `complete` method should be called when the API has finished sending responses, and The `error` method should be called if an error occurs.

### Example: Streaming Adapter

Let's say we want to create an adapter for a custom API that sends responses in a stream.
This eventual API has a WebSocket endpoint that can be used to send messages and receive responses.

We can create a streaming adapter for this API by implementing the `ChatAdapter` interface's `streamText` method as follows:

```typescript
import {ChatAdapter, StreamingAdapterObserver} from '@nlux/core';

export const myCustomAdapter: ChatAdapter = {
    streamText: (message: string, observer: StreamingAdapterObserver): void => {
        const socket = new WebSocket('ws://localhost:8080');
        
        // We register listeners for the WebSocket events here
        // and call the observer methods accordingly
        socket.onmessage = (event) => observer.next(event.data);
        socket.onclose = () => observer.complete();
        socket.onerror = (error) => observer.error(error);
        
        // This is where we send the user message to the API
        socket.send(message);
    }
}
```

Streaming adapters can also be used with APIs that send responses as Server-Sent Events (SSE). [All the examples on this website](/nlux/examples/react-js-ai-assistant) use this approach.

Another potentially useful configuration is `messageOptions.waitTimeBeforeStreamCompletion`, which sets the wait time in milliseconds after the last data chunk; the default value is 2000ms.

## Batch Adapters

Batch adapters can be used when the API sends responses in a single request (e.g. REST APIs).

The advantage of using a batch adapter is that **they are easier to implement**.

To implement a custom batch adapter for `NLUX`, you need to implement the following interface:

```typescript
interface ChatAdapter {
    batchText(message: string, extras: AdapterExtras): Promise<string>;
}
```

> **Note**
> If you're using the React version of `NLUX`, you can use the `useAsBatchAdapter` hook to create a streaming adapter as shown below:
>
> ```typescript
> const adapter: ChatAdapter = useStreamingAdapter(batchText, []);
> ```
>
> This wraps the `batchText` in a `ChatAdapter` object and offers memoization parameters.

The `batchText` method takes 2 parameters:

*   `message` - The prompt message typed by the user, to be sent to the API.
*   `extras` - An object containing additional information that the adapter might need.

The `batchText` method should return a promise that resolves to the response from the API.

### Example: Batch Adapter

Let's say we want to create a batch adapter for a custom API that sends responses in a single request.

The API has a REST endpoint that we can use to send messages and receive responses.

We can create a batch adapter for this API by implementing the `PromiseAdapter` interface:

```typescript
import {useAsBatchAdapter, AdapterExtras} from '@nlux/react';

export const myCustomAdapter = useAsBatchAdapter(
    (message: string, extras: AdapterExtras): Promise<string> => {
        return fetch('http://localhost:8080', {
            method: 'POST',
            body: JSON.stringify({message})
        })
            .then(response => response.json())
            .then(json => json.message);
    }
);
```

## Using Custom Adapters

Once you have created a custom adapter, you can use it to create a chat component and render it in the DOM:

The same custom adapter can be used with the React and JavaScript versions of `NLUX`.

### Example: Using a Custom Adapter

**React JS ⚛️**
```tsx
import {AiChat, useAsBatchAdapter} from '@nlux/react';

const App = () => {
    const myCustomAdapter = useAsBatchAdapter(
        async (prompts: string[]) => {
            // Submit the prompt and get the response ...
        }
    );

    return <AiChat adapter={myCustomAdapter} />;
}
```

**JavaScript 🟨**
```tsx
import {createAiChat} from '@nlux/core';

const aiChat = createAiChat().withAdapter(myCustomAdapter);
const root = document.getElementById('root-element');

aiChat.mount(root);
```

You can refer to the Getting Started guides for [React](/nlux/learn/get-started?platform=react-js) and [JavaScript](/nlux/learn/get-started?platform=javascript) for more details on how to use `NLUX`.
