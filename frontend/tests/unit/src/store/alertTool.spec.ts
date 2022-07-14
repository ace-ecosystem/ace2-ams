import { describe, it, beforeEach, expect, vi } from "vitest";
import { useAlertToolStore } from "@/stores/alertTool";
import { createCustomPinia } from "@tests/unitHelpers";
import { AlertTool } from "@/services/api/alertTool";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useAlertToolStore();
const spy = vi.spyOn(AlertTool, "readAll");
const mock = genericObjectReadFactory({ value: "alertTool" });

describe("alertTool store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call AlertTool.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(() => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
