import { alertCommentRead } from "@/models/alertComment";
import { eventCommentRead } from "@/models/eventComment";
import { userReadFactory } from "./user";

export const alertCommentReadFactory = ({
  insertTime = "2020-01-01T00:00:00.000000+00:00",
  submissionUuid = "uuid1",
  user = userReadFactory(),
  uuid = "commentUuid1",
  value = "A test alert comment",
}: Partial<alertCommentRead> = {}): alertCommentRead => ({
  insertTime: insertTime,
  submissionUuid: submissionUuid,
  user: user,
  uuid: uuid,
  value: value,
});

export const eventCommentReadFactory = ({
  insertTime = "2020-01-01T00:00:00.000000+00:00",
  eventUuid = "uuid1",
  user = userReadFactory(),
  uuid = "commentUuid1",
  value = "A test event comment",
}: Partial<eventCommentRead> = {}): eventCommentRead => ({
  insertTime: insertTime,
  eventUuid: eventUuid,
  user: user,
  uuid: uuid,
  value: value,
});
