import { useAlertStore } from "./alert";
import { useAlertTableStore } from "./alertTable";
import { useEventStore } from "./event";
import { useEventTableStore } from "./eventTable";
import { useSelectedAlertStore } from "./selectedAlert";
import { useSelectedEventStore } from "./selectedEvent";

export const objectStores = {
  alerts: useAlertStore,
  events: useEventStore,
};
export const objectTableStores = {
  alerts: useAlertTableStore,
  events: useEventTableStore,
};
export const objectSelectedStores = {
  alerts: useSelectedAlertStore,
  events: useSelectedEventStore,
};
