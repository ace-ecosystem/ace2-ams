import { describe, it, beforeEach, expect, vi } from "vitest";
import { useEventPreventionToolStore } from "@/stores/eventPreventionTool";
import { createCustomPinia } from "@tests/unitHelpers";
import { EventPreventionTool } from "@/services/api/eventPreventionTool";

import {
  genericObjectReadFactory,
  queueableObjectReadFactory,
} from "@mocks/genericObject";

createCustomPinia();
const store = useEventPreventionToolStore();
const spy = vi.spyOn(EventPreventionTool, "readAll");
const mockDefaultQueue = genericObjectReadFactory({ value: "defaultQueue" });
const mock = queueableObjectReadFactory({
  value: "eventPreventionTool",
  queues: [mockDefaultQueue],
});

describe("eventPreventionTool store", () => {
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

  it("will call EventPreventionTool.readAll on readAll action and set items and itemsByQueue with the result", async () => {
    spy.mockImplementationOnce(async () => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
    expect(store.itemsByQueue).toEqual({ defaultQueue: [mock] });
  });
});
