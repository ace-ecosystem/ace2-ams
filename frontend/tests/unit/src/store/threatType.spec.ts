import { describe, it, beforeEach, expect, vi } from "vitest";
import { useThreatTypeStore } from "@/stores/threatType";
import { createCustomPinia } from "@tests/unitHelpers";
import { ThreatType } from "@/services/api/threatType";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useThreatTypeStore();
const spy = vi.spyOn(ThreatType, "readAll");
const mock = {
  ...genericObjectReadFactory({ value: "threattype" }),
  queues: [],
};

describe("threattype store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call ThreatType.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(async () => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
