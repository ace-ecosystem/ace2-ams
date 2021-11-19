<template>
  <div>
    <ul>
      <li v-for="i of items" :key="i.uuid">
        {{ treeItemName(i) }}
        <AlertTree v-if="i.children" :items="i.children" />
      </li>
    </ul>
  </div>
</template>

<script>
  export default {
    name: "AlertTree",
    props: {
      items: { type: Array, required: true },
    },

    methods: {
      treeItemName(item) {
        if (item.parentUuid === null) {
          return "Root Analysis";
        }

        if ("analysisModuleType" in item) {
          return item.analysisModuleType.value;
        }

        if ("observable" in item) {
          return item.observable.type.value + ": " + item.observable.value;
        }
      },
    },
  };
</script>
