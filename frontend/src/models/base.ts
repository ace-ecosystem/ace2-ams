export type UUID = string;
export type genericObject = {
  description: string;
  value: string;
  uuid: UUID;
  rank?: string;
  types?: string;
};
export type genericGetAll = genericObject[];
