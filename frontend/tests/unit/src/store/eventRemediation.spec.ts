import { describe, it, beforeEach, expect, vi } from "vitest";
import { useEventRemediationStore } from "@/stores/eventRemediation";
import { createCustomPinia } from "@tests/unitHelpers";
import { EventRemediation } from "@/services/api/eventRemediation";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useEventRemediationStore();
const spy = vi.spyOn(EventRemediation, "readAll");
const mock = genericObjectReadFactory({ value: "eventRemediation" });

describe("eventRemediation store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call EventRemediation.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(() => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
