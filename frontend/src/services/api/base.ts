/* eslint-disable @typescript-eslint/no-explicit-any */

import { AxiosRequestConfig } from "axios";
import instance from "./axios";
import camelcaseKeys from "camelcase-keys";
import snakecaseKeys from "snakecase-keys";
import { page } from "@/models/base";

type Method = "GET" | "DELETE" | "POST" | "PATCH";

export class BaseApi {
  formatIncomingData(data: Record<string, unknown>): Record<string, unknown> {
    return camelcaseKeys(data, { deep: true });
  }

  formatOutgoingData(data: Record<string, unknown>): Record<string, unknown> {
    return snakecaseKeys(data);
  }

  methodDict = {
    POST: "create",
    GET: "fetch",
    PATCH: "update",
    DELETE: "delete",
  };

  async baseRequest(
    url: string,
    method: Method,
    options?: {
      data?: Record<string, unknown> | Record<string, unknown>[] | string[];
      params?: Record<string, unknown>;
    },
    getAfterCreate = false,
  ): Promise<any> {
    const config: AxiosRequestConfig = {
      url: url,
      method: method,
      withCredentials: true,
    };

    if (options) {
      if (options.data) {
        if (Array.isArray(options.data)) {
          config["data"] = options.data.map((x) => {
            if (typeof x === "string") {
              return x;
            } else {
              return this.formatOutgoingData(x);
            }
          });
        } else {
          config["data"] = this.formatOutgoingData(options.data);
        }
      }

      if (options.params) {
        config["params"] = this.formatOutgoingData(options.params);
      }
    }

    const response = await instance.request(config).catch((error) => {
      throw error;
    });

    if (response) {
      if ("content-location" in response.headers && getAfterCreate) {
        return await this.read(response.headers["content-location"]);
      }

      if (Array.isArray(response.data)) {
        return response.data.map(this.formatIncomingData);
      }
      return this.formatIncomingData(response.data);
    }
    throw new Error(`${this.methodDict[method]} failed!`);
  }

  async create(
    url: string,
    data: Record<string, unknown> | Record<string, unknown>[],
    getAfterCreate: boolean,
  ): Promise<any> {
    return await this.baseRequest(url, "POST", { data: data }, getAfterCreate);
  }

  async read(url: string, params?: Record<string, unknown>): Promise<any> {
    return await this.baseRequest(url, "GET", { params: params });
  }

  async readAll(url: string, params?: Record<string, unknown>): Promise<any> {
    let results: any[] = [];
    let offset = 0;

    if (typeof params === "undefined") {
      params = {};
    }

    // eslint-disable-next-line no-constant-condition
    while (true) {
      params.offset = offset;
      const page: page = await this.read(url, params).catch((err) => {
        throw err;
      });

      results = results.concat(page.items);

      if (results.length < page.total) {
        offset = offset + page.limit;
        continue;
      }

      break;
    }

    return results;
  }

  async update(
    url: string,
    data?: Record<string, unknown> | Record<string, unknown>[],
  ): Promise<any> {
    return await this.baseRequest(url, "PATCH", { data: data });
  }
}
