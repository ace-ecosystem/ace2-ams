import { describe, it, beforeEach, expect, vi } from "vitest";
import { useThreatStore } from "@/stores/threat";
import { createCustomPinia } from "@tests/unitHelpers";
import { Threat } from "@/services/api/threat";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useThreatStore();
const spy = vi.spyOn(Threat, "readAll");
const mock = genericObjectReadFactory({ value: "threat" });

describe("threat store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call Threat.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(() => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
