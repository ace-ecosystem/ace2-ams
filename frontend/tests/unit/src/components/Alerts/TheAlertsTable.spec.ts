import TheAlertsTable from "@/components/Alerts/TheAlertsTable.vue";
import { mount, VueWrapper } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import myNock from "@unit/services/api/nock";
import { FilterMatchMode } from "primevue/api";
import { createTestingPinia, TestingOptions } from "@pinia/testing";

import InputText from "primevue/inputtext";
import MultiSelect from "primevue/multiselect";
import Toolbar from "primevue/toolbar";
import DataTable from "primevue/datatable";
import Button from "primevue/button";
import Column from "primevue/column";
import Paginator from "primevue/paginator";
import { alertRead } from "@/models/alert";
import { useFilterStore } from "@/stores/filter";
import { createRouterMock, injectRouterMock } from "vue-router-mock";
import { useSelectedAlertStore } from "@/stores/selectedAlert";

const mockAPIAlert: alertRead = {
  childTags: [],
  childThreatActors: [],
  childThreats: [],
  comments: [],
  description: "",
  disposition: null,
  dispositionTime: null,
  dispositionUser: null,
  eventTime: new Date(0),
  eventUuid: null,
  insertTime: new Date(0),
  instructions: null,
  name: "Test Alert",
  nodeType: "alert",
  owner: null,
  queue: { value: "Default", description: "queue", uuid: "uuid1" },
  tags: [],
  threatActors: [],
  threats: [],
  tool: null,
  toolInstance: null,
  type: { value: "Manual", description: "type", uuid: "uuid1" },
  uuid: "uuid1",
  version: "uuid2",
};

function factory(options?: TestingOptions) {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper: VueWrapper<any> = mount(TheAlertsTable, {
    global: {
      plugins: [createTestingPinia(options), PrimeVue],
    },
  });

  const filterStore = useFilterStore();
  const selectedAlertStore = useSelectedAlertStore();

  return { wrapper, filterStore, selectedAlertStore };
}

// DATA/CREATION
describe("TheAlertsTable data/creation", () => {
  it("renders", async () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });

  it("contains expected components upon creation", () => {
    const { wrapper } = factory();

    expect(wrapper.findComponent(Button).exists()).toBe(true);
    expect(wrapper.findComponent(Column).exists()).toBe(true);
    expect(wrapper.findComponent(DataTable).exists()).toBe(true);
    expect(wrapper.findComponent(InputText).exists()).toBe(true);
    expect(wrapper.findComponent(MultiSelect).exists()).toBe(true);
    expect(wrapper.findComponent(Toolbar).exists()).toBe(true);
    expect(wrapper.findComponent(Paginator).exists()).toBe(true);
  });

  it("initializes data as expected", () => {
    const { wrapper } = factory();

    expect(wrapper.vm.alertTableFilter).toStrictEqual({
      global: { matchMode: "contains", value: null },
    });
    expect(wrapper.vm.selectedColumns).toStrictEqual([
      { field: "eventTime", header: "Event Time" },
      { field: "name", header: "Name" },
      { field: "owner", header: "Owner" },
      { field: "disposition", header: "Disposition" },
    ]);
    expect(wrapper.vm.selectedRows).toStrictEqual([]);
    expect(wrapper.vm.expandedRows).toStrictEqual([]);
    expect(wrapper.vm.columns).toStrictEqual([
      { field: "dispositionTime", header: "Dispositioned Time" },
      { field: "insertTime", header: "Insert Time" },
      { field: "eventTime", header: "Event Time" },
      { field: "name", header: "Name" },
      { field: "owner", header: "Owner" },
      { field: "disposition", header: "Disposition" },
      { field: "dispositionUser", header: "Dispositioned By" },
      { field: "queue", header: "Queue" },
      { field: "type", header: "Type" },
    ]);
    expect(wrapper.vm.defaultColumns).toStrictEqual([
      "eventTime",
      "name",
      "owner",
      "disposition",
    ]);
    expect(wrapper.vm.isLoading).toEqual(true);
    expect(wrapper.vm.error).toBeNull();
    expect(
      wrapper.vm.alertTableStore.visibleQueriedAlertSummaries,
    ).toHaveLength(0);
    expect(wrapper.vm.alertTableStore.totalAlerts).toEqual(0);
    expect(wrapper.vm.sortField).toEqual("eventTime");
    expect(wrapper.vm.sortOrder).toEqual("desc");
    expect(wrapper.vm.numRows).toEqual(10);
    expect(wrapper.vm.page).toEqual(0);
  });

  it("computes computed properties correctly", () => {
    const { wrapper } = factory();

    expect(wrapper.vm.pageOptions).toStrictEqual({
      limit: 10,
      offset: 0,
    });
    expect(wrapper.vm.sortFilter).toEqual("event_time|desc");
    wrapper.vm.sortField = null;
    expect(wrapper.vm.sortFilter).toBeNull();
  });

  it("will fetch an alert's observables and set the sorted array in expandedRowsData on rowExpand", async () => {
    const { wrapper } = factory();

    myNock.post("/node/tree/observable", '["uuid1"]').reply(200, [
      { type: { value: "type_B" }, value: "value_B" },
      { type: { value: "type_A" }, value: "value_A" },
    ]);
    await wrapper.vm.rowExpand("uuid1");
    expect(wrapper.vm.expandedRowsData).toStrictEqual({
      uuid1: [
        { type: { value: "type_A" }, value: "value_A" },
        { type: { value: "type_B" }, value: "value_B" },
      ],
    });
  });

  it("will remove the given property (an alert UUID) from expandedRowsData on rowCollapse", () => {
    const { wrapper } = factory();

    wrapper.vm.expandedRowsData = {
      uuid1: [
        { type: { value: "type_A" }, value: "value_A" },
        { type: { value: "type_B" }, value: "value_B" },
      ],
    };
    wrapper.vm.rowCollapse("uuid1");
    expect(wrapper.vm.expandedRowsData).toStrictEqual({});
  });

  it("will set filters to the given observable and clear expandedRows on filterByObservable", async () => {
    myNock.get("/alert/?sort=event_time%7Cdesc&limit=10&offset=0").reply(200, {
      items: [mockAPIAlert, mockAPIAlert],
      total: 2,
    });
    myNock
      .get(
        "/alert/?sort=event_time%7Cdesc&limit=10&offset=0&observable=type_A%7Cvalue_A",
      )
      .reply(200, {
        items: [],
        total: 0,
      });
    const { wrapper, filterStore } = factory({ stubActions: false });

    wrapper.vm.expandedRows = ["uuid1"];
    wrapper.vm.filterByObservable({
      type: { value: "type_A" },
      value: "value_A",
    });

    expect(wrapper.vm.expandedRows).toEqual([]);
    expect(filterStore.alerts).toStrictEqual({
      observable: { category: { value: "type_A" }, value: "value_A" },
    });
  });

  it("will reset Alert table to defaults upon reset()", async () => {
    const { wrapper } = factory();

    wrapper.vm.alertTableFilter = [];
    wrapper.vm.selectedColumns = [];
    wrapper.vm.reset();
    expect(wrapper.vm.selectedColumns).toStrictEqual([
      { field: "eventTime", header: "Event Time" },
      { field: "name", header: "Name" },
      { field: "owner", header: "Owner" },
      { field: "disposition", header: "Disposition" },
    ]);
    expect(wrapper.vm.alertTableFilter).toStrictEqual({
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    });
  });

  it("will init Alert table to defaults upon initAlertTable()", async () => {
    const { wrapper } = factory();

    wrapper.vm.alertTableFilter = [];
    wrapper.vm.initAlertTable();
    expect(wrapper.vm.alertTableFilter).toStrictEqual({
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    });
  });
  // Skip this test for now since the CSV export needs to be reworked & this test currently gives a warning
  it.skip("will export the alerts table to CSV on exportCSV", async () => {
    const { wrapper } = factory();

    // we cant actually export the CSV in test so mock one of the dependency functions
    window.URL.createObjectURL = jest.fn().mockReturnValueOnce("fakeURL");
    wrapper.vm.exportCSV();
  });

  it("will correctly set selectedColumns when onColumnToggle", async () => {
    const { wrapper } = factory();

    expect(wrapper.vm.selectedColumns).toStrictEqual([
      { field: "eventTime", header: "Event Time" },
      { field: "name", header: "Name" },
      { field: "owner", header: "Owner" },
      { field: "disposition", header: "Disposition" },
    ]);
    await wrapper.vm.onColumnToggle([wrapper.vm.columns[0]]);
    expect(wrapper.vm.selectedColumns).toStrictEqual([
      { field: "dispositionTime", header: "Dispositioned Time" },
    ]);
  });
  it("will reload the alerts with new pagination settings on 'onPage'", async () => {
    myNock.get("/alert/?sort=event_time%7Cdesc&limit=10&offset=0").reply(200, {
      items: [mockAPIAlert, mockAPIAlert],
      total: 2,
    });
    const { wrapper } = factory({ stubActions: false });

    const mockRequest = myNock
      .get("/alert/?sort=event_time%7Cdesc&limit=1&offset=1")
      .reply(200, {
        items: [mockAPIAlert],
        total: 2,
      });
    await wrapper.vm.onPage({ rows: 1, page: 1 });
    expect(wrapper.vm.numRows).toEqual(1);
    expect(wrapper.vm.selectedRows).toEqual([]);
    expect(mockRequest.isDone()).toEqual(true);
  });
  it("will reload the alerts with new sort settings on 'sort'", async () => {
    myNock.get("/alert/?sort=event_time%7Cdesc&limit=10&offset=0").reply(200, {
      items: [mockAPIAlert, mockAPIAlert],
      total: 2,
    });
    const { wrapper } = factory({ stubActions: false });

    const mockRequestSort = myNock
      .get("/alert/?sort=name%7Casc&limit=10&offset=0")
      .reply(200, {
        items: [mockAPIAlert],
        total: 2,
      });
    await wrapper.vm.sort({ sortField: "name", sortOrder: 1 });
    expect(wrapper.vm.sortField).toEqual("name");
    expect(wrapper.vm.sortOrder).toEqual("asc");
    expect(mockRequestSort.isDone()).toEqual(true);
  });
  it("will reset sort settings if sort called without sortField", async () => {
    const { wrapper } = factory();

    await wrapper.vm.sort({});
    expect(wrapper.vm.sortField).toBeNull();
    expect(wrapper.vm.sortOrder).toBeNull();
  });
  it("will reload and clear selected alerts, and clear requestReload on reloadTable", async () => {
    myNock
      .get("/alert/?sort=event_time%7Cdesc&limit=10&offset=0")
      .twice()
      .reply(200, {
        items: [mockAPIAlert, mockAPIAlert],
        total: 2,
      });
    const { wrapper, selectedAlertStore } = factory({ stubActions: false });

    selectedAlertStore.selected = ["uuid1", "uuid2", "uuid3"];
    wrapper.vm.alertTableStore.requestReload = true;
    await wrapper.vm.reloadTable();
    expect(wrapper.vm.selectedRows).toEqual([]);
    expect(wrapper.vm.selectedAlertStore.selected).toEqual([]);
    expect(wrapper.vm.alertTableStore.requestReload).toBeFalsy();
  });

  it("will set the error data property to the given error if getAllAlerts fails within loadAlerts", async () => {
    myNock.get("/alert/?sort=event_time%7Cdesc&limit=10&offset=0").reply(200, {
      items: [mockAPIAlert, mockAPIAlert],
      total: 2,
    });
    const { wrapper } = factory({ stubActions: false });

    const mockRequest = myNock
      .get("/alert/?sort=event_time%7Cdesc&limit=10&offset=0")
      .reply(403, "Request Failed");

    expect(wrapper.vm.error).toBeNull();
    await wrapper.vm.loadAlerts();
    expect(mockRequest.isDone()).toEqual(true);
    expect(wrapper.vm.error).toEqual("Request failed with status code 403");
  });
});
