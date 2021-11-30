<template>
  <div>
    <ul>
      <li v-for="i of items" :key="i.uuid">
        {{ treeItemName(i) }} {{ tagString(i) }}
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

      tagString(item) {
        let string = "";

        if ("tags" in item) {
          for (let i = 0; i < item.tags.length; i++) {
            string = string + "(" + item.tags[i].value + ") ";
          }
        }

        return string;
      },
    },
  };
</script>
