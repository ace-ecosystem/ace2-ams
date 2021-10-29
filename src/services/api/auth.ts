import { AxiosRequestConfig } from "axios";

import instance, { axiosRefresh } from "@/services/api/axios";

export default {
  // AUTH
  async authenticate(loginData: {
    username: string;
    password: string;
  }): Promise<void> {
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

    await instance.request(config).catch((error) => {
      sessionStorage.removeItem("authenticated");
      throw error;
    });

    sessionStorage.setItem("authenticated", "yes");
  },

  // REFRESH AUTH
  async refresh(): Promise<void> {
    // The axiosRefresh function is used to avoid circular dependencies between auth.ts and axios.ts
    return axiosRefresh();
  },

  // VALIDATE
  async validate(): Promise<void> {
    const config: AxiosRequestConfig = {
      url: "/auth/validate",
      method: "GET",
      withCredentials: true,
    };

    await instance.request(config).catch((error) => {
      console.debug("refresh token not present or expired");
      sessionStorage.removeItem("authenticated");
      throw error;
    });
  },

  // LOGOUT
  async logout(): Promise<void> {
    const config: AxiosRequestConfig = {
      url: "/auth/logout",
      method: "GET",
      withCredentials: true,
    };

    await instance.request(config).catch((error) => {
      throw error;
    });

    sessionStorage.removeItem("authenticated");
  },
};
