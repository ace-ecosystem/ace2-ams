import { AxiosRequestConfig } from "axios";
import camelcaseKeys from "camelcase-keys";

import { useAuthStore } from "@/stores/auth";
import instance, { axiosRefresh } from "@/services/api/axios";

export default {
  // AUTH
  async authenticate(loginData: {
    username: string;
    password: string;
  }): Promise<void> {
    const authStore = useAuthStore();

    const config: AxiosRequestConfig = {
      url: "/auth",
      method: "POST",
      withCredentials: true,
    };

    const formData = new FormData();
    formData.append("username", loginData.username);
    formData.append("password", loginData.password);
    config["data"] = formData;
    config["headers"] = {
      "content-type": "application/x-www-form-urlencoded",
    };

    const response = await instance.request(config).catch((error) => {
      authStore.$reset();
      throw error;
    });

    authStore.user = camelcaseKeys(response.data.user, { deep: true });
  },

  // REFRESH AUTH
  async refresh(): Promise<void> {
    // The axiosRefresh function is used to avoid circular dependencies between auth.ts and axios.ts
    await axiosRefresh();
  },

  // VALIDATE
  async validate(): Promise<void> {
    const authStore = useAuthStore();

    const config: AxiosRequestConfig = {
      url: "/auth/validate",
      method: "GET",
      withCredentials: true,
    };

    await instance.request(config).catch((error) => {
      console.debug("refresh token not present or expired");
      authStore.$reset();
      throw error;
    });
  },

  // LOGOUT
  async logout(): Promise<void> {
    const authStore = useAuthStore();

    const config: AxiosRequestConfig = {
      url: "/auth/logout",
      method: "GET",
      withCredentials: true,
    };

    authStore.$reset();

    await instance.request(config).catch((error) => {
      throw error;
    });
  },
};
