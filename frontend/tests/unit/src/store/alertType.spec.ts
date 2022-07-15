import { describe, it, beforeEach, expect, vi } from "vitest";
import { useAlertTypeStore } from "@/stores/alertType";
import { createCustomPinia } from "@tests/unitHelpers";
import { AlertType } from "@/services/api/alertType";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useAlertTypeStore();
const spy = vi.spyOn(AlertType, "readAll");
const mock = genericObjectReadFactory({ value: "alertType" });

describe("alertType store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call AlertType.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(async () => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
