import { describe, it, beforeEach, expect, vi } from "vitest";
import { useEventSourceStore } from "@/stores/eventSource";
import { createCustomPinia } from "@tests/unitHelpers";
import { EventSource } from "@/services/api/eventSource";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useEventSourceStore();
const spy = vi.spyOn(EventSource, "readAll");
const mock = genericObjectReadFactory({ value: "eventSource" });

describe("eventSource store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call EventSource.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(() => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
