import { UUID } from "./base";

interface ObservableTypeBase {
  description?: string;
  value: string;
}

export interface ObservableTypeCreate extends ObservableTypeBase {
  uuid: UUID;
}

export interface ObservableTypeRead extends ObservableTypeBase {
  uuid: UUID;
}

export interface ObservableTypeUpdate extends ObservableTypeBase {
  value: string;
}
