import { genericObjectRead, UUID } from "@/models/base";

export const genericObjectFactory = (
  description = "A test queue",
  uuid: UUID = "testQueue1",
  value = "testQueue",
): genericObjectRead => ({
  description: description,
  uuid: uuid,
  value: value,
});

