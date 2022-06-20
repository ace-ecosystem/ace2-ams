import { nodeCommentRead } from "@/models/nodeComment";
import { userReadFactory } from "./user";

export const commentReadFactory = ({
  insertTime = "2020-01-01T00:00:00.000000+00:00",
  nodeUuid = "nodeUuid1",
  user = userReadFactory(),
  uuid = "commentUuid1",
  value = "A test comment",
}: Partial<nodeCommentRead> = {}): nodeCommentRead => ({
  insertTime: insertTime,
  nodeUuid: nodeUuid,
  user: user,
  uuid: uuid,
  value: value,
});
