import { describe, it, beforeEach, expect, vi } from "vitest";
import { useEventVectorStore } from "@/stores/eventVector";
import { createCustomPinia } from "@tests/unitHelpers";
import { EventVector } from "@/services/api/eventVector";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useEventVectorStore();
const spy = vi.spyOn(EventVector, "readAll");
const mock = genericObjectReadFactory({ value: "eventVector" });

describe("eventVector store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call EventVector.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(() => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
