// TODO: Move to alertTable store tests
import myNock from "@unit/services/api/nock";
import { alertFilterParams } from "@/models/alert";
import { useAlertTableStore } from "@/stores/alertTable";
import { createCustomPinia } from "@unit/helpers";
import { parseAlertSummary } from "@/etc/helpers";
import {
  alertTreeReadFactory,
  alertSummaryFactory,
  alertReadPageFactory,
} from "@mocks/alert";

import { describe, it, expect, beforeEach } from "vitest";

createCustomPinia();
const store = useAlertTableStore();

const mockAlertTreeReadA = alertTreeReadFactory({ uuid: "uuid1" });
const mockAlertTreeReadB = alertTreeReadFactory({ uuid: "uuid2" });
const mockAlertTreeReadC = alertTreeReadFactory({ uuid: "uuid3" });

const mockAlertReadASummary = alertSummaryFactory({ uuid: "uuid1" });
const mockAlertReadBSummary = alertSummaryFactory({ uuid: "uuid2" });
const mockAlertReadCSummary = alertSummaryFactory({ uuid: "uuid3" });

const mockAlertReadPage = alertReadPageFactory(
  [mockAlertTreeReadA, mockAlertTreeReadB, mockAlertTreeReadC],
  5,
);

const mockParams: alertFilterParams = { limit: 5, offset: 0 };

describe("alertTable helpers", () => {
  it("will correctly parse an alert received from the backend using parseAlertSummary", () => {
    const resA = parseAlertSummary(mockAlertTreeReadA);
    const resB = parseAlertSummary(mockAlertTreeReadC);
    expect(resA).toEqual(mockAlertReadASummary);
    expect(resB).toEqual(mockAlertReadCSummary);
  });
});

describe("alertTable getters", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will correctly return  visibleQueriedItemSummaries", () => {
    store.visibleQueriedItems = [
      mockAlertTreeReadA,
      mockAlertTreeReadB,
      mockAlertTreeReadC,
    ];
    expect(store.visibleQueriedItemSummaries).toEqual([
      mockAlertReadASummary,
      mockAlertReadBSummary,
      mockAlertReadCSummary,
    ]);
  });

  it("will correctly return  visibleQueriedItemsUuids", () => {
    store.visibleQueriedItems = [
      mockAlertTreeReadA,
      mockAlertTreeReadB,
      mockAlertTreeReadC,
    ];
    expect(store.visibleQueriedItemsUuids).toEqual(["uuid1", "uuid2", "uuid3"]);
  });

  it("will correctly return  visibleQueriedItemById", () => {
    store.visibleQueriedItems = [
      mockAlertTreeReadA,
      mockAlertTreeReadB,
      mockAlertTreeReadC,
    ];
    expect(store.visibleQueriedItemById("uuid1")).toEqual(mockAlertTreeReadA);
  });

  it("will correctly return sortFilter", () => {
    expect(store.sortFilter).toEqual("event_time|desc");
  });

  it("will correctly return allFiltersLoaded", () => {
    expect(store.allFiltersLoaded).toBeFalsy();
    store.stateFiltersLoaded = true;
    expect(store.allFiltersLoaded).toBeFalsy();
    store.stateFiltersLoaded = false;
    store.routeFiltersLoaded = true;
    expect(store.allFiltersLoaded).toBeFalsy();
    store.stateFiltersLoaded = true;
    expect(store.allFiltersLoaded).toBeTruthy();
  });
});

describe("alertTable actions", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will request to read page of alerts with given params on readPage", async () => {
    const mockRequest = myNock
      .get("/alert/?limit=5&offset=0")
      .reply(200, mockAlertReadPage);

    await store.readPage(mockParams);

    expect(mockRequest.isDone()).toEqual(true);
    expect(store.visibleQueriedItems).toEqual([
      JSON.parse(JSON.stringify(mockAlertTreeReadA)),
      JSON.parse(JSON.stringify(mockAlertTreeReadB)),
      JSON.parse(JSON.stringify(mockAlertTreeReadC)),
    ]);
    expect(store.totalItems).toEqual(3);
    expect(store.requestReload).toEqual(false);
  });

  it("will throw an error if request fails on readPage", async () => {
    myNock.get("/alert/?limit=5&offset=0").reply(403);

    await expect(store.readPage(mockParams)).rejects.toEqual(
      new Error("Request failed with status code 403"),
    );

    expect(store.visibleQueriedItems).toEqual([]);
    expect(store.totalItems).toEqual(0);
    expect(store.requestReload).toEqual(false);
  });
  it("will reset the sort order and sort field to written defaults on resetSort", () => {
    store.sortField = "exampleSort";
    store.sortOrder = "asc";

    store.resetSort();

    expect(store.sortField).toEqual("eventTime");
    expect(store.sortOrder).toEqual("desc");
  });
});
