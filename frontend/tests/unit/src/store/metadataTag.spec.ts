import { describe, it, beforeEach, expect, vi } from "vitest";
import { useMetadataTagStore } from "@/stores/metadataTag";
import { createCustomPinia } from "@tests/unitHelpers";
import { MetadataTag } from "@/services/api/metadataTag";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useMetadataTagStore();
const spy = vi.spyOn(MetadataTag, "readAll");
const mock = genericObjectReadFactory({ value: "metadataTag" });

describe("metadataTag store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call MetadataTag.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(() => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
