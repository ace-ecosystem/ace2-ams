import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";
import { testConfiguration } from "@/etc/configuration/test/index";

import TheNodeTable from "@/components/Node/TheNodeTable.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { Alert } from "@/services/api/alert";
import { alertReadFactory } from "@mocks/alert";
import { userReadFactory } from "@mocks/user";
import { genericObjectReadFactory } from "@mocks/genericObject";
import ToastService from "primevue/toastservice";

interface column {
  required: boolean;
  default: boolean;
  field: string;
  header: string;
  sortable: boolean;
}
interface TheNodeTableProps {
  columns: column[];
  columnSelect?: boolean;
  exportCSV?: boolean;
  keywordSearch?: boolean;
  resetTable?: boolean;
  rowExpansion?: boolean;
}

const defaultColumns = [
  {
    field: "name",
    header: "Name",
    sortable: true,
    default: true,
    required: false,
  },
  {
    field: "owner",
    header: "Owner",
    sortable: true,
    default: true,
    required: false,
  },
];

const defaultProps: TheNodeTableProps = {
  columns: defaultColumns,
};

function factory(props: TheNodeTableProps = defaultProps) {
  return mount(TheNodeTable, {
    global: {
      plugins: [
        PrimeVue,
        ToastService,
        createCustomCypressPinia({
          stubActions: false,
          initialState: {
            currentUserSettingsStore: {
              queues: {
                alerts: genericObjectReadFactory({ value: "external" }),
                events: null,
              },
            },
          },
        }),
      ],
      provide: {
        nodeType: "alerts",
        availableFilters: testConfiguration.alerts.alertFilters,
      },
    },
    propsData: props,
  });
}

const bigPage = [
  alertReadFactory({ uuid: "3", name: "Alert C" }),
  alertReadFactory({ uuid: "3", name: "Alert C" }),
  alertReadFactory({ uuid: "3", name: "Alert C" }),
  alertReadFactory({ uuid: "3", name: "Alert C" }),
  alertReadFactory({ uuid: "3", name: "Alert C" }),
  alertReadFactory({ uuid: "3", name: "Alert C" }),
  alertReadFactory({ uuid: "3", name: "Alert C" }),
  alertReadFactory({ uuid: "3", name: "Alert C" }),
  alertReadFactory({ uuid: "3", name: "Alert C" }),
  alertReadFactory({ uuid: "3", name: "Alert C" }),
  alertReadFactory({ uuid: "3", name: "Alert C" }),
];

describe("TheNodeTable", () => {
  it("renders empty with default props", () => {
    cy.stub(Alert, "readPage")
      .withArgs({
        sort: "event_time|desc",
        limit: 10,
        offset: 0,
      })
      .as("readPage")
      .resolves({
        items: [],
        limit: 10,
        offset: 0,
        total: 0,
      });
    factory();
    cy.contains("Name, Owner").should("be.visible");
    cy.findByPlaceholderText("Search in table").should("be.visible");
    cy.get('[data-cy="reset-table-button"]').should("be.visible");
    cy.get('[data-cy="export-table-button"]').should("be.visible");
    cy.findByRole("table").should("be.visible");
    cy.contains("No alerts found.").should("be.visible");
  });
  it("renders empty with all optional props disabled", () => {
    cy.stub(Alert, "readPage").resolves({
      items: [alertReadFactory({ uuid: "2", name: "Alert B" })],
      limit: 10,
      offset: 0,
      total: 1,
    });
    factory({
      columns: defaultColumns,
      columnSelect: false,
      exportCSV: false,
      keywordSearch: false,
      resetTable: false,
      rowExpansion: false,
    });
    cy.contains("Name, Owner").should("not.exist");
    cy.findByPlaceholderText("Search in table").should("not.exist");
    cy.get('[data-cy="reset-table-button"]').should("not.exist");
    cy.get('[data-cy="export-table-button"]').should("not.exist");
    cy.get(".p-row-toggler-icon").should("not.exist");
  });
  it("displays error if data cannot be fetched", () => {
    cy.stub(Alert, "readPage")
      .withArgs({
        sort: "event_time|desc",
        limit: 10,
        offset: 0,
      })
      .as("readPage")
      .rejects(new Error("404 Request failed"));
    factory();
    cy.findByRole("table").should("be.visible");
    cy.contains("No alerts found.").should("be.visible");
    cy.contains("Failed to fetch alerts").should("be.visible");
    cy.contains("404 Request failed").should("be.visible");
  });
  it("renders when there is node data available", () => {
    const columnHeaders = ["", "", "Name", "Owner"];
    const rows = [
      "",
      "",
      "Alert A",
      "Test Analyst",
      "",
      "",
      "Alert B",
      "None",
      "",
      "",
      "Alert C",
      "None",
    ];

    cy.stub(Alert, "readPage")
      .withArgs({
        sort: "event_time|desc",
        limit: 10,
        offset: 0,
      })
      .as("readPage")
      .resolves({
        items: [
          alertReadFactory({
            uuid: "1",
            name: "Alert A",
            owner: userReadFactory(),
          }),
          alertReadFactory({ uuid: "2", name: "Alert B" }),
          alertReadFactory({ uuid: "3", name: "Alert C" }),
        ],
        limit: 10,
        offset: 0,
        total: 3,
      });
    factory();

    cy.get("tr").should("have.length", 4);
    cy.get("th").each(($el, index) => {
      cy.wrap($el).should("contain.text", columnHeaders[index]);
    });

    cy.get(".p-row-toggler-icon").should("have.length", 3);
    cy.get(" .p-checkbox-box").should("have.length", 4);
    cy.get("td").each(($el, index) => {
      cy.wrap($el).should("contain.text", rows[index]);
    });
  });
  it("will make call when sort is changed", () => {
    const stub = cy.stub(Alert, "readPage");
    stub
      .withArgs({
        sort: "event_time|desc",
        limit: 10,
        offset: 0,
      })
      .as("defaultReadPage")
      .resolves({
        items: [alertReadFactory({ uuid: "2", name: "Alert B" })],
        limit: 10,
        offset: 0,
        total: 1,
      });
    stub
      .withArgs({
        sort: "name|asc",
        limit: 10,
        offset: 0,
      })
      .as("nameAscReadPage")
      .resolves({
        items: [alertReadFactory({ uuid: "2", name: "Alert B" })],
        limit: 10,
        offset: 0,
        total: 1,
      });
    stub
      .withArgs({
        sort: "name|desc",
        limit: 10,
        offset: 0,
      })
      .as("nameDescReadPage")
      .resolves({
        items: [alertReadFactory({ uuid: "2", name: "Alert B" })],
        limit: 10,
        offset: 0,
        total: 1,
      });
    factory();
    cy.get("@defaultReadPage").should("have.been.calledOnce");
    cy.findAllByText("Name").click();
    cy.get("@nameAscReadPage").should("have.been.calledOnce");
    cy.findAllByText("Name").click();
    cy.get("@nameDescReadPage").should("have.been.calledOnce");

    // No sort is set now, so no need to make any additional calls
    cy.findAllByText("Name").click();
    cy.get("@defaultReadPage").should("have.been.calledOnce");
    cy.get("@nameAscReadPage").should("have.been.calledOnce");
    cy.get("@nameDescReadPage").should("have.been.calledOnce");
  });
  it("will update selected store when selected changes", () => {
    const stub = cy.stub(Alert, "readPage");
    stub
      .withArgs({
        sort: "event_time|desc",
        limit: 10,
        offset: 0,
      })
      .as("defaultReadPage")
      .resolves({
        items: [alertReadFactory({ uuid: "2", name: "Alert B" })],
        limit: 10,
        offset: 0,
        total: 1,
      });
    factory();
    cy.get(" .p-checkbox ").first().click();
    cy.get("@spy-5").should("have.been.calledOnceWith", ["2"]); // selectAll
    cy.get(" .p-checkbox ").first().click();
    cy.get("@spy-7").should("have.been.calledOnce"); // unselectAll
    cy.get(" .p-checkbox ").last().click();
    cy.get("@spy-4").should("have.been.calledOnceWith", "2"); // select (single)
    cy.get(" .p-checkbox ").last().click();
    cy.get("@spy-6").should("have.been.calledOnceWith", "2"); // de-select (single)
  });
  it("will reset as expected", () => {
    const stub = cy.stub(Alert, "readPage");
    stub
      .withArgs({
        sort: "event_time|desc",
        limit: 10,
        offset: 0,
      })
      .as("defaultReadPage")
      .resolves({
        items: [alertReadFactory({ uuid: "2", name: "Alert B" })],
        limit: 10,
        offset: 0,
        total: 1,
      });
    stub
      .withArgs({
        sort: "name|asc",
        limit: 10,
        offset: 0,
      })
      .as("nameAscReadPage")
      .resolves({
        items: [alertReadFactory({ uuid: "2", name: "Alert B" })],
        limit: 10,
        offset: 0,
        total: 1,
      });
    factory();
    cy.get("@defaultReadPage").should("have.been.calledOnce");

    // change sort
    cy.findAllByText("Name").click();
    // change columns showing
    cy.contains("Name, Owner").click();
    cy.get('[aria-label="Name"]').click();
    cy.get('[aria-label="Owner"]').click();
    cy.get(".p-multiselect-close-icon").click();
    cy.contains("Name").should("not.exist");
    cy.contains("Owner").should("not.exist");
    cy.get('[data-cy="reset-table-button"]').click();
    // Call with default sort should be made again
    cy.get("@defaultReadPage").should("have.been.calledTwice");
    cy.contains("Name, Owner").should("be.visible"); // columns will be back to default
  });
  // Come back to this once we update CSV export
  // it("will export to csv as expected", () => {
  //   const stub = cy.stub(Alert, "readPage");
  //   stub
  //     .withArgs({
  //       sort: "event_time|desc",
  //       limit: 10,
  //       offset: 0,
  //     })
  //     .as("defaultReadPage")
  //     .resolves({
  //       items: [alertReadFactory({ uuid: "2", name: "Alert B" })],
  //       limit: 10,
  //       offset: 0,
  //       total: 1,
  //     });
  //   factory();
  //   cy.get('[data-cy="export-table-button"]').click();
  // });
  it("will expand row as expected", () => {
    const stub = cy.stub(Alert, "readPage");
    stub
      .withArgs({
        sort: "event_time|desc",
        limit: 10,
        offset: 0,
      })
      .as("defaultReadPage")
      .resolves({
        items: [alertReadFactory({ uuid: "2", name: "Alert B" })],
        limit: 10,
        offset: 0,
        total: 1,
      });
    factory();
    cy.get(".p-row-toggler-icon").click();
    cy.contains("No content provided").should("be.visible");
    cy.get(".p-row-toggler-icon").click();
    cy.contains("No content provided").should("not.exist");
  });
  it("will make call to fetch new page and update currently selected when page is changed", () => {
    const stub = cy.stub(Alert, "readPage");
    stub
      .withArgs({
        sort: "event_time|desc",
        limit: 10,
        offset: 0,
      })
      .as("defaultReadPage")
      .resolves({
        items: bigPage,
        limit: 10,
        offset: 0,
        total: 11,
      });
    stub
      .withArgs({
        sort: "event_time|desc",
        limit: 10,
        offset: 10,
      })
      .as("nextPageDefaultReadPage")
      .resolves({
        items: [alertReadFactory({ uuid: "2", name: "Alert B" })],
        limit: 10,
        offset: 10,
        total: 11,
      });
    factory();
    cy.get("@defaultReadPage").should("have.been.calledOnce");
    cy.contains("Showing 1 to 10 of 11").should("be.visible");
    cy.get(".p-paginator-next").click();
    cy.get("@spy-7").should("have.been.called"); // unselectAll
    cy.get("@nextPageDefaultReadPage").should("have.been.calledOnce");
    cy.contains("Showing 11 to 11 of 11").should("be.visible");
  });
  it("will initialize columns as expected", () => {
    const stub = cy.stub(Alert, "readPage");
    stub
      .withArgs({
        sort: "event_time|desc",
        limit: 10,
        offset: 0,
      })
      .as("defaultReadPage")
      .resolves({
        items: [alertReadFactory({ uuid: "2", name: "Alert B" })],
        limit: 10,
        offset: 0,
        total: 1,
      });
    factory({
      columns: [
        ...defaultColumns,
        {
          field: "Required",
          header: "Required&CantSort",
          sortable: false,
          default: false,
          required: true,
        },
        {
          field: "notDefaultOrReq",
          header: "notDefaultOrReq",
          sortable: false,
          default: false,
          required: false,
        },
      ],
    });
    // Required column should be shown, but is not an option in col select
    cy.get("th").should("have.length", 5);
    cy.contains("Required&CantSort").should("be.visible");
    cy.contains("Name, Owner").should("be.visible");
    // Not required, not default column will not be shown, but is an option in col select
    cy.contains("Name, Owner").click();
    cy.get("[aria-label").should("have.length", 3); // only 3 column options
    cy.get('[aria-label="Name"]').should("be.visible");
    cy.get('[aria-label="Owner"]').should("be.visible");
    cy.get('[aria-label="notDefaultOrReq"]').should("be.visible").click();
    cy.get("th").should("have.length", 6);
  });
  it("will add filter on click if a column is filterable", () => {
    const stub = cy.stub(Alert, "readPage");
    stub
      .withArgs({
        sort: "event_time|desc",
        limit: 10,
        offset: 0,
      })
      .as("defaultReadPage")
      .resolves({
        items: [
          alertReadFactory({
            uuid: "2",
            name: "Alert B",
            owner: userReadFactory(),
          }),
        ],
        limit: 10,
        offset: 0,
        total: 1,
      });
    factory();
    // Name field is not in the list of available filters, so nothing should happen when clicked
    cy.contains("Alert B").click();
    cy.get("@spy-12").should("not.have.been.called");
    // Owner field is one of the available filters, so a filter should be added when an 'Owner' column cell is clicked
    cy.contains("Test Analyst").click();
    cy.get("@spy-12").should("have.been.calledOnceWith", {
      nodeType: "alerts",
      filterName: "owner",
      filterValue: userReadFactory(),
    });
  });
});
