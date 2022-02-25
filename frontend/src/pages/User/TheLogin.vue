<template>
  <div class="card" name="loginForm">
    <div class="flex align-items-center justify-content-center">
      <div class="surface-card p-4 shadow-2 border-round w-full lg:w-6">
        <div class="text-center mb-5">
          <div class="text-900 text-3xl font-medium mb-3">Welcome Back :)</div>
        </div>

        <div>
          <label for="username" class="block text-900 font-medium mb-2"
            >Username</label
          >
          <InputText
            id="username"
            v-model="username"
            type="text"
            class="w-full mb-3"
          />

          <label for="password" class="block text-900 font-medium mb-2"
            >Password</label
          >
          <InputText
            id="password"
            v-model="password"
            type="password"
            class="w-full mb-3"
            @keyup.enter="login"
          />

          <Button
            id="submit"
            label="Log In"
            icon="pi pi-user"
            class="w-full"
            :disabled="isDisabled"
            @click="login"
          ></Button>
        </div>

        <!-- Make a reusable Error component -->
        <div v-if="loginError" id="error" class="p-error">
          Invalid username or password
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { computed, ref } from "vue";
  import { useRouter } from "vue-router";

  import Button from "primevue/button";
  import InputText from "primevue/inputtext";

  import { populateCommonStores, setUserDefaults } from "@/etc/helpers";
  import authApi from "@/services/api/auth";

  const router = useRouter();

  const username = ref(null);
  const password = ref(null);

  const loginError = ref(false);

  const isDisabled = computed(() => {
    return username.value == null || password.value == null;
  });

  const loginData = computed(() => {
    return { username: username.value, password: password.value };
  });

  const login = async () => {
    await authApi
      .authenticate(loginData.value)
      .then(async () => {
        loginError.value = false;

        // And then populate some of the stores with items from the API that
        // will be used throughout the application.
        await populateCommonStores();
        setUserDefaults();
      })
      .catch(() => {
        console.error("Invalid username or password");
        loginError.value = true;
      });

    username.value = null;
    password.value = null;
    router.replace({ name: "Manage Alerts" });
  };
</script>
