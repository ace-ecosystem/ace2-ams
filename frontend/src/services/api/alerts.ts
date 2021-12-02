import { getAllParams } from "@/models/api";
import { GenericEndpoint } from "./base";
import { alertFilters } from "@/etc/constants";

class alert extends GenericEndpoint {
    getAll(params: getAllParams) {
        let param: keyof getAllParams;
        for (param in params) {
            const paramValue = params[param];
            const filterType = alertFilters.find((filter) => {
                return filter.name === param;
            });
            if (filterType && filterType.formatForAPI) {
                params[param] = filterType.formatForAPI(paramValue) as never;
            }
        }
        return super.getAll(params);
    }
}

export default new alert("/alert/");
