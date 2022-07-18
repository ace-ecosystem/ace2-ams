import { describe, it, beforeEach, expect, vi } from "vitest";
import { useThreatStore } from "@/stores/threat";
import { createCustomPinia } from "@tests/unitHelpers";
import { Threat } from "@/services/api/threat";

import {
  genericObjectReadFactory,
  queueableObjectReadFactory,
  genericObjectCreateFactory,
} from "@mocks/genericObject";

createCustomPinia();
const store = useThreatStore();
const spy = vi.spyOn(Threat, "readAll");
const createSpy = vi.spyOn(Threat, "create");
const updateSpy = vi.spyOn(Threat, "update");
const mockDefaultQueue = genericObjectReadFactory({ value: "defaultQueue" });
const mock = {
  ...queueableObjectReadFactory({
    value: "threat",
    queues: [mockDefaultQueue],
  }),
  types: [],
};

describe("threat store", () => {
  beforeEach(() => {
    store.$reset();
    spy.mockReset();
    createSpy.mockReset();
    updateSpy.mockReset();
  });

  it("will return state.items on the allItems getter", () => {
    expect(store.allItems).toEqual([]);
    store.items = [mock];
    expect(store.allItems).toEqual([mock]);
  });

  it("will return items for the given queue on the getItemsByQueue getter, if queue available", () => {
    store.items = [mock];
    store.itemsByQueue = { defaultQueue: [mock] };
    expect(store.getItemsByQueue("defaultQueue")).toEqual([mock]);
  });

  it("will return an empty array for the given queue on the getItemsByQueue getter, if queue not available", () => {
    store.items = [mock];
    store.itemsByQueue = { defaultQueue: [mock] };
    expect(store.getItemsByQueue("otherQueue")).toEqual([]);
  });

  it("will call Threat.create and Threat.readAll on create action and set items with the updated results", async () => {
    createSpy.mockImplementationOnce(async () => undefined);
    spy.mockImplementationOnce(async () => [mock]);
    await store.create({
      ...genericObjectCreateFactory({ value: "threat" }),
      types: [],
      queues: [],
    });
    expect(createSpy).toHaveBeenCalledTimes(1);
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
    expect(store.itemsByQueue).toEqual({ defaultQueue: [mock] });
  });

  it("will throw error if create action fails", async () => {
    createSpy.mockImplementationOnce(async () => {
      throw new Error("Error");
    });
    try {
      await store.create({
        ...genericObjectCreateFactory({ value: "threat" }),
        types: [],
        queues: [],
      });
    } catch (e) {
      const error = e as Error;
      expect(error.message).toEqual("Error");
    }
  });

  it("will call Threat.update and Threat.readAll on create action and set items with the updated results", async () => {
    updateSpy.mockImplementationOnce(async () => undefined);
    spy.mockImplementationOnce(async () => [mock]);
    await store.update("uuid", { value: "threat", types: [] });
    expect(updateSpy).toHaveBeenCalledTimes(1);
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
    expect(store.itemsByQueue).toEqual({ defaultQueue: [mock] });
  });

  it("will throw error if update action fails", async () => {
    updateSpy.mockImplementationOnce(async () => {
      throw new Error("Error");
    });
    try {
      await store.update("uuid", { value: "threat", types: [] });
    } catch (e) {
      const error = e as Error;
      expect(error.message).toEqual("Error");
    }
  });

  it("will call Threat.readAll on readAll action and set items with the result", async () => {
    spy.mockImplementationOnce(async () => [mock]);
    await store.readAll();
    expect(spy).toHaveBeenCalledTimes(1);
    expect(store.items).toEqual([mock]);
    expect(store.itemsByQueue).toEqual({ defaultQueue: [mock] });
  });
});
