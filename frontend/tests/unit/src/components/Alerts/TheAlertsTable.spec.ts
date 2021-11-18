import TheAlertsTable from "@/components/Alerts/TheAlertsTable.vue";
import { mount } from "@vue/test-utils";
import store from "@/store";
import PrimeVue from "primevue/config";
import myNock from "@unit/services/api/nock";
import router from "@/router";
import { FilterMatchMode } from "primevue/api";

import InputText from "primevue/inputtext";
import MultiSelect from "primevue/multiselect";
import Toolbar from "primevue/toolbar";
import DataTable from "primevue/datatable";
import Button from "primevue/button";
import Column from "primevue/column";
import Paginator from "primevue/paginator";
import nock from "nock";

// DATA/CREATION
describe("TheAlertsTable data/creation", () => {
  const wrapper = mount(TheAlertsTable, {
    global: {
      plugins: [store, PrimeVue, router],
    },
  });

  beforeAll(async () => {
    nock.cleanAll();
    myNock
      .get("/alert/?limit=10&offset=0")
      .reply(200, {
        items: [{ uuid: "alert_1" }, { uuid: "alert_2" }],
        total: 2,
      })
      .persist();
  });

  beforeEach(async () => {
    wrapper.vm.reset();
    await wrapper.vm.loadAlerts();
  });

  afterAll(() => {
    nock.cleanAll();
  });

  it("renders", async () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("contains expected components upon creation", async () => {
    expect(wrapper.findComponent(Button).exists()).toBe(true);
    expect(wrapper.findComponent(Column).exists()).toBe(true);
    expect(wrapper.findComponent(DataTable).exists()).toBe(true);
    expect(wrapper.findComponent(InputText).exists()).toBe(true);
    expect(wrapper.findComponent(MultiSelect).exists()).toBe(true);
    expect(wrapper.findComponent(Toolbar).exists()).toBe(true);
    expect(wrapper.findComponent(Paginator).exists()).toBe(true);
  });

  it("initializes data as expected", async () => {
    expect(wrapper.vm.alertTableFilter).toStrictEqual({
      global: { matchMode: "contains", value: null },
    });
    expect(wrapper.vm.selectedColumns).toStrictEqual([
      { field: "eventTime", header: "Event Date" },
      { field: "name", header: "Name" },
      { field: "owner", header: "Owner" },
      { field: "disposition", header: "Disposition" },
    ]);
    expect(wrapper.vm.selectedRows).toBeNull();
    expect(wrapper.vm.expandedRows).toStrictEqual([]);
    expect(wrapper.vm.columns).toStrictEqual([
      { field: "dispositionTime", header: "Dispositioned Time" },
      { field: "insertTime", header: "Insert Date" },
      { field: "eventTime", header: "Event Date" },
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
    expect(wrapper.vm.isLoading).toEqual(false);
    expect(wrapper.vm.error).toBeNull();
    expect(wrapper.vm.alerts).toHaveLength(2);
    expect(wrapper.vm.totalAlerts).toEqual(2);
    expect(wrapper.vm.numRows).toEqual(10);
    expect(wrapper.vm.page).toEqual(0);
  });
  it("computes computed properties correctly", async () => {
    expect(wrapper.vm.pageOptions).toStrictEqual({
      limit: 10,
      offset: 0,
    });
  });
});

// METHODS (SUCCESS)
describe("TheAlertsTable methods success", () => {
  const wrapper = mount(TheAlertsTable, {
    global: {
      plugins: [store, PrimeVue, router],
    },
  });

  beforeAll(async () => {
    nock.cleanAll();
    myNock
      .get("/alert/?limit=10&offset=0")
      .reply(200, {
        items: [{ uuid: "alert_1" }, { uuid: "alert_2" }],
        total: 2,
      })
      .persist();
  });

  beforeEach(async () => {
    wrapper.vm.reset();
    await wrapper.vm.loadAlerts();
  });

  afterAll(() => {
    nock.cleanAll();
  });

  it("will reset Alert table to defaults upon reset()", async () => {
    wrapper.setData({
      alertTableFilter: [],
      selectedColumns: [],
    });
    wrapper.vm.reset();
    expect(wrapper.vm.selectedColumns).toStrictEqual([
      { field: "eventTime", header: "Event Date" },
      { field: "name", header: "Name" },
      { field: "owner", header: "Owner" },
      { field: "disposition", header: "Disposition" },
    ]);
    expect(wrapper.vm.alertTableFilter).toStrictEqual({
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    });
  });

  it("will init Alert table to defaults upon initAlertTable()", async () => {
    wrapper.setData({
      alertTableFilter: [],
    });
    wrapper.vm.initAlertTable();
    expect(wrapper.vm.alertTableFilter).toStrictEqual({
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    });
  });
  it("will reload the alerts with new pagination settings on 'onPage'", async () => {
    const mockRequest = myNock
      .get("/alert/?limit=1&offset=1")
      .thrice()
      .reply(200, {
        items: [{ uuid: "alert_2" }],
        total: 2,
      });
    await wrapper.vm.onPage({ rows: 1, page: 1 });
    expect(wrapper.vm.numRows).toEqual(1);
    expect(wrapper.vm.selectedRows).toEqual([]);
    expect(mockRequest.isDone()).toEqual(true);
  });
});

// METHODS (FAILED)
describe("TheAlertsTable methods failed", () => {
  const wrapper = mount(TheAlertsTable, {
    global: {
      plugins: [store, PrimeVue, router],
    },
  });

  beforeAll(async () => {
    nock.cleanAll();
  });

  afterAll(() => {
    nock.cleanAll();
  });

  it("will set the error data property to the given error if getAllAlerts fails within loadAlerts", async () => {
    const mockRequest = myNock
      .get("/alert/?limit=10&offset=0")
      .twice()
      .reply(403, "Request Failed");

    expect(wrapper.vm.error).toBeNull();
    await wrapper.vm.loadAlerts();
    expect(mockRequest.isDone()).toEqual(true);
    expect(wrapper.vm.error).toEqual("Request failed with status code 403");
  });
});
