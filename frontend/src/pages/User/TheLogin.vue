<!-- ManageAlerts.vue -->

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
            @click="login"
          ></Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapActions } from "pinia";
  import Button from "primevue/button";
  import InputText from "primevue/inputtext";

  import authApi from "@/services/api/auth";
  import { useAuthStore } from "@/stores/auth";

  export default {
    components: {
      Button,
      InputText,
    },
    data() {
      return {
        username: null,
        password: null,
      };
    },
    computed: {
      loginData() {
        return { username: this.username, password: this.password };
      },
    },
    methods: {
      ...mapActions(useAuthStore, ["setAuthenticated"]),

      async login() {
        await authApi
          .authenticate(this.loginData)
          .then(() => {
            this.setAuthenticated(true);
          })
          .catch(() => {
            // TODO: Add a proper message saying the login failed
            console.error("Invalid username or password");
            this.setAuthenticated(false);
          });

        this.resetData();
        this.$router.replace({ name: "Manage Alerts" });
      },

      resetData() {
        (this.username = null), (this.password = null);
      },
    },
  };
</script>
