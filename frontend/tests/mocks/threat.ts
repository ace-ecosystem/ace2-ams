import { threatRead } from "@/models/threat";

export const threatReadFactory = ({
  description = "A test node threat",
  uuid = "threat1",
  value = "threat",
  types = [],
  queues = [],
}: Partial<threatRead> = {}): threatRead => ({
  description: description,
  uuid: uuid,
  value: value,
  types: types,
  queues: queues,
});
