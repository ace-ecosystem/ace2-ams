import { describe, it, beforeEach, expect, vi } from "vitest";
import { useEventSourceStore } from "@/stores/eventSource";
import { createCustomPinia } from "@tests/unitHelpers";
import { EventSource } from "@/services/api/eventSource";

import {
  genericObjectReadFactory,
  queueableObjectReadFactory,
} from "@mocks/genericObject";

createCustomPinia();
const store = useEventSourceStore();
const spy = vi.spyOn(EventSource, "readAll");
const mockDefaultQueue = genericObjectReadFactory({ value: "defaultQueue" });
const mock = queueableObjectReadFactory({
  value: "eventSource",
  queues: [mockDefaultQueue],
});
describe("eventSource store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will return items for the given queue on the getItemsByQueue getter, if queue available", () => {
    store.items = [mock];
    store.itemsByQueue = { defaultQueue: [mock] };
    expect(store.getItemsByQueue("defaultQueue")).toEqual([mock]);
  });

  it("will return an empty array for the given queue on the getItemsByQueue getter, if queue not available", () => {
    store.items = [mock];
    store.itemsByQueue = { defaultQueue: [mock] };
    expect(store.getItemsByQueue("otherQueue")).toEqual([]);
  });

  it("will call EventSource.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(() => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
    expect(store.itemsByQueue).toEqual({ defaultQueue: [mock] });
  });
});
