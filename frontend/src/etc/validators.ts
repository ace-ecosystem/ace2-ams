// https://stackoverflow.com/questions/1353684/detecting-an-invalid-date-date-instance-in-javascript

export function isValidDate(d: unknown): d is Date {
  return d instanceof Date && !isNaN(d.getTime());
}

export function isValidDateString(s: string): boolean {
  // Some of the strings passed into this function might have datetimes as substrings in them.
  // As on way of identifying these strings (that we want to not consider as valid dates),
  // look for the "@" character in the string.
  //
  // An example of this type of string would be the Owner row in the alert details table:
  // Owner: Test Analyst @ 5/4/2020, 12:00:00 PM UTC
  //
  // In these cases, the datetime should already be formatted in the string.
  return typeof s === "string" && !s.includes("@") && !isNaN(Date.parse(s));
}

export function isObject(o: unknown): o is Record<string, unknown> {
  return typeof o === "object" && o !== null;
}
