import { nodeThreatRead } from "@/models/nodeThreat";

export const nodeThreatReadFactory = ({
  description = "A test node threat",
  uuid = "nodeThreat1",
  value = "nodeThreat",
  types = [],
  queues = [],
}: Partial<nodeThreatRead> = {}): nodeThreatRead => ({
  description: description,
  uuid: uuid,
  value: value,
  types: types,
  queues: queues,
});
