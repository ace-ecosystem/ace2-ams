import { describe, it, beforeEach, expect, vi } from "vitest";
import { useEventTypeStore } from "@/stores/eventType";
import { createCustomPinia } from "@tests/unitHelpers";
import { EventType } from "@/services/api/eventType";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useEventTypeStore();
const spy = vi.spyOn(EventType, "readAll");
const mock = genericObjectReadFactory({ value: "eventType" });

describe("eventType store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call EventType.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(() => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
