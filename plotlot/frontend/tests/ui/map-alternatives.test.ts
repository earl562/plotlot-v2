import { describe, expect, it } from "vitest";

import { openStreetMapStaticUrl, openStreetMapUrl } from "@/lib/mapAlternatives";

describe("map alternatives", () => {
  it("builds an OpenStreetMap deep-link for coordinates", () => {
    const url = openStreetMapUrl(25.957, -80.199, 17);
    expect(url).toContain("openstreetmap.org");
    expect(url).toContain("mlat=25.957");
    expect(url).toContain("mlon=-80.199");
    expect(url).toContain("#map=17/25.957/-80.199");
  });

  it("builds an OpenStreetMap static map URL", () => {
    const url = openStreetMapStaticUrl(25.957, -80.199, 16);
    expect(url).toContain("staticmap.openstreetmap.de");
    expect(url).toContain("center=25.957,-80.199");
    expect(url).toContain("zoom=16");
    expect(url).toContain("markers=25.957,-80.199,red-pushpin");
  });
});
