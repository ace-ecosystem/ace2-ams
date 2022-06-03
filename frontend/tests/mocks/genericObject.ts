import { genericObjectRead, genericQueueableObjectRead } from "@/models/base";

export const genericObjectReadFactory = ({
  description = "A generic object",
  uuid = "testObject1",
  value = "testObject",
}: Partial<genericObjectRead> = {}): genericObjectRead => ({
  description: description,
  uuid: uuid,
  value: value,
});

export const queueableObjectReadFactory = ({
  description = "A generic queueable object",
  uuid = "testObject1",
  value = "testObject",
  queues = [],
}: Partial<genericQueueableObjectRead> = {}): genericQueueableObjectRead => ({
  description: description,
  uuid: uuid,
  value: value,
  queues: queues,
});
