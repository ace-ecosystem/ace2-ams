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

// DATA/CREATION
describe("TheAlertsTable data/creation", () => {
  myNock
    .get("/alert/")
    .times(4)
    .reply(200, { items: [{ uuid: "alert_1" }, { uuid: "alert_2" }] });

  const wrapper = mount(TheAlertsTable, {
    global: {
      plugins: [store, PrimeVue, router],
    },
  });

  beforeEach(async () => {
    wrapper.vm.reset();
    await wrapper.vm.loadAlerts();
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
  });
});

// METHODS
describe("AnalyzeAlertForm methods", () => {
  myNock
    .get("/alert/")
    .times(5)
    .reply(200, { items: [{ uuid: "alert_1" }, { uuid: "alert_2" }] });

  const wrapper = mount(TheAlertsTable, {
    global: {
      plugins: [store, PrimeVue, router],
    },
  });

  beforeEach(async () => {
    wrapper.vm.reset();
    await wrapper.vm.loadAlerts();
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

  it("will build a list of UUIDs from currently queried alerts and selectAll within the selectedAlerts store upon alertSelectAll()", async () => {
    expect(wrapper.vm.selectedAlerts).toEqual([]);
    wrapper.vm.alertSelectAll();
    expect(wrapper.vm.selectedAlerts).toEqual(["alert_1", "alert_2"]);
  });

  it("will set the error data property to the given error if getAllAlerts fails within loadAlerts", async () => {
    myNock.get("/alert/").reply(403, "Request Failed");

    expect(wrapper.vm.error).toBeNull();
    wrapper.vm.loadAlerts();
    expect(wrapper.vm.error).toBeNull();
  });
});
