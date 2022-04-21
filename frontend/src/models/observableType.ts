import CSS from "csstype";
import {
  genericObjectCreate,
  genericObjectRead,
  genericObjectReadPage,
  genericObjectUpdate,
} from "./base";
import { observableAction, observableActionSection } from "./observable";

export type observableTypeCreate = genericObjectCreate;

export type observableTypeRead = genericObjectRead;

export interface observableTypeReadPage extends genericObjectReadPage {
  items: observableTypeRead[];
}

export type observableTypeUpdate = genericObjectUpdate;

export type observableTypeMetaData = {
  actions?: observableAction[] | observableActionSection[];
  style?: CSS.Properties;
};
