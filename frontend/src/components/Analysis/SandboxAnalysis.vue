<!-- AnalysisDetailsBase.vue -->
<!-- Base/Details component for analysis details -->

<template>
  <div>
    <ul>
      <li
        v-for="file in files"
        :key="file.md5"
        class="link-text"
        @click="scrollTo(file.md5)"
      >
        {{ file.legend }}
      </li>
    </ul>
  </div>
  <div v-for="file in files" :key="file.md5">
    <Fieldset
      :id="file.md5"
      :legend="file.legend"
      :toggleable="true"
      responsive-layout="scroll"
    >
      <Fieldset
        legend="Sandbox URLs"
        :toggleable="true"
        responsive-layout="scroll"
      >
        <div style="width: 90vw">
          <ul>
            <li v-for="url in file.urls" :key="url">
              <a :href="url">{{ url }}</a>
            </li>
          </ul>
        </div>
      </Fieldset>
      <Fieldset
        v-if="file.contactedHosts.length"
        legend="Contacted Hosts"
        :toggleable="true"
        responsive-layout="scroll"
      >
        <div style="width: 90vw">
          <DataTable
            :value="file.contactedHosts"
            sort-field="ip"
            :sort-order="1"
            class="p-datatable-sm"
            ><Column field="ip" header="Address" :sortable="true"></Column
            ><Column field="port" header="Port" :sortable="true"></Column
            ><Column
              field="protocol"
              header="Protocol"
              :sortable="true"
            ></Column
            ><Column
              field="location"
              header="Location"
              :sortable="true"
            ></Column
            ><Column field="associatedDomains" header="Associated Domains"
              ><template #body="slotProps">
                <span class="flex align-items-center justify-content-center">
                  {{ slotProps.data.associatedDomains.join() }}
                </span>
              </template></Column
            ></DataTable
          >
        </div>
      </Fieldset>

      <Fieldset
        v-if="file.dnsRequests.length"
        legend="DNS Requests"
        :toggleable="true"
        responsive-layout="scroll"
      >
        <div style="width: 90vw">
          <DataTable
            :value="file.dnsRequests"
            sort-field="request"
            :sort-order="1"
            class="p-datatable-sm"
            ><Column field="request" header="Request" :sortable="true"></Column
            ><Column field="type" header="Type" :sortable="true"></Column
            ><Column field="answer" header="Answer" :sortable="true"></Column
            ><Column
              field="answerType"
              header="Answer Type"
              :sortable="true"
            ></Column
          ></DataTable>
        </div>
      </Fieldset>

      <Fieldset
        v-if="file.droppedFiles.length"
        legend="Dropped Files"
        :toggleable="true"
        responsive-layout="scroll"
      >
        <div style="width: 90vw">
          <DataTable
            :value="file.droppedFiles"
            sort-field="filename"
            :sort-order="1"
            class="p-datatable-sm"
            responsive-layout="scroll"
            ><Column
              field="filename"
              header="Filename"
              :sortable="true"
            ></Column
            ><Column field="path" header="Path" :sortable="true"></Column
            ><Column field="size" header="Size" :sortable="true"></Column
            ><Column field="type" header="Type" :sortable="true"></Column
            ><Column field="md5" header="MD5" :sortable="true"></Column
            ><Column field="sha1" header="SHA1" :sortable="true"></Column
            ><Column field="sha256" header="SHA256" :sortable="true"></Column
            ><Column field="sha512" header="SHA512" :sortable="true"></Column
            ><Column field="ssdeep" header="ssdeep" :sortable="true"></Column
          ></DataTable>
        </div>
      </Fieldset>

      <Fieldset
        v-if="file.httpRequests.length"
        legend="HTTP Requests"
        :toggleable="true"
      >
        <div style="width: 90vw">
          <DataTable
            :value="file.httpRequests"
            sort-field="host"
            :sort-order="1"
            class="p-datatable-sm"
            responsive-layout="scroll"
            ><Column field="method" header="Method" :sortable="true"></Column
            ><Column field="host" header="Host" :sortable="true"></Column
            ><Column field="port" header="Port" :sortable="true"></Column
            ><Column field="path" header="URI" :sortable="true"></Column
            ><Column
              field="userAgent"
              header="User-Agent"
              :sortable="true"
            ></Column
          ></DataTable>
        </div>
      </Fieldset>
      <Fieldset
        v-if="file.mutexes.length"
        legend="Mutexes"
        :toggleable="true"
        responsive-layout="scroll"
      >
        <div style="width: 90vw">
          <pre v-for="mutex in file.mutexes" :key="mutex">{{ mutex }}</pre>
        </div>
      </Fieldset>

      <Fieldset
        v-if="file.processTrees.length"
        legend="Process Trees"
        :toggleable="true"
        responsive-layout="scroll"
      >
        <div style="width: 90vw">
          <div v-for="tree in file.processTrees" :key="tree">
            <pre>{{ tree }}</pre>
          </div>
        </div>
      </Fieldset>
    </Fieldset>
    <br />
  </div>
</template>

<script setup lang="ts">
  import { onMounted, ref, defineProps, computed } from "vue";
  import { Event } from "@/services/api/event";
  import { sandboxSummary } from "@/models/eventSummaries";
  import Fieldset from "primevue/fieldset";
  import DataTable from "primevue/datatable";
  import Column from "primevue/column";

  import {
    sandboxContactedHost,
    sandboxDnsRequest,
    sandboxDroppedFile,
    sandboxHttpRequest,
  } from "@/models/sandbox";

  const props = defineProps({
    eventUuid: { type: String, required: true },
  });
  const isLoading = ref(false);
  const sandboxSummariesByHash = ref({} as Record<string, sandboxSummary[]>);

  onMounted(async () => {
    isLoading.value = true;
    const sandboxSummaries = await Event.readSandboxSummary(props.eventUuid);
    if (sandboxSummaries) {
      sandboxSummariesByHash.value = groupByHash(sandboxSummaries);
    }
    isLoading.value = false;
  });

  const files = computed(() => {
    return Object.keys(sandboxSummariesByHash.value).map((md5) => {
      const names: string[] = [];
      const urls: string[] = [];
      const contactedHosts: sandboxContactedHost[] = [];
      const dnsRequests: sandboxDnsRequest[] = [];
      const droppedFiles: sandboxDroppedFile[] = [];
      const httpRequests: sandboxHttpRequest[] = [];
      const mutexes: string[] = [];
      const processTrees: string[] = [];

      sandboxSummariesByHash.value[md5].forEach((summary) => {
        if (!names.includes(summary.filename)) {
          names.push(summary.filename);
        }

        urls.push(summary.sandboxUrl);
        contactedHosts.push(...summary.contactedHosts);
        dnsRequests.push(...summary.dnsRequests);
        droppedFiles.push(...summary.droppedFiles);
        httpRequests.push(...summary.httpRequests);
        mutexes.push(...summary.mutexes);
        processTrees.push(summary.processTree);
      });

      return {
        md5: md5,
        legend: `${names.join(" | ")}: ${md5} `,
        urls: urls,
        contactedHosts: dedupe(contactedHosts),
        dnsRequests: dedupe(dnsRequests),
        droppedFiles: dedupe(droppedFiles),
        httpRequests: dedupe(httpRequests),
        mutexes: dedupe(mutexes),
        processTrees: [...new Set(processTrees)],
      };
    });
  });

  function scrollTo(md5: string) {
    console.log(md5);
    document.getElementById(md5)?.scrollIntoView();
  }

  function dedupe<T>(arr: T[]) {
    return arr.reduce(
      (r: T[], i: T) =>
        !r.some((j) => JSON.stringify(i) === JSON.stringify(j)) ? [...r, i] : r,
      [],
    );
  }

  const groupByHash = (summaries: sandboxSummary[]) => {
    return summaries.reduce(
      (r: Record<string, sandboxSummary[]>, v, i, a, k = v.md5) => (
        (r[k] || (r[k] = [])).push(v), r
      ),
      {},
    );
  };
</script>

<style>
  .p-fieldset {
    margin-top: 15px;
  }
</style>
