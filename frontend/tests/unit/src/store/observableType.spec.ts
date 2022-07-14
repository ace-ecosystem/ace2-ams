import { describe, it, beforeEach, expect, vi } from "vitest";
import { useObservableTypeStore } from "@/stores/observableType";
import { createCustomPinia } from "@tests/unitHelpers";
import { ObservableType } from "@/services/api/observableType";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useObservableTypeStore();
const spy = vi.spyOn(ObservableType, "readAll");
const mock = genericObjectReadFactory({ value: "observableType" });

describe("observableType store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call ObservableType.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(() => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
