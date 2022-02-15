import { alertRead } from "./alert";
import { UUID } from "./base";
import { eventRead } from "./event";
import { observableRead } from "./observable";
import { readPage } from "./page";
import { userRead } from "./user";

interface diff {
  oldValue: boolean | string | null;
  newValue: boolean | string | null;
  addedToList: string[] | null;
  removedFromList: string[] | null;
}

interface historyBase {
  uuid: UUID;
  action: string;
  actionBy: userRead;
  actionTime: Date;
  recordUuid: UUID;
  field: string | null;
  diff: diff | null;
}

interface alertHistoryRead extends historyBase {
  snapshot: alertRead;
}

interface eventHistoryRead extends historyBase {
  snapshot: eventRead;
}

interface observableHistoryRead extends historyBase {
  snapshot: observableRead;
}

interface userHistoryRead extends historyBase {
  snapshot: userRead;
}

export interface alertHistoryReadPage extends readPage {
  items: alertHistoryRead[];
}

export interface eventHistoryReadPage extends readPage {
  items: eventHistoryRead[];
}

export interface observableHistoryReadPage extends readPage {
  items: observableHistoryRead[];
}

export interface userHistoryReadPage extends readPage {
  items: userHistoryRead[];
}
