import { describe, it, beforeEach, expect, vi } from "vitest";
import { useMetadataDirectiveStore } from "@/stores/metadataDirective";
import { createCustomPinia } from "@tests/unitHelpers";
import { MetadataDirective } from "@/services/api/metadataDirective";

import { genericObjectReadFactory } from "@mocks/genericObject";

createCustomPinia();
const store = useMetadataDirectiveStore();
const spy = vi.spyOn(MetadataDirective, "readAll");
const mock = genericObjectReadFactory({ value: "metadataDirective" });

describe("metadataDirective store", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will call MetadataDirective.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(() => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
  });
});
