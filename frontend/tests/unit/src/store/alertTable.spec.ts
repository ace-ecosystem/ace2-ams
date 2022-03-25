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
    expect(resA).to.eql(mockAlertReadASummary);
    expect(resB).to.eql(mockAlertReadCSummary);
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
    expect(store.visibleQueriedItemSummaries).to.eql([
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
    expect(store.visibleQueriedItemsUuids).to.eql(["uuid1", "uuid2", "uuid3"]);
  });

  it("will correctly return  visibleQueriedItemById", () => {
    store.visibleQueriedItems = [
      mockAlertTreeReadA,
      mockAlertTreeReadB,
      mockAlertTreeReadC,
    ];
    expect(store.visibleQueriedItemById("uuid1")).to.eql(mockAlertTreeReadA);
  });

  it("will correctly return sortFilter", () => {
    expect(store.sortFilter).to.eql("event_time|desc");
  });

  it("will correctly return allFiltersLoaded", () => {
    expect(store.allFiltersLoaded).to.equal(false);
    store.stateFiltersLoaded = true;
    expect(store.allFiltersLoaded).to.equal(false);
    store.stateFiltersLoaded = false;
    store.routeFiltersLoaded = true;
    expect(store.allFiltersLoaded).to.equal(false);
    store.stateFiltersLoaded = true;
    expect(store.allFiltersLoaded).to.equal(true);
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

    expect(mockRequest.isDone()).to.eql(true);
    expect(store.visibleQueriedItems).to.eql([
      JSON.parse(JSON.stringify(mockAlertTreeReadA)),
      JSON.parse(JSON.stringify(mockAlertTreeReadB)),
      JSON.parse(JSON.stringify(mockAlertTreeReadC)),
    ]);
    expect(store.totalItems).to.eql(3);
    expect(store.requestReload).to.eql(false);
  });

  it("will throw an error if request fails on readPage", async () => {
    myNock.get("/alert/?limit=5&offset=0").reply(403);

    try {
      await store.readPage(mockParams);
    } catch (e) {
      const error = e as Error;
      expect(error.message).to.equal("Request failed with status code 403");
    }

    expect(store.visibleQueriedItems).to.eql([]);
    expect(store.totalItems).to.eql(0);
    expect(store.requestReload).to.eql(false);
  });
  it("will reset the sort order and sort field to written defaults on resetSort", () => {
    store.sortField = "exampleSort";
    store.sortOrder = "asc";

    store.resetSort();

    expect(store.sortField).to.eql("eventTime");
    expect(store.sortOrder).to.eql("desc");
  });
});
