import { describe, it, beforeEach, expect, vi } from "vitest";
import { useAlertToolInstanceStore } from "@/stores/alertToolInstance";
import { createCustomPinia } from "@tests/unitHelpers";
import { AlertToolInstance } from "@/services/api/alertToolInstance";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useAlertToolInstanceStore();
const spy = vi.spyOn(AlertToolInstance, "readAll");
const mock = genericObjectReadFactory({ value: "alertToolInstance" });

describe("alertToolInstance store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call AlertToolInstance.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(async () => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
