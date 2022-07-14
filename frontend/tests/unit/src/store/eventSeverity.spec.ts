import { describe, it, beforeEach, expect, vi } from "vitest";
import { useEventSeverityStore } from "@/stores/eventSeverity";
import { createCustomPinia } from "@tests/unitHelpers";
import { EventSeverity } from "@/services/api/eventSeverity";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useEventSeverityStore();
const spy = vi.spyOn(EventSeverity, "readAll");
const mock = genericObjectReadFactory({ value: "eventSeverity" });

describe("eventSeverity store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call EventSeverity.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(() => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
