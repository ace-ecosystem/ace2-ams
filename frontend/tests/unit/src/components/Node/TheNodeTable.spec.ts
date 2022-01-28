import { mount, VueWrapper } from "@vue/test-utils";
import myNock from "@unit/services/api/nock";
import { FilterMatchMode } from "primevue/api";
import { TestingOptions } from "@pinia/testing";

import InputText from "primevue/inputtext";
import MultiSelect from "primevue/multiselect";
import Toolbar from "primevue/toolbar";
import DataTable from "primevue/datatable";
import Button from "primevue/button";
import Column from "primevue/column";
import Paginator from "primevue/paginator";
import { useFilterStore } from "@/stores/filter";
import { createRouterMock, injectRouterMock } from "vue-router-mock";
import { useSelectedAlertStore } from "@/stores/selectedAlert";
import TheNodeTableVue from "@/components/Node/TheNodeTable.vue";
import { useAlertTableStore } from "@/stores/alertTable";
import { mockAlert } from "../../../../mockData/alert";
import { createCustomPinia } from "@unit/helpers";

const mockAlertReadA = Object.assign({}, mockAlert, { uuid: "uuid1" });
const mockAlertReadB = Object.assign({}, mockAlert, { uuid: "uuid2" });

interface factoryOptions {
  piniaOptions?: TestingOptions;
  props?: {
    columns: Record<string, any>[];
    columnSelect?: boolean;
    exportCSV?: boolean;
    keywordSearch?: boolean;
    resetTable?: boolean;
    rowExpansion?: boolean;
  };
  nodeType?: string;
}

const columns = [
  { field: "test", header: "Test", default: false },
  { field: "otherTest", header: "Other Test", default: true },
];

function factory(
  options: factoryOptions = {
    piniaOptions: undefined,
    props: { columns: columns },
    nodeType: "alerts",
  },
) {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper: VueWrapper<any> = mount(TheNodeTableVue, {
    global: {
      plugins: [createCustomPinia(options.piniaOptions)],
      provide: {
        nodeType: options.nodeType,
      },
    },
    props: options.props,
  });

  const filterStore = useFilterStore();
  const alertTableStore = useAlertTableStore();
  const selectedAlertStore = useSelectedAlertStore();

  return { wrapper, alertTableStore, filterStore, selectedAlertStore };
}

// DATA/CREATION
describe("TheNodeTable data/creation", () => {
  it("renders", () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });

  it("contains expected components upon creation when all bool props are true", () => {
    const { wrapper } = factory();

    expect(wrapper.findComponent(Button).exists()).toBe(true);
    expect(wrapper.findComponent(Column).exists()).toBe(true);
    expect(wrapper.findComponent(DataTable).exists()).toBe(true);
    expect(wrapper.findComponent(InputText).exists()).toBe(true);
    expect(wrapper.findComponent(MultiSelect).exists()).toBe(true);
    expect(wrapper.findComponent(Toolbar).exists()).toBe(true);
    expect(wrapper.findComponent(Paginator).exists()).toBe(true);
  });

  it("contains expected components upon creation when all bool props are false", () => {
    const { wrapper } = factory({
      piniaOptions: undefined,
      props: {
        columns: columns,
        columnSelect: false,
        exportCSV: false,
        keywordSearch: false,
        resetTable: false,
        rowExpansion: false,
      },
      nodeType: "alerts",
    });

    expect(wrapper.findComponent(Column).exists()).toBe(true);
    expect(wrapper.findComponent(DataTable).exists()).toBe(true);
    expect(wrapper.findComponent(Paginator).exists()).toBe(true);
  });

  it("initializes data as expected", async () => {
    const { wrapper } = factory();
    await wrapper.vm.$nextTick();

    expect(wrapper.vm.nodeTableFilter).toStrictEqual({
      global: { matchMode: "contains", value: null },
    });
    expect(wrapper.vm.selectedColumns).toStrictEqual([
      { field: "otherTest", header: "Other Test", default: true },
    ]);
    expect(wrapper.vm.expandedRows).toStrictEqual([]);
    expect(wrapper.vm.columns).toStrictEqual(columns);
    expect(wrapper.vm.defaultColumns).toStrictEqual([columns[1]]);
    expect(wrapper.vm.isLoading).toEqual(false);
    expect(wrapper.vm.error).toBeNull();
    expect(wrapper.vm.tableStore.visibleQueriedItemSummaries).toHaveLength(0);
    expect(wrapper.vm.tableStore.totalItems).toEqual(0);
    expect(wrapper.vm.page).toEqual(0);
  });
  it("initializes tableToolbarRequired as expected when all bool props are true", () => {
    const { wrapper } = factory();

    expect(wrapper.vm.tableToolbarRequired).toBeTruthy();
  });

  it("initializes tableToolbarRequired as expected when all bool props are false", () => {
    const { wrapper } = factory({
      piniaOptions: undefined,
      props: {
        columns: columns,
        columnSelect: false,
        exportCSV: false,
        keywordSearch: false,
        resetTable: false,
        rowExpansion: false,
      },
      nodeType: "alerts",
    });

    expect(wrapper.vm.tableToolbarRequired).toBeFalsy();
  });

  it("will execute loadNodes when filterStore is changed (filterStore subscription)", async () => {
    const { wrapper, filterStore } = factory();
    // Read once on load
    expect(wrapper.vm.tableStore.readPage).toHaveBeenCalledTimes(1);

    filterStore.alerts = {
      test: "test",
    };

    await wrapper.vm.$nextTick();
    expect(wrapper.vm.tableStore.readPage).toHaveBeenCalledTimes(2);
  });

  it("will execute loadNodes when tableStore requestReload is set to true (tableStore subscription)", async () => {
    const { wrapper, alertTableStore } = factory();
    // Read once on load
    expect(wrapper.vm.tableStore.readPage).toHaveBeenCalledTimes(1);

    alertTableStore.requestReload = true;

    await wrapper.vm.$nextTick();
    expect(wrapper.vm.tableStore.readPage).toHaveBeenCalledTimes(2);
  });

  it("computes selectedRows correctly", () => {
    const { wrapper, selectedAlertStore, alertTableStore } = factory();

    expect(wrapper.vm.selectedRows).toEqual([]);

    selectedAlertStore.selected = ["uuid1"];
    alertTableStore.visibleQueriedItems = [mockAlertReadA, mockAlertReadB];

    expect(wrapper.vm.selectedRows).toEqual([mockAlertReadA]);
  });

  it("computes sortOrder correctly", () => {
    const { wrapper, alertTableStore } = factory();

    expect(wrapper.vm.sortOrder).toEqual(-1);

    alertTableStore.sortOrder = "asc";
    expect(wrapper.vm.sortOrder).toEqual(1);

    alertTableStore.sortOrder = null;
    expect(wrapper.vm.sortOrder).toEqual(0);
  });

  it("computes pageOptions correctly", () => {
    const { wrapper, alertTableStore } = factory();

    expect(wrapper.vm.pageOptions).toStrictEqual({
      limit: 10,
      offset: 0,
    });

    wrapper.vm.page = 2;

    expect(wrapper.vm.pageOptions).toStrictEqual({
      limit: 10,
      offset: 20,
    });

    alertTableStore.pageSize = 5;

    expect(wrapper.vm.pageOptions).toStrictEqual({
      limit: 5,
      offset: 10,
    });
  });

  // Skip this test for now since the CSV export needs to be reworked & this test currently gives a warning
  it.skip("will export the alerts table to CSV on exportCSV", async () => {
    const { wrapper } = factory();

    // we cant actually export the CSV in test so mock one of the dependency functions
    window.URL.createObjectURL = vi.fn().mockReturnValueOnce("fakeURL");
    wrapper.vm.exportCSV();
  });

  it("will init table to defaults upon initNodeTable()", async () => {
    const { wrapper } = factory();

    wrapper.vm.nodeTableFilter = [];
    wrapper.vm.selectedColumns = [];
    wrapper.vm.error = "test error";

    wrapper.vm.initNodeTable();
    expect(wrapper.vm.nodeTableFilter).toStrictEqual({
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    });
    expect(wrapper.vm.selectedColumns).toEqual([
      {
        field: "otherTest",
        header: "Other Test",
        default: true,
      },
    ]);
    expect(wrapper.vm.error).toBeNull();
  });

  it("will correctly set selectedColumns when onColumnToggle", async () => {
    const { wrapper } = factory();

    wrapper.vm.selectedColumns = columns;
    await wrapper.vm.onColumnToggle([wrapper.vm.columns[0]]);
    expect(wrapper.vm.selectedColumns).toStrictEqual([columns[0]]);
  });

  it("will reload and clear selected nodes, and clear requestReload on reloadTable", async () => {
    myNock
      .get("/alert/?sort=event_time%7Cdesc&limit=10&offset=0")
      .twice()
      .reply(200, {
        items: [mockAlertReadA, mockAlertReadB],
        total: 2,
      });
    const { wrapper, selectedAlertStore } = factory({
      piniaOptions: { stubActions: false },
      props: { columns: columns },
      nodeType: "alerts",
    });

    selectedAlertStore.selected = ["uuid2"];
    wrapper.vm.tableStore.requestReload = true;
    await wrapper.vm.reloadTable();
    expect(wrapper.vm.selectedRows).toEqual([]);
    expect(wrapper.vm.selectedStore.selected).toEqual([]);
    expect(wrapper.vm.tableStore.requestReload).toBeFalsy();
  });

  it("will set the error data property to the given error if readPage fails within loadNodes", async () => {
    myNock.get("/alert/?sort=event_time%7Cdesc&limit=10&offset=0").reply(200, {
      items: [mockAlertReadA, mockAlertReadB],
      total: 2,
    });
    const { wrapper } = factory({
      piniaOptions: { stubActions: false },
      props: { columns: columns },
      nodeType: "alerts",
    });

    const mockRequest = myNock
      .get("/alert/?sort=event_time%7Cdesc&limit=10&offset=0")
      .reply(403, "Request Failed");

    expect(wrapper.vm.error).toBeNull();
    await wrapper.vm.loadNodes();
    expect(mockRequest.isDone()).toEqual(true);
    expect(wrapper.vm.error).toEqual("Request failed with status code 403");
  });

  it("will reload nodes with new pagination settings on 'onPage'", async () => {
    myNock.get("/alert/?sort=event_time%7Cdesc&limit=10&offset=0").reply(200, {
      items: [mockAlertReadA, mockAlertReadB],
      total: 2,
    });
    const { wrapper } = factory({
      piniaOptions: { stubActions: false },
      props: { columns: columns },
      nodeType: "alerts",
    });

    const mockRequest = myNock
      .get("/alert/?sort=event_time%7Cdesc&limit=1&offset=1")
      .reply(200, {
        items: [mockAlertReadA],
        total: 2,
      });
    await wrapper.vm.onPage({ rows: 1, page: 1 });
    expect(wrapper.vm.selectedRows).toEqual([]);
    expect(mockRequest.isDone()).toEqual(true);
  });

  it("will reset table to defaults upon reset()", () => {
    const { wrapper } = factory();

    wrapper.vm.nodeTableFilter = [];
    wrapper.vm.selectedColumns = [];
    wrapper.vm.error = "test error";

    wrapper.vm.reset();
    expect(wrapper.vm.selectedColumns).toStrictEqual([columns[1]]);
    expect(wrapper.vm.error).toBeNull();
    expect(wrapper.vm.nodeTableFilter).toStrictEqual({
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
    });
    expect(wrapper.vm.tableStore.readPage).toHaveBeenCalled();
    expect(wrapper.vm.tableStore.resetSort).toHaveBeenCalled();
  });
  it("will reload the alerts with new sort settings on 'sort'", async () => {
    const { wrapper } = factory();

    wrapper.vm.sort({ sortField: "name", sortOrder: 1 });
    expect(wrapper.vm.tableStore.sortField).toEqual("name");
    expect(wrapper.vm.tableStore.sortOrder).toEqual("asc");
    expect(wrapper.vm.tableStore.readPage).toHaveBeenNthCalledWith(2, {
      limit: 10,
      offset: 0,
      sort: "name|asc",
    });
  });
  it("will reset tablerStore sort settings if sort called without sortField", async () => {
    const { wrapper } = factory();

    await wrapper.vm.sort({});
    expect(wrapper.vm.tableStore.sortField).toBeNull();
    expect(wrapper.vm.tableStore.sortOrder).toBeNull();
  });
});
