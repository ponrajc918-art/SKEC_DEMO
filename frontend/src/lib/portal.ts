const moduleEndpoints: Record<string, string> = {
  attendance: "attendance/mine",
  timetable: "timetable/mine",
  assignments: "assignments/mine",
  results: "results/mine",
  fees: "fees/mine",
  notifications: "notifications/mine",
  announcements: "announcements/mine",
  students: "academic/students",
  admin: "admin/users",
};

export function moduleEndpoint(module: string): string | undefined {
  return moduleEndpoints[module];
}

export function csrfHeaders(cookie: string): Record<string, string> {
  const value = cookie
    .split("; ")
    .find((item) => item.startsWith("skec_csrf="))
    ?.slice("skec_csrf=".length);
  return value ? { "X-CSRF-Token": decodeURIComponent(value) } : {};
}
