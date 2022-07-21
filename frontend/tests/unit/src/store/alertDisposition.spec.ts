import { describe, it, beforeEach, expect, vi } from "vitest";
import { useAlertDispositionStore } from "@/stores/alertDisposition";
import { createCustomPinia } from "@tests/unitHelpers";
import { AlertDisposition } from "@/services/api/alertDisposition";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useAlertDispositionStore();
const spy = vi.spyOn(AlertDisposition, "readAll");
const mock = {
  ...genericObjectReadFactory({ value: "alertDisposition" }),
  rank: 1,
};

describe("alertDisposition store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call AlertDisposition.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(async () => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
