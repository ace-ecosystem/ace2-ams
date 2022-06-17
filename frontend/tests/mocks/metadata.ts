import { metadataDirectiveRead } from "@/models/metadataDirective";
import { metadataDisplayTypeRead } from "@/models/metadataDisplayType";
import { metadataDisplayValueRead } from "@/models/metadataDisplayValue";
import { metadataTagRead } from "@/models/metadataTag";
import { metadataTimeRead } from "@/models/metadataTime";

export const metadataDirectiveReadFactory = ({
  description = "A directive object",
  uuid = "testObject1",
  value = "directive1",
}: Partial<metadataDirectiveRead> = {}): metadataDirectiveRead => ({
  description: description,
  metadataType: "directive",
  uuid: uuid,
  value: value,
});

export const metadataDisplayTypeReadFactory = ({
  description = "A display type object",
  uuid = "testObject1",
  value = "display_type1",
}: Partial<metadataDisplayTypeRead> = {}): metadataDisplayTypeRead => ({
  description: description,
  metadataType: "display_type",
  uuid: uuid,
  value: value,
});

export const metadataDisplayValueReadFactory = ({
  description = "A display value object",
  uuid = "testObject1",
  value = "display_value1",
}: Partial<metadataDisplayValueRead> = {}): metadataDisplayValueRead => ({
  description: description,
  metadataType: "display_value",
  uuid: uuid,
  value: value,
});

export const metadataTagReadFactory = ({
  description = "A tag object",
  uuid = "testObject1",
  value = "tag1",
}: Partial<metadataTagRead> = {}): metadataTagRead => ({
  description: description,
  metadataType: "tag",
  uuid: uuid,
  value: value,
});

export const metadataTimeReadFactory = ({
  description = "A time object",
  uuid = "testObject1",
  value = "2021-01-01T00:00:00.000000+00:00",
}: Partial<metadataTimeRead> = {}): metadataTimeRead => ({
  description: description,
  metadataType: "time",
  uuid: uuid,
  value: value,
});
