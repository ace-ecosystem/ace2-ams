// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import router from "@/router/index";
import SandboxAnalysis from "@/components/Analysis/SandboxAnalysis.vue";
import { Event } from "@/services/api/event";
import { sandboxSummary } from "@/models/eventSummaries";

interface sandboxAnalysisProps {
  eventUuid: string;
}

function factory(props: sandboxAnalysisProps) {
  return mount(SandboxAnalysis, {
    global: {
      plugins: [PrimeVue, createPinia(), router],
    },
    propsData: props,
  });
}

describe("SandboxAnalysis Blank State", () => {
  it("renders when API call returns nothing", () => {
    const stub = cy.stub(Event, "readSandboxSummary");
    stub.withArgs("blankUuid").as("readBlankSandboxSummary").resolves([]);
    factory({ eventUuid: "blankUuid" });
    cy.contains(emptyMessage).should("be.visible");
    cy.contains(errorMessage).should("not.exist");
  });
});
describe("SandboxAnalysis Results", () => {
  it("renders multiple sandbox summaries correctly", () => {
    const stub = cy.stub(Event, "readSandboxSummary");
    stub
      .withArgs("resultsUuid")
      .as("readResultsSandboxSummary")
      .resolves(results);
    factory({ eventUuid: "resultsUuid" });
    cy.contains(errorMessage).should("not.exist");
    cy.contains(emptyMessage).should("not.exist");

    // Check that each files links and headers are there
    cy.findAllByText("email.rfc822: 912ec803b2ce49e4a541068d495ab570")
      .should("be.visible")
      .should("have.length", 2);
    cy.findAllByText(
      "malware.exe | malware_alt.exe: 9051c29972c935649d8fa4b823e54dea",
    )
      .should("be.visible")
      .should("have.length", 2);

    // Check first file's sections
    // URLS
    cy.get("[data-cy=912ec803b2ce49e4a541068d495ab570-urls]")
      .should("be.visible")
      .get("[data-cy=912ec803b2ce49e4a541068d495ab570-urls] li")
      .should("have.text", "https://blah.url");
    // Rest should not be visible
    cy.get("[data-cy=912ec803b2ce49e4a541068d495ab570-contacted-hosts]").should(
      "not.exist",
    );
    cy.get("[data-cy=912ec803b2ce49e4a541068d495ab570-dns-requests]").should(
      "not.exist",
    );
    cy.get("[data-cy=912ec803b2ce49e4a541068d495ab570-dropped-files]").should(
      "not.exist",
    );
    cy.get("[data-cy=912ec803b2ce49e4a541068d495ab570-http-requests]").should(
      "not.exist",
    );
    cy.get("[data-cy=912ec803b2ce49e4a541068d495ab570-mutexes]").should(
      "not.exist",
    );
    cy.get("[data-cy=912ec803b2ce49e4a541068d495ab570-process-trees]").should(
      "not.exist",
    );

    // Check second file's sections
    // URLS
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-urls]").should(
      "be.visible",
    );
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-urls] li")
      .eq(0)
      .should("have.text", "https://url.to.sandbox.report");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-urls] li")
      .eq(1)
      .should("have.text", "https://different.url.to.sandbox.report");
    // Contacted Hosts
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-contacted-hosts]").should(
      "be.visible",
    );
    cy.get(
      "[data-cy=9051c29972c935649d8fa4b823e54dea-contacted-hosts] td",
    ).should("have.length", 10);
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-contacted-hosts] td")
      .eq(0)
      .should("have.text", "127.0.0.1");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-contacted-hosts] td")
      .eq(1)
      .should("have.text", "80");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-contacted-hosts] td")
      .eq(2)
      .should("have.text", "TCP");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-contacted-hosts] td")
      .eq(3)
      .should("have.text", "some place");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-contacted-hosts] td")
      .eq(4)
      .should("have.text", "domain1,domain2");

    //  DNS Requests
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-dns-requests]").should(
      "be.visible",
    );
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-dns-requests] td").should(
      "have.length",
      8,
    );
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-dns-requests] td")
      .eq(0)
      .should("have.text", "malware.com");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-dns-requests] td")
      .eq(1)
      .should("have.text", "A");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-dns-requests] td")
      .eq(2)
      .should("have.text", "127.0.0.1");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-dns-requests] td")
      .eq(3)
      .should("have.text", "A");

    // Dropped Files
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-dropped-files]").should(
      "be.visible",
    );
    cy.get(
      "[data-cy=9051c29972c935649d8fa4b823e54dea-dropped-files] td",
    ).should("have.length", 18);
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-dropped-files] td")
      .eq(0)
      .should("have.text", "dropped1.exe");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-dropped-files] td")
      .eq(1)
      .should("have.text", "c:\\users\\analyst\\desktop\\dropped1.exe");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-dropped-files] td")
      .eq(2)
      .should("have.text", "100");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-dropped-files] td")
      .eq(3)
      .should("have.text", "application/octet-stream");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-dropped-files] td")
      .eq(4)
      .should("have.text", "10239eb7264449296277d10538e27f3e");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-dropped-files] td")
      .eq(5)
      .should("have.text", "344329cc1356f227a722ad81e36a6e5baf6a0642");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-dropped-files] td")
      .eq(6)
      .should(
        "have.text",
        "17d771db597ca8eb06c874200a067d7ac4374aa14d7b775a3b57181e69cfb100",
      );
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-dropped-files] td")
      .eq(7)
      .should(
        "have.text",
        "54f61aba3cfb0249b84b9b2464b946e1039615dbebe6ce2ca6403c91945ef30a6156eb5c3ec330fe8c67b34e8a8b71a2f6e8d394874a72dd06fb96649d020682",
      );
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-dropped-files] td")
      .eq(8)
      .should("have.text", "3:cIoN:cb");

    // HTTP Requests
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-http-requests]").should(
      "be.visible",
    );
    cy.get(
      "[data-cy=9051c29972c935649d8fa4b823e54dea-http-requests] td",
    ).should("have.length", 10);
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-http-requests] td")
      .eq(0)
      .should("have.text", "GET");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-http-requests] td")
      .eq(1)
      .should("have.text", "malware.com");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-http-requests] td")
      .eq(2)
      .should("have.text", "80");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-http-requests] td")
      .eq(3)
      .should("have.text", "/malware.exe");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-http-requests] td")
      .eq(4)
      .should(
        "have.text",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
      );

    // Mutexes
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-mutexes]").should(
      "be.visible",
    );
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-mutexes] pre").should(
      "have.length",
      2,
    );
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-mutexes] pre")
      .eq(0)
      .should("have.text", "mutex1");
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-mutexes] pre")
      .eq(1)
      .should("have.text", "mutex2");

    // Process Trees
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-process-trees]").should(
      "be.visible",
    );
    cy.get("[data-cy=9051c29972c935649d8fa4b823e54dea-process-trees] pre")
      .should("be.visible")
      .should(
        "contain.text",
        "malware.exe\n    sub_command1\n        sub_sub_command1\n    sub_command2",
      );
  });
});
describe("SandboxAnalysis Error", () => {
  it("renders correctly when API call fails", () => {
    const stub = cy.stub(Event, "readSandboxSummary");
    stub
      .withArgs("errorUuid")
      .as("readErrorSandboxSummary")
      .rejects(new Error(errorMessage));
    factory({ eventUuid: "errorUuid" });
    cy.contains(errorMessage).should("be.visible");
    cy.contains(emptyMessage).should("be.visible");
  });
});

const errorMessage = "404 Request failed";
const emptyMessage = "No sandbox analysis available.";

const results: sandboxSummary[] = [
  {
    contactedHosts: [],
    createdServices: ["created_service1", "created_service2"],
    dnsRequests: [],
    droppedFiles: [],
    filename: "email.rfc822",
    httpRequests: [],
    malwareFamily: "ransomware",
    md5: "912ec803b2ce49e4a541068d495ab570",
    memoryStrings: ["memory_string1", "memory_string2"],
    memoryUrls: [],
    mutexes: [],
    processes: [],
    registryKeys: ["registry_key1", "registry_key2"],
    resolvedApis: ["resolved_api1", "resolved_api2"],
    sandboxUrl: "https://blah.url",
    sha1: "2da7b04fa4f6e94c7c82c1c8ee09ead16121bc60",
    sha256: "66ecfc29b6d458538b23310988289158f319e2e1cf7587413011d43a639c6ec0",
    sha512:
      "951c56c1bad4cdb721da736d9f1c04ebbbf32d2737c8ec8c64086a4c5448cb37f95784186c8c67c42b7bc622ba6358dc8befee750c14bcf5136a6706a19e007b",
    ssdeep: "3:5c+a:q",
    startedServices: ["started_service1", "started_service2"],
    stringsUrls: ["https://string.url1", "https://string.url2"],
    suricataAlerts: ["suricata_alert1", "suricata_alert2"],
    processTree: "",
  },
  {
    contactedHosts: [
      {
        ip: "127.0.0.1",
        port: 80,
        protocol: "TCP",
        location: "some place",
        associatedDomains: ["domain1", "domain2"],
      },
      {
        ip: "192.168.1.1",
        port: 443,
        protocol: "TCP",
        location: "some other place",
        associatedDomains: [],
      },
    ],
    createdServices: ["created_service1", "created_service2"],
    dnsRequests: [
      {
        request: "malware.com",
        type: "A",
        answer: "127.0.0.1",
        answerType: "A",
      },
      {
        request: "othermalware.com",
        type: "A",
        answer: "192.168.1.1",
        answerType: "A",
      },
    ],
    droppedFiles: [
      {
        filename: "dropped1.exe",
        path: "c:\\users\\analyst\\desktop\\dropped1.exe",
        size: 100,
        type: "application/octet-stream",
        md5: "10239eb7264449296277d10538e27f3e",
        sha1: "344329cc1356f227a722ad81e36a6e5baf6a0642",
        sha256:
          "17d771db597ca8eb06c874200a067d7ac4374aa14d7b775a3b57181e69cfb100",
        sha512:
          "54f61aba3cfb0249b84b9b2464b946e1039615dbebe6ce2ca6403c91945ef30a6156eb5c3ec330fe8c67b34e8a8b71a2f6e8d394874a72dd06fb96649d020682",
        ssdeep: "3:cIoN:cb",
      },
      {
        filename: "dropped2.exe",
        path: "c:\\users\\analyst\\desktop\\dropped2.exe",
        size: 100,
        type: "application/octet-stream",
        md5: "8ad98e2965070ebbb86a95e35c18010f",
        sha1: "6e1833d62213441c60edce1a4cfb6674af102d69",
        sha256:
          "fc0fefa8d1f318419f927bc3b793bf66a035d59f24874ce7cf773f9162d0a158",
        sha512:
          "6774d837fb2851c1c1d89170068caa1b81143b81ec7fbf4322b3ffdbc24efcebcc12d763d1c6f4b0c843e43427671453167b1c50ed5f71c7ede8759f75f39732",
        ssdeep: "3:cIeAn:ckn",
      },
    ],
    filename: "malware.exe",
    httpRequests: [
      {
        host: "malware.com",
        port: 80,
        path: "/malware.exe",
        method: "GET",
        userAgent:
          "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
      },
      {
        host: "othermalware.com",
        port: 443,
        path: "/othermalware.exe",
        method: "GET",
        userAgent:
          "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
      },
    ],
    malwareFamily: "ransomware",
    md5: "9051c29972c935649d8fa4b823e54dea",
    memoryStrings: ["memory_string1", "memory_string2"],
    memoryUrls: [],
    mutexes: ["mutex1", "mutex2"],
    processes: [
      {
        command: "malware.exe",
        pid: 1000,
        parentPid: 0,
      },
      {
        command: "sub_command1",
        pid: 1001,
        parentPid: 1000,
      },
      {
        command: "sub_sub_command1",
        pid: 1002,
        parentPid: 1001,
      },
      { command: "sub_command2", pid: 1003, parentPid: 1000 },
    ],
    registryKeys: ["registry_key1", "registry_key2"],
    resolvedApis: ["resolved_api1", "resolved_api2"],
    sandboxUrl: "https://url.to.sandbox.report",
    sha1: "2da7b04fa4f6e94c7c82c1c8ee09ead16121bc60",
    sha256: "66ecfc29b6d458538b23310988289158f319e2e1cf7587413011d43a639c6ec0",
    sha512:
      "951c56c1bad4cdb721da736d9f1c04ebbbf32d2737c8ec8c64086a4c5448cb37f95784186c8c67c42b7bc622ba6358dc8befee750c14bcf5136a6706a19e007b",
    ssdeep: "3:5c+a:q",
    startedServices: ["started_service1", "started_service2"],
    stringsUrls: ["https://string.url1", "https://string.url2"],
    suricataAlerts: ["suricata_alert1", "suricata_alert2"],
    processTree:
      "malware.exe\n    sub_command1\n        sub_sub_command1\n    sub_command2",
  },
  {
    contactedHosts: [
      {
        ip: "127.0.0.1",
        port: 80,
        protocol: "TCP",
        location: "some place",
        associatedDomains: ["domain1", "domain2"],
      },
      {
        ip: "192.168.1.1",
        port: 443,
        protocol: "TCP",
        location: "some other place",
        associatedDomains: [],
      },
    ],
    createdServices: ["created_service1", "created_service2"],
    dnsRequests: [
      {
        request: "malware.com",
        type: "A",
        answer: "127.0.0.1",
        answerType: "A",
      },
      {
        request: "othermalware.com",
        type: "A",
        answer: "192.168.1.1",
        answerType: "A",
      },
    ],
    droppedFiles: [
      {
        filename: "dropped1.exe",
        path: "c:\\users\\analyst\\desktop\\dropped1.exe",
        size: 100,
        type: "application/octet-stream",
        md5: "10239eb7264449296277d10538e27f3e",
        sha1: "344329cc1356f227a722ad81e36a6e5baf6a0642",
        sha256:
          "17d771db597ca8eb06c874200a067d7ac4374aa14d7b775a3b57181e69cfb100",
        sha512:
          "54f61aba3cfb0249b84b9b2464b946e1039615dbebe6ce2ca6403c91945ef30a6156eb5c3ec330fe8c67b34e8a8b71a2f6e8d394874a72dd06fb96649d020682",
        ssdeep: "3:cIoN:cb",
      },
      {
        filename: "dropped2.exe",
        path: "c:\\users\\analyst\\desktop\\dropped2.exe",
        size: 100,
        type: "application/octet-stream",
        md5: "8ad98e2965070ebbb86a95e35c18010f",
        sha1: "6e1833d62213441c60edce1a4cfb6674af102d69",
        sha256:
          "fc0fefa8d1f318419f927bc3b793bf66a035d59f24874ce7cf773f9162d0a158",
        sha512:
          "6774d837fb2851c1c1d89170068caa1b81143b81ec7fbf4322b3ffdbc24efcebcc12d763d1c6f4b0c843e43427671453167b1c50ed5f71c7ede8759f75f39732",
        ssdeep: "3:cIeAn:ckn",
      },
    ],
    filename: "malware_alt.exe",
    httpRequests: [
      {
        host: "malware.com",
        port: 80,
        path: "/malware.exe",
        method: "GET",
        userAgent:
          "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
      },
      {
        host: "othermalware.com",
        port: 443,
        path: "/othermalware.exe",
        method: "GET",
        userAgent:
          "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
      },
    ],
    malwareFamily: "ransomware",
    md5: "9051c29972c935649d8fa4b823e54dea",
    memoryStrings: ["memory_string1", "memory_string2"],
    memoryUrls: [],
    mutexes: ["mutex1", "mutex2"],
    processes: [
      {
        command: "malware.exe",
        pid: 1000,
        parentPid: 0,
      },
      {
        command: "sub_command1",
        pid: 1001,
        parentPid: 1000,
      },
      {
        command: "sub_sub_command1",
        pid: 1002,
        parentPid: 1001,
      },
      { command: "sub_command2", pid: 1003, parentPid: 1000 },
    ],
    registryKeys: ["registry_key1", "registry_key2"],
    resolvedApis: ["resolved_api1", "resolved_api2"],
    sandboxUrl: "https://different.url.to.sandbox.report",
    sha1: "2da7b04fa4f6e94c7c82c1c8ee09ead16121bc60",
    sha256: "66ecfc29b6d458538b23310988289158f319e2e1cf7587413011d43a639c6ec0",
    sha512:
      "951c56c1bad4cdb721da736d9f1c04ebbbf32d2737c8ec8c64086a4c5448cb37f95784186c8c67c42b7bc622ba6358dc8befee750c14bcf5136a6706a19e007b",
    ssdeep: "3:5c+a:q",
    startedServices: ["started_service1", "started_service2"],
    stringsUrls: ["https://string.url1", "https://string.url2"],
    suricataAlerts: ["suricata_alert1", "suricata_alert2"],
    processTree:
      "malware.exe\n    sub_command1\n        sub_sub_command1\n    sub_command2",
  },
];
