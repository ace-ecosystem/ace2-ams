import { useAlertStore } from "./alert";
import { useAlertTableStore } from "./alertTable";
import { useEventStore } from "./event";
import { useEventTableStore } from "./eventTable";
import { useSelectedAlertStore } from "./selectedAlert";
import { useSelectedEventStore } from "./selectedEvent";

export const nodeStores = {
  alerts: useAlertStore,
  events: useEventStore,
};
export const nodeTableStores = {
  alerts: useAlertTableStore,
  events: useEventTableStore,
};
export const nodeSelectedStores = {
  alerts: useSelectedAlertStore,
  events: useSelectedEventStore,
};
