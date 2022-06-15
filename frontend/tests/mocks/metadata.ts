import { metadataRead } from "@/models/metadata";

export const metadataObjectReadFactory = ({
  description = "A metadata object",
  metadataType = "metadataObject",
  uuid = "testObject1",
  value = "testObject",
}: Partial<metadataRead> = {}): metadataRead => ({
  description: description,
  metadataType: metadataType,
  uuid: uuid,
  value: value,
});
