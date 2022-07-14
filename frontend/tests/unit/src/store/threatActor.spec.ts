import { describe, it, beforeEach, expect, vi } from "vitest";
import { useThreatActorStore } from "@/stores/threatActor";
import { createCustomPinia } from "@tests/unitHelpers";
import { ThreatActor } from "@/services/api/threatActor";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useThreatActorStore();
const spy = vi.spyOn(ThreatActor, "readAll");
const mock = genericObjectReadFactory({ value: "threatactor" });

describe("threatactor store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call ThreatActor.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(() => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
