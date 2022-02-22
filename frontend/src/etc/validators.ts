// https://stackoverflow.com/questions/1353684/detecting-an-invalid-date-date-instance-in-javascript

export function isValidDate(d: unknown): d is Date {
return d instanceof Date && !isNaN(d.getTime());
}

export function isObject(o: unknown): o is Record<string, unknown> {
return typeof o === "object" && o !== null;
}
