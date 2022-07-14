import { describe, it, beforeEach, expect, vi } from "vitest";
import { useEventPreventionToolStore } from "@/stores/eventPreventionTool";
import { createCustomPinia } from "@tests/unitHelpers";
import { EventPreventionTool } from "@/services/api/eventPreventionTool";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useEventPreventionToolStore();
const spy = vi.spyOn(EventPreventionTool, "readAll");
const mock = genericObjectReadFactory({ value: "eventPreventionTool" });

describe("eventPreventionTool store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call EventPreventionTool.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(() => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
