import { describe, it, beforeEach, expect, vi } from "vitest";
import { useEventRemediationStore } from "@/stores/eventRemediation";
import { createCustomPinia } from "@tests/unitHelpers";
import { EventRemediation } from "@/services/api/eventRemediation";

import {
  genericObjectReadFactory,
  queueableObjectReadFactory,
} from "@mocks/genericObject";

createCustomPinia();
const store = useEventRemediationStore();
const spy = vi.spyOn(EventRemediation, "readAll");
const mockDefaultQueue = genericObjectReadFactory({ value: "defaultQueue" });
const mock = queueableObjectReadFactory({
  value: "eventRemediation",
  queues: [mockDefaultQueue],
});

describe("eventRemediation store", () => {
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

  it("will call EventRemediation.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(() => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
    expect(store.itemsByQueue).toEqual({ defaultQueue: [mock] });
  });
});
