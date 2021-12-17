import ViewAlert from "../../../../../src/pages/Alerts/ViewAlert.vue";
import { mount, VueWrapper } from "@vue/test-utils";
import { createTestingPinia, TestingOptions } from "@pinia/testing";
// import { getRouter, createRouterMock, injectRouterMock } from "vue-router-mock";
import { useAlertStore } from "@/stores/alert";
import { useSelectedAlertStore } from "@/stores/selectedAlert";
import { observableTreeRead } from "@/models/observable";
import { alertRead } from "@/models/alert";
import { analysisTreeRead } from "@/models/analysis";
import myNock from "@unit/services/api/nock";
import { createRouterMock, getRouter, injectRouterMock } from "vue-router-mock";
import router from "@/router";

const mockAlert = {
  directives: [],
  tags: [],
  threatActor: null,
  threats: [],
  version: "2e1b021f-e169-41a3-836c-3b30db5e237d",
  description: null,
  eventTime: new Date("2021-12-15T19:21:50.964478+00:00"),
  insertTime: new Date("2021-12-15T19:21:50.964480+00:00"),
  instructions: null,
  queue: {
    description: null,
    value: "test_queue",
    uuid: "67106bea-5541-4855-a72a-ae62336a6088",
  },
  owner: {
    defaultAlertQueue: {
      description: null,
      value: "test_queue",
      uuid: "67106bea-5541-4855-a72a-ae62336a6088",
    },
    displayName: "Analyst",
    email: "bob@bob.com",
    enabled: true,
    roles: [
      {
        description: null,
        value: "test_role",
        uuid: "03eaa38e-e44c-412b-b8f4-eeb8ea06d2ce",
      },
    ],
    timezone: "UTC",
    username: "bob",
    uuid: "4223ba76-c61b-4877-b3cc-174de2e6be46",
  },
  comments: [],
  parentTreeUuid: null,
  treeUuid: null,
  uuid: "02f8299b-2a24-400f-9751-7dd9164daf6a",
  disposition: null,
  dispositionTime: null,
  dispositionUser: {
    defaultAlertQueue: {
      description: null,
      value: "test_queue",
      uuid: "67106bea-5541-4855-a72a-ae62336a6088",
    },
    displayName: "Analyst",
    email: "alice@alice.com",
    enabled: true,
    roles: [
      {
        description: null,
        value: "test_role",
        uuid: "03eaa38e-e44c-412b-b8f4-eeb8ea06d2ce",
      },
    ],
    timezone: "UTC",
    username: "alice",
    uuid: "d3fe20c4-9173-4e81-8bb5-69e95c1b8dad",
  },
  eventUuid: null,
  name: "Small Alert",
  tool: {
    description: null,
    value: "test_tool",
    uuid: "2c9c0dac-f405-4c8e-8e90-7fd298b1c693",
  },
  toolInstance: {
    description: null,
    value: "test_tool_instance",
    uuid: "25c724eb-fc42-4f15-b9c3-71b9ad452a04",
  },
  type: {
    description: null,
    value: "test_type",
    uuid: "37592ad0-c3f6-4fcb-8fba-2fe09b042721",
  },
};

const mockTree: (analysisTreeRead | observableTreeRead)[] = [
  {
    directives: [],
    tags: [],
    threatActor: null,
    threats: [],
    version: "d0c4cc36-5794-4cb1-bf24-715e6219811d",
    context: null,
    expiresOn: null,
    forDetection: false,
    redirectionUuid: null,
    time: new Date("2021-12-15T19:21:51.345360+00:00"),
    type: {
      description: null,
      value: "file",
      uuid: "7a58e9a0-f9ab-4e25-8c81-030ddb50e1ad",
    },
    value: "email.rfc822",
    comments: [],
    parentTreeUuid: null,
    treeUuid: "ba9b3b3b-9904-43f7-812d-d187532b4d31",
    uuid: "187aa0e8-ed53-4226-bbbd-91bb17792182",
  },
  {
    analysisModuleType: {
      value: "Email Analysis",
      uuid: "86d1b2ae-e309-447e-ba0c-0eec348c1040",
    },
    parentTreeUuid: "ba9b3b3b-9904-43f7-812d-d187532b4d31",
    treeUuid: "baa866a3-d704-4429-bb09-05a8fb83cf23",
    uuid: "a48452c8-4bdc-4d16-821e-9159657d3ae7",
  },
  {
    directives: [],
    tags: [
      {
        description: null,
        value: "from_address",
        uuid: "b39d762d-5654-458c-8b20-cf0d3bad0f03",
      },
    ],
    threatActor: null,
    threats: [],
    version: "ebf52897-b3a3-4b43-9c1c-5c002b0dcb91",
    context: null,
    expiresOn: null,
    forDetection: false,
    redirectionUuid: null,
    time: new Date("2021-12-15T19:21:51.395163+00:00"),
    type: {
      description: null,
      value: "email_address",
      uuid: "dabfc053-e442-4897-b565-b22dc72c5a67",
    },
    value: "badguy@evil.com",
    comments: [],
    parentTreeUuid: "baa866a3-d704-4429-bb09-05a8fb83cf23",
    treeUuid: "970a09d8-2c97-4315-84be-7687b06dd2bc",
    uuid: "b742e1b0-b000-4807-b768-7c05ec5df61f",
  },
  {
    analysisModuleType: {
      value: "Email Address Analysis",
      uuid: "850fdbd4-455e-41c1-89d9-106bfe0fa733",
    },
    parentTreeUuid: "970a09d8-2c97-4315-84be-7687b06dd2bc",
    treeUuid: "5d8cb617-5732-42ff-92ee-c0529e3c51f7",
    uuid: "e44c898e-20a3-4719-9044-438ae3f9dc0d",
  },
  {
    directives: [],
    tags: [],
    threatActor: null,
    threats: [],
    version: "289a65cc-7ca9-48ca-8e48-27104802631f",
    context: null,
    expiresOn: null,
    forDetection: false,
    redirectionUuid: null,
    time: new Date("2021-12-15T19:21:51.423600+00:00"),
    type: {
      description: null,
      value: "fqdn",
      uuid: "91441637-523b-4609-81f8-da161b68e3eb",
    },
    value: "evil.com",
    comments: [],
    parentTreeUuid: "5d8cb617-5732-42ff-92ee-c0529e3c51f7",
    treeUuid: "892ac598-e564-43c7-a42a-30ad3018e186",
    uuid: "a88dfca9-9849-446a-92ba-d2e6fb8308d9",
  },
  {
    directives: [],
    tags: [
      {
        description: null,
        value: "recipient",
        uuid: "ce7a4e31-1eda-43bb-b95a-6eac0b943e4d",
      },
    ],
    threatActor: null,
    threats: [],
    version: "fade33a5-73d7-46d0-85d1-42ca16e73de5",
    context: null,
    expiresOn: null,
    forDetection: false,
    redirectionUuid: null,
    time: new Date("2021-12-15T19:21:51.434847+00:00"),
    type: {
      description: null,
      value: "email_address",
      uuid: "dabfc053-e442-4897-b565-b22dc72c5a67",
    },
    value: "goodguy@company.com",
    comments: [],
    parentTreeUuid: "baa866a3-d704-4429-bb09-05a8fb83cf23",
    treeUuid: "908bda99-b50e-4691-a533-af3ca1464c63",
    uuid: "0aa9ed7e-1e9c-43df-9185-c79d14cdc22e",
  },
  {
    analysisModuleType: {
      value: "Email Address Analysis",
      uuid: "850fdbd4-455e-41c1-89d9-106bfe0fa733",
    },
    parentTreeUuid: "908bda99-b50e-4691-a533-af3ca1464c63",
    treeUuid: "eee49cd0-d2e5-49b5-891a-a22435095210",
    uuid: "e41ae1ae-4d50-42a1-a38b-1c9936ed9c18",
  },
  {
    directives: [],
    tags: [],
    threatActor: null,
    threats: [],
    version: "c10b23c7-88a3-435a-b8b3-068141b59682",
    context: null,
    expiresOn: null,
    forDetection: false,
    redirectionUuid: null,
    time: new Date("2021-12-15T19:21:51.455080+00:00"),
    type: {
      description: null,
      value: "fqdn",
      uuid: "91441637-523b-4609-81f8-da161b68e3eb",
    },
    value: "company.com",
    comments: [],
    parentTreeUuid: "eee49cd0-d2e5-49b5-891a-a22435095210",
    treeUuid: "f4cbaef5-659f-46e3-a7c9-be46f6b50ae0",
    uuid: "ce45125a-6364-46c4-8d25-bee57644f723",
  },
  {
    directives: [],
    tags: [],
    threatActor: null,
    threats: [],
    version: "93f7471d-b377-4b3c-86e0-479b1a9cc52f",
    context: null,
    expiresOn: null,
    forDetection: false,
    redirectionUuid: null,
    time: new Date("2021-12-15T19:21:51.464006+00:00"),
    type: {
      description: null,
      value: "email_subject",
      uuid: "3d090e5f-0541-42c7-996b-ad3b184b5c36",
    },
    value: "Hello",
    comments: [],
    parentTreeUuid: "baa866a3-d704-4429-bb09-05a8fb83cf23",
    treeUuid: "a1d4fd8f-08b1-460d-aaec-df1afd59f915",
    uuid: "a7efeab7-a633-414f-987d-a91ccd7044d7",
  },
  {
    directives: [],
    tags: [],
    threatActor: null,
    threats: [],
    version: "d0c2fd3f-faea-4e35-b7a6-09e2c5a5965d",
    context: null,
    expiresOn: null,
    forDetection: false,
    redirectionUuid: null,
    time: new Date("2021-12-15T19:21:51.475601+00:00"),
    type: {
      description: null,
      value: "file",
      uuid: "7a58e9a0-f9ab-4e25-8c81-030ddb50e1ad",
    },
    value: "email.rfc822.unknown_plain_text_000",
    comments: [],
    parentTreeUuid: "baa866a3-d704-4429-bb09-05a8fb83cf23",
    treeUuid: "775cc0bf-cc8d-4333-9002-c2c7a0f1162e",
    uuid: "fea9e7b2-276c-4b48-8a9a-fc1b33bc96c4",
  },
  {
    analysisModuleType: {
      value: "URL Extraction Analysis",
      uuid: "20053d70-6af0-41e8-bc2a-2088f2f53d6e",
    },
    parentTreeUuid: "775cc0bf-cc8d-4333-9002-c2c7a0f1162e",
    treeUuid: "a5eb0e6a-7608-4c83-a03a-aeaa3eea1c26",
    uuid: "5712f2bd-503c-4ae9-b3d6-55ddf0b9b655",
  },
  {
    directives: [],
    tags: [],
    threatActor: null,
    threats: [],
    version: "4575351e-e864-4926-b825-29db5f3de955",
    context: null,
    expiresOn: null,
    forDetection: false,
    redirectionUuid: null,
    time: new Date("2021-12-15T19:21:51.496415+00:00"),
    type: {
      description: null,
      value: "url",
      uuid: "ddfdbacc-fe3b-495f-9bbc-ffaa0ed35007",
    },
    value: "http://evil.com/malware.exe",
    comments: [],
    parentTreeUuid: "a5eb0e6a-7608-4c83-a03a-aeaa3eea1c26",
    treeUuid: "689fbced-7def-4706-b804-93152aea874e",
    uuid: "1942c3d9-2520-48d5-8f1e-19d10959e399",
  },
  {
    analysisModuleType: {
      value: "URL Parse Analysis",
      uuid: "70ea2c84-ceaa-4516-8da6-9373c0f7cbe9",
    },
    parentTreeUuid: "689fbced-7def-4706-b804-93152aea874e",
    treeUuid: "0cec6cf7-d810-408a-9825-3c95576c2127",
    uuid: "bca0249c-78c0-4495-9af5-9e71d9116399",
  },
  {
    directives: [],
    tags: [],
    threatActor: null,
    threats: [],
    version: "289a65cc-7ca9-48ca-8e48-27104802631f",
    context: null,
    expiresOn: null,
    forDetection: false,
    redirectionUuid: null,
    time: new Date("2021-12-15T19:21:51.423600+00:00"),
    type: {
      description: null,
      value: "fqdn",
      uuid: "91441637-523b-4609-81f8-da161b68e3eb",
    },
    value: "evil.com",
    comments: [],
    parentTreeUuid: "0cec6cf7-d810-408a-9825-3c95576c2127",
    treeUuid: "6b54b9e9-a767-4e3d-9061-df71bd028a61",
    uuid: "a88dfca9-9849-446a-92ba-d2e6fb8308d9",
  },
  {
    directives: [],
    tags: [],
    threatActor: null,
    threats: [],
    version: "4d63eeec-02e0-4f31-9b47-518b6095ecce",
    context: null,
    expiresOn: null,
    forDetection: false,
    redirectionUuid: null,
    time: new Date("2021-12-15T19:21:51.523629+00:00"),
    type: {
      description: null,
      value: "uri_path",
      uuid: "9dc7e81d-a26c-4a66-ab2c-87db92583715",
    },
    value: "/malware.exe",
    comments: [],
    parentTreeUuid: "0cec6cf7-d810-408a-9825-3c95576c2127",
    treeUuid: "37d09793-b132-4971-89c2-f6014b81ecc8",
    uuid: "97b88904-4fad-47c7-935f-aaeec7a700c6",
  },
  {
    analysisModuleType: {
      value: "File Analysis",
      uuid: "46bdd9d1-e9d5-4d1b-83b2-1ccccdd9b711",
    },
    parentTreeUuid: "ba9b3b3b-9904-43f7-812d-d187532b4d31",
    treeUuid: "524e0a5f-8406-411c-86f1-27437e65bcf6",
    uuid: "50aa1b1a-baef-413f-9fb2-f24450e73ece",
  },
  {
    directives: [],
    tags: [],
    threatActor: null,
    threats: [],
    version: "0dabea32-4df0-4078-871b-0dab13233d64",
    context: null,
    expiresOn: null,
    forDetection: false,
    redirectionUuid: null,
    time: new Date("2021-12-15T19:21:51.545867+00:00"),
    type: {
      description: null,
      value: "md5",
      uuid: "ebcf1db0-6644-4f1f-bea3-7c5660ddbb29",
    },
    value: "912ec803b2ce49e4a541068d495ab570",
    comments: [],
    parentTreeUuid: "524e0a5f-8406-411c-86f1-27437e65bcf6",
    treeUuid: "bdf8fea8-8447-4bbe-b7ee-7d7ca07e6b6c",
    uuid: "0c05be68-58b1-4744-a1b3-f12eefd6e75e",
  },
  {
    directives: [],
    tags: [
      {
        description: null,
        value: "c2",
        uuid: "59a5e47d-5f35-45d0-9a21-f473a5fb546b",
      },
      {
        description: null,
        value: "contacted_host",
        uuid: "29a85e3b-dbf5-4ba2-879b-2423115a2711",
      },
    ],
    threatActor: null,
    threats: [],
    version: "99078314-16cd-4496-a592-2a82fa5309f0",
    context: null,
    expiresOn: null,
    forDetection: false,
    redirectionUuid: null,
    time: new Date("2021-12-15T19:21:51.557310+00:00"),
    type: {
      description: null,
      value: "ipv4",
      uuid: "8d53473c-ba62-4713-8484-0ef8637f73c3",
    },
    value: "127.0.0.1",
    comments: [],
    parentTreeUuid: null,
    treeUuid: "f096b869-fc93-4349-ad4c-bb97c699782d",
    uuid: "41dd07b2-1c36-413d-ae90-e96761513d4c",
  },
];

describe("ViewAlert.vue", () => {
  // const router = createRouterMock({
  //   initialLocation: "/alert/uuid1",
  // });

  // let wrapper: VueWrapper<any>;

  // beforeEach(async () => {
  // injectRouterMock(router);
  // getRouter().setParams({ alertID: "uuid1" });
  // router.push("/alert/uuid1")
  //     const wrapper = mount(ViewAlert, {
  //       global: {
  //         mocks: {
  // $route
  //         },
  //         provide: {
  //           plugins: [ createTestingPinia({ stubActions: false })],
  //         },
  //       },
  //     });
  // });

  it.only("renders", async () => {
    const wrapper = mount(ViewAlert, {
      global: {
        // mocks: {
        //   useRoute: jest.fn(() => ({ params: { alertID: "uuid1" } })),
        // },
        provide: {
          plugins: [createTestingPinia({ stubActions: false })],
        },
      },
    });
    expect(wrapper.exists()).toBe(true);
  });
  // it("selects open alert when mounted", async () => {
  //   const alertStore = useAlertStore();
  //   // alertStore.openAlert = { alert: mockAlert, tree: mockTree };

  //   console.log(alertStore.openAlert);
  //   console.log(wrapper.vm.alertTree);
  // });
});
