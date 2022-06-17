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
        // Have to use URLSearchParams in order to have duplicate paramters correctly formatted
        // Passing an object like {foo: [1, 2, 3]} to axios will result in a query string of foo[]=1&foo[]=2&foo[]=3, which FastAPI doesn't like
        // By appending duplicate parameters to URLSearchParams as below, we can get the correct query string, foo=1&foo=2&foo=3
        const p = new URLSearchParams();
        const formattedParams = this.formatOutgoingData(options.params);
        for (const param in formattedParams) {
          // If the paramter is an array, then we need to append each element of the array to URLSearchParams
          if (Array.isArray(formattedParams[param])) {
            for (const item of formattedParams[param] as string) {
              p.append(param, item);
            }
          } else {
            // Otherwise, we can just append the parameter to URLSearchParams
            p.append(param, formattedParams[param] as string);
          }
        }
        config["params"] = p;
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

  async readAll(
    url: string,
    params?: Record<string, unknown>,
  ): Promise<Array<any>> {
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
