import { describe, expect, it } from "vitest";
import { csrfHeaders, moduleEndpoint } from "./portal";

describe("portal API helpers", () => {
  it("maps supported modules to protected API endpoints", () => {
    expect(moduleEndpoint("assignments")).toBe("assignments/mine");
    expect(moduleEndpoint("admin")).toBe("admin/users");
    expect(moduleEndpoint("unknown")).toBeUndefined();
  });

  it("extracts and decodes the CSRF cookie without forwarding unrelated cookies", () => {
    expect(csrfHeaders("theme=navy; skec_csrf=token%2Fwith%20space")).toEqual({
      "X-CSRF-Token": "token/with space",
    });
    expect(csrfHeaders("theme=navy")).toEqual({});
  });
});
