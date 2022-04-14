import { genericObjectRead } from "@/models/base";

export const genericObjectReadFactory = ({
  description = "A generic object",
  uuid = "testObject1",
  value = "testObject",
  queues = undefined,
}: Partial<genericObjectRead> = {}): genericObjectRead => ({
  description: description,
  uuid: uuid,
  value: value,
  queues: queues,
});
