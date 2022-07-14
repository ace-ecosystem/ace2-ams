import { describe, it, beforeEach, expect, vi } from "vitest";
import { useEventStatusStore } from "@/stores/eventStatus";
import { createCustomPinia } from "@tests/unitHelpers";
import { EventStatus } from "@/services/api/eventStatus";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useEventStatusStore();
const spy = vi.spyOn(EventStatus, "readAll");
const mock = genericObjectReadFactory({ value: "eventStatus" });

describe("eventStatus store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call EventStatus.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(() => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
