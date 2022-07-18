import { describe, it, beforeEach, expect, vi } from "vitest";
import { useQueueStore } from "@/stores/queue";
import { createCustomPinia } from "@tests/unitHelpers";
import { queue } from "@/services/api/queue";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useQueueStore();
const spy = vi.spyOn(queue, "readAll");
const mock = genericObjectReadFactory({ value: "queue" });

describe("queue store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call Queue.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(async () => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
